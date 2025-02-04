# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional
import glob
import json

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

from . import config
from .graphics import Graphics
from .player import heroes, PlayerInfo, Team
from .monsters import MonsterInfo
from .music import play_music
from .loot import Loot, LootInfo
from .worlds import Forest, Desert, Mountain, Mine


class Engine:
    def __init__(
        self,
        team: Team,
        world: str = "forest",
        safe: bool = False,
        seed: Optional[int] = None,
        follow: bool = False,
        music: bool = False,
        side: str = None,
        restart: str | int | None = None,
        xp_cheat: float | None = 1.0,
    ):
        # Set the seed
        # BitGen = type(config.rng.bit_generator)
        # config.rng.bit_generator.state = BitGen(seed).state

        self.team = team
        match world:
            case "forest":
                self.world = Forest()
            case "desert":
                self.world = Desert()
            case "mountain":
                self.world = Mountain()
            case "mine":
                self.world = Mine()
        # if seed is not None:
        #     np.random.seed(seed)
        self._music = music
        self.safe = safe
        self._follow = follow
        self.game_ended = False
        self.monster_info = {}

        self.bots = {p.hero: p for p in team.players}

        # Distribute players in ring around center
        start_x = []
        start_y = []
        r = 100.0
        for i in range(len(team.players)):
            angle = i * 2 * np.pi / len(team.players)
            start_x.append(r * np.cos(angle))
            start_y.append(r * np.sin(angle))

        self.players = {
            p.hero: heroes[p.hero](x=start_x[i], y=start_y[i])
            for i, p in enumerate(team.players)
        }

        self.graphics = Graphics(players=self.players, world=self.world, side=side)

        for player in self.players.values():
            player.add_to_graphics()
            player.weapon.add_to_graphics()

        self.xp = 0.0
        self.dxp = 1.05
        self.xp_step = 20.0
        self.next_xp = self.xp_step
        self.xpmult = xp_cheat if xp_cheat is not None else 1.0

        # Create loot objects
        self.chicken = Loot(size=300, kind="chicken")
        self.treasures = Loot(size=150, kind="treasure")

        # Create monster hordes
        self.monsters = self.world.monsters

        # Add all sprites to the graphics
        self.graphics.add(self.chicken.sprites)
        self.graphics.add(self.treasures.sprites)

        for horde in self.monsters:
            horde.make_sprites()
            self.graphics.add(horde.sprites)

        for player in self.players.values():
            self.graphics.add(player.avatar)
            self.graphics.add(player.dead_avatar)
            self.graphics.add(player.weapon.sprites)

        self.dt = 1.0 / config.fps
        self.player_center = np.array([0.0, 0.0])

        if restart is not None:
            self.restart_from_state(restart)

        self.graphics.update_player_status(self.players, xp=self.xp, t=0)
        self.move_camera()

    def restart_from_state(self, restart):
        if restart == -1:
            # Find the most recent state file
            restart = sorted(glob.glob("state-*.json"), reverse=True)[-1]
        state = json.load(open(restart))
        for hero, info in state["players"].items():
            self.players[hero].from_dict(info)
        for i, info in enumerate(state["monsters"]):
            self.monsters[i].from_dict(info)
        self.xp = state["xp"]
        self.next_xp = state["next_xp"]
        self.xp_step = state["xp_step"]
        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        self.dt = state["dt"]

    def make_player_info(self):
        player_info = {}
        for name, player in self.players.items():
            info = player.as_dict()
            del info["hero"]
            player_info[name] = PlayerInfo(**info)
        return player_info

    def make_loot_info(self):
        loot_info = {}
        distances = np.linalg.norm(self.chicken.positions - self.player_center, axis=1)
        visible = distances <= config.view_radius
        if visible.sum() > 0:
            loot_info["chicken"] = LootInfo(
                kind="chicken",
                x=self.chicken.positions[visible, 0],
                y=self.chicken.positions[visible, 1],
            )
        distances = np.linalg.norm(
            self.treasures.positions - self.player_center, axis=1
        )
        visible = distances <= config.view_radius
        if visible.sum() > 0:
            loot_info["treasures"] = LootInfo(
                kind="treasure",
                x=self.treasures.positions[visible, 0],
                y=self.treasures.positions[visible, 1],
                xp=self.treasures.xp[visible],
            )
        return loot_info

    def call_player_bots(self, t: float, dt: float):
        player_info = self.make_player_info()
        loot_info = self.make_loot_info()
        for name in self.bots:
            if self.safe:
                try:
                    move = self.bots[name].run(
                        t=t,
                        dt=dt,
                        monsters=self.monster_info,
                        players=player_info,
                        pickups=loot_info,
                    )
                    self.players[name].execute_bot_instructions(move)
                except:  # noqa
                    pass
            else:
                move = self.bots[name].run(
                    t=t,
                    dt=dt,
                    monsters=self.monster_info,
                    players=player_info,
                    pickups=loot_info,
                )
                self.players[name].execute_bot_instructions(move)

    def fight(self, t: float):
        # Make a list of all the players and the projectiles their weapon has fired.
        # Then make a list of all the monsters from all the hordes.
        # Compute a matrix of distances between (players + projectiles) and monsters.
        # If any monster is within the radius of a projectile, the monster takes damage
        # equal to the projectile's damage.
        # If the monster's health is less than or equal to zero, the monster is
        # destroyed.
        # If any monster is within the radius of a player, the player takes damage equal
        # to the monster's damage. If the player's health is less than or equal to
        # zero, the player is destroyed.

        # Combine all hero and projectile positions
        player_list = [p for p in self.players.values() if p.alive]

        projectiles = [
            proj for player in player_list for proj in player.weapon.projectiles
        ]
        players_and_projectiles = player_list + projectiles
        good_positions = np.concatenate(
            [pp.position.reshape(1, 2) for pp in players_and_projectiles]
        )
        good_healths = np.array([pp.health for pp in players_and_projectiles])
        good_attacks = np.array([pp.attack for pp in players_and_projectiles])
        good_radius = np.array([pp.radius for pp in players_and_projectiles])
        good_freeze = np.array([(pp.freeze + t) for pp in players_and_projectiles])

        # Find center of mass of players and projectiles
        center = np.mean(good_positions, axis=0)
        self.player_center = np.mean(
            np.concatenate([pp.position.reshape(1, 2) for pp in player_list]), axis=0
        )
        # Find radius of object furthest from center
        max_radius = np.max(
            np.linalg.norm(good_positions - center, axis=1) + good_radius
        )

        # Filter out monsters that are too far away
        evil_positions = []
        evil_healths = []
        evil_attacks = []
        evil_radius = []
        evil_masks = []
        visible_evil = []

        for horde in self.monsters:
            distances = np.linalg.norm(horde.positions - center, axis=1)
            mask = distances < max_radius + 150.0
            evil_positions.append(horde.positions[mask, :])
            evil_healths.append(horde.healths[mask])
            evil_attacks.append(horde.attacks[mask])
            evil_radius.append(horde.radii[mask])
            evil_masks.append(mask)

            distances = np.linalg.norm(horde.positions - self.player_center, axis=1)
            visible_evil.append(distances <= config.view_radius)

        evil_positions = np.concatenate(evil_positions)
        evil_healths = np.concatenate(evil_healths)
        evil_attacks = np.concatenate(evil_attacks)
        evil_radius = np.concatenate(evil_radius)

        # Compute pairwise distances
        distances = np.linalg.norm(
            evil_positions[:, np.newaxis, :] - good_positions[np.newaxis, :, :], axis=2
        )
        sum_of_radii = evil_radius[:, np.newaxis] + good_radius[np.newaxis, :]

        # Find the closest monster to each player
        closest_monster_positions = None
        if len(evil_healths) > 0:
            closest_monster_indices = np.argmin(distances, axis=0)
            closest_monster_positions = evil_positions[closest_monster_indices, :]

        # Find indices where distances are less than sum of radii
        mask = (distances < sum_of_radii).astype(int)
        monster_damage = np.broadcast_to(good_attacks.reshape(1, -1), mask.shape) * mask
        monster_freeze = np.broadcast_to(good_freeze.reshape(1, -1), mask.shape) * mask
        player_damage = np.broadcast_to(evil_attacks.reshape(-1, 1), mask.shape) * mask
        evil_healths -= monster_damage.sum(axis=1)
        good_healths -= player_damage.sum(axis=0)
        evil_freeze = monster_freeze.max(axis=1)

        for pp, health in zip(players_and_projectiles, good_healths):
            pp.health = health

        # Apply healing from weapons
        # Compute distances between players and projectiles
        # If any player is within a projectile radius, the player is healed
        # equal to the projectile's healing power
        if len(projectiles) > 0:
            distances = np.linalg.norm(
                np.concatenate([pp.position.reshape(1, 2) for pp in player_list])[
                    :, np.newaxis, :
                ]
                - np.concatenate([proj.position.reshape(1, 2) for proj in projectiles])[
                    np.newaxis, :, :
                ],
                axis=2,
            )
            mask = (distances < np.array([proj.radius for proj in projectiles])).astype(
                int
            )
            healing = (
                np.broadcast_to(
                    np.array([proj.healing for proj in projectiles]).reshape(1, -1),
                    mask.shape,
                )
                * mask
            ).sum(axis=1)
        else:
            healing = np.zeros(len(player_list))

        for i, player in enumerate(player_list):
            if closest_monster_positions is not None:
                player._closest_monster = closest_monster_positions[i, :]
            else:
                player._closest_monster = None
            player.health = min(player.health + healing[i] * self.dt, player.max_health)
            if player.health <= 0:
                player.die(t=t)
            player.weapon.projectiles = [
                proj for proj in player.weapon.projectiles if proj.health > 0
            ]

        n = 0
        self.monster_info.clear()
        for i, horde in enumerate(self.monsters):
            size = evil_masks[i].sum()
            horde.healths[evil_masks[i]] = evil_healths[n : n + size]
            horde.freezes[evil_masks[i]] = np.maximum(
                horde.freezes[evil_masks[i]], evil_freeze[n : n + size]
            )

            # Save the visible monsters
            visible = visible_evil[i] & (horde.healths > 0)
            nvisible = visible.sum()
            if nvisible > 0:
                self.monster_info[horde.kind] = MonsterInfo(
                    x=horde.positions[visible, 0].copy(),
                    y=horde.positions[visible, 1].copy(),
                    healths=horde.healths[visible].copy(),
                    attacks=horde.attacks[visible].copy(),
                    radii=horde.radii[visible].copy(),
                    speeds=np.full(shape=nvisible, fill_value=horde.speed),
                )

            inds = np.where(horde.healths <= 0)[0]
            ndead = len(inds)
            if ndead > 0:
                new_pos = horde.positions.copy()
                new_pos[inds, :] = horde.make_positions(
                    ndead, offset=horde.positions[inds]
                )
                horde.positions = new_pos
                horde.healths[inds] = horde.xp
                self.xp += ndead * horde.xp * self.xpmult
            n += size

    def resolve_xp(self, t: float):
        if self.xp < self.next_xp:
            return
        self.xp_step *= self.dxp
        self.next_xp += self.xp_step
        print("Leveling up:", self.xp, self.next_xp, self.xp_step)
        lup = self.team.strategist.levelup(
            t=t,
            info={"xp": float(self.xp), "next_levelup": float(self.next_xp)},
            players=self.make_player_info(),
        )
        if lup is not None:
            print(f"Leveling up {lup.hero} with {lup.what}")
            self.players[lup.hero].levelup(lup.what)
            # print(self.players[lup.hero].as_dict())

    def move_camera(self):
        positions = np.array([[p.x, p.y] for p in self.players.values()])
        xmin, ymin = np.min(positions, axis=0)
        xmax, ymax = np.max(positions, axis=0)
        dxmin = 900.0
        if (xmax - xmin) < dxmin:
            padding = 0.5 * dxmin - 0.5 * (xmax - xmin)
            xmin -= padding
            xmax += padding
        dymin = 900.0
        if ymax - ymin < dymin:
            padding = 0.5 * dymin - 0.5 * (ymax - ymin)
            ymin -= padding
            ymax += padding
        self.graphics.viewbox.setRange(xRange=(xmin, xmax), yRange=(ymin, ymax))

    def resolve_pickup(self):
        for player in self.players.values():
            pos = player.position
            if self.chicken.maybe_pickup(pos):
                player.health = min(
                    player.health + 0.5 * player.max_health, player.max_health
                )
            maybe_xp = self.treasures.maybe_pickup(pos)
            if maybe_xp:
                self.xp += maybe_xp * self.xpmult

    def update(self):
        t = self.elapsed_timer.elapsed() / 1000.0
        alive_players = [p for p in self.players.values() if p.alive]
        if len(alive_players) == 0:
            if not self.game_ended:
                self.graphics.update_player_status(self.players, xp=self.xp, t=t)
                self.graphics.update_time(t=t)
                self.game_ended = True
            return

        self.call_player_bots(t=t, dt=self.dt)
        dead_players = [p for p in self.players.values() if not p.alive]
        for player in alive_players:
            player.move(self.dt)
            if t > player.weapon.timer:
                player.weapon.fire(player.position, t)
            player.weapon.update(t, self.dt)
        for horde in self.monsters:
            horde.move(t, self.dt, players=alive_players)

        if self._follow:  # and (int(t * 3) % 3 == 0):
            self.move_camera()

        self.resolve_pickup()
        self.fight(t=t)
        self.resolve_xp(t=t)
        for player in dead_players:
            player.maybe_respawn(t=t)

        # Update player status every 10 frames
        if int(t * 10) % 10 == 0:
            self.graphics.update_player_status(self.players, xp=self.xp, t=t)
            self.graphics.update_time(t=t)

    def run(self):
        if self._music:
            play_music(self.world.name)

        timer = QtCore.QTimer()
        self.elapsed_timer = QtCore.QElapsedTimer()
        timer.timeout.connect(self.update)
        timer.start(1000.0 * self.dt)
        # timer.start(330)
        self.elapsed_timer.start()
        pg.exec()

        # # Dump state at the end of the run
        # state = {
        #     "players": {p.hero: p.as_dict() for p in self.players.values()},
        #     "monsters": [m.as_dict() for m in self.monsters],
        #     "loot": {
        #         "chicken": self.chicken.as_dict(),
        #         "treasures": self.treasures.as_dict(),
        #     },
        #     "xp": self.xp,
        #     "next_xp": self.next_xp,
        #     "xp_step": self.xp_step,
        #     "elapsed": self.elapsed_timer.elapsed() / 1000.0,
        #     "dt": self.dt,
        # }
        # now = str(datetime.datetime.now()).replace(" ", "-").replace(":", "-")
        # json.dump(state, open(f"state-{now}.json", "w"))
