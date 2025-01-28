# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional
import glob
import json

import numpy as np

# import pyglet

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

try:
    # import vlc
    # from playsound import playsound
    from pygame import mixer
except ImportError:
    # vlc = None
    # playsound = None
    mixer = None
# from pyglet.window import key


# from .asteroid import Asteroid
from . import config
from .graphics import Graphics
from .player import Team, heroes
from .loot import Loot
from .monsters import Monsters

# from .scores import finalize_scores
# from .terrain import Terrain
# from .tools import AsteroidInfo, Instructions, PlayerInfo, image_to_sprite


# @dataclass
# class Position:
#     x: float
#     y: float


# @dataclass
# class Monster:
#     vector: Tuple[float, float]
#     image: Image


# def add_key_actions(window, pos: Position):
#     @window.event
#     def on_key_press(symbol, modifiers):
#         delta = 20
#         if symbol == pyglet.window.key.UP:
#             pos.y += delta
#         elif symbol == pyglet.window.key.DOWN:
#             pos.y -= delta
#         elif symbol == pyglet.window.key.LEFT:
#             pos.x -= delta
#         elif symbol == pyglet.window.key.RIGHT:
#             pos.x += delta

# @window.event
# def on_key_release(symbol, modifiers):
#     if symbol == pyglet.window.key.UP:
#         player.main_thruster = False
#     elif symbol == pyglet.window.key.LEFT:
#         player.left_thruster = False
#     elif symbol == pyglet.window.key.RIGHT:
#         player.right_thruster = False


class Engine:
    def __init__(
        self,
        # bots: list,
        # test: bool = True,
        team: Team,
        world: str = "forest",
        safe: bool = False,
        seed: Optional[int] = None,
        # fullscreen: bool = False,
        follow: bool = False,
        manual: bool = False,
        music: bool = False,
        side: str = None,
        restart: str | int | None = None,
        # crater_scaling: float = 1.0,
        # player_collisions: bool = True,
        # asteroid_collisions: bool = True,
        # speedup: float = 1.0,
    ):
        # Set the seed
        # BitGen = type(config.rng.bit_generator)
        # config.rng.bit_generator.state = BitGen(seed).state

        self.team = team
        self.world = world
        # if seed is not None:
        #     np.random.seed(seed)
        self._manual = manual
        self._music = music
        self.safe = safe
        self._follow = follow

        # self.graphics = Graphics(manual=manual)

        # v1 = np.array([1.0, 1.0])
        # v2 = np.array([0.9, 1.0])

        # self.players = [
        #     Player(vector=v1 / np.linalg.norm(v1), weapon="runetracer"),
        #     Player(vector=v2 / np.linalg.norm(v2), weapon="runetracer"),
        # ]
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

        self.graphics = Graphics(
            players=self.players, world=self.world, manual=manual, side=side
        )

        for player in self.players.values():
            player.add_to_graphics()
            player.weapon.add_to_graphics()

        if self._manual:
            self.graphics.set_hero(self.players[0])

        self.xp = 0.0
        self.dxp = 1.05
        self.xp_step = 20.0
        self.next_xp = self.xp_step

        # self.nx = config.nx
        # self.ny = config.ny
        # self.start_time = None
        # # self._test = test
        # # self.asteroids = []
        # # self.exiting = False
        # # self.time_of_last_scoreboard_update = 0
        # # self.time_of_last_asteroid = 0
        # # self._crater_scaling = crater_scaling
        # # self._player_collisions = player_collisions
        # # self._asteroid_collisions = asteroid_collisions
        # # self._speedup = speedup
        # self.position = Position(x=5000, y=5000)
        # self.scale = 1.0

        # self.game_map = Terrain()

        # self.key_state_handler = key.KeyStateHandler()
        # self.graphics.window.push_handlers(self.key_state_handler)

        # zombie_image = Image.open(config.resources / "bat.png").convert("RGBA")

        # scenery = make_scenery(world=world)
        # for sprites in scenery:
        #     self.graphics.add(sprites)

        self.chicken = Loot(size=300, kind="chicken")
        self.treasures = Loot(size=150, kind="treasure")

        s = 32.0
        d = 25.0
        self.monsters = [
            Monsters(size=2000, kind="bat", distance=400.0 * d, scale=100 * s),
            Monsters(size=2000, kind="rottingghoul", distance=600 * d, scale=100 * s),
            Monsters(size=500, kind="giantbat", distance=800 * d, scale=100 * s),
            Monsters(size=500, kind="thereaper", distance=1000 * d, scale=100 * s),
        ]

        self.graphics.add(self.chicken.sprites)
        self.graphics.add(self.treasures.sprites)

        for horde in self.monsters:
            self.graphics.add(horde.sprites)

        for player in self.players.values():
            self.graphics.add(player.avatar)
            self.graphics.add(player.dead_avatar)
            self.graphics.add(player.weapon.sprites)
            # player.weapon.fire(0, 0, 0)

        # self.start_button = ipw.Button(description="Start!")
        # self.start_button.on_click(self.run)

        # self.camera_lock = ipw.ToggleButton(
        #     icon="lock",
        #     tooltip="Lock camera",
        #     value=True,
        #     layout={"width": "40px"},
        # )
        # # self.camera_lock.observe(self.toggle_camera_lock, names="value")

        # self.toolbar = ipw.HBox([self.start_button, self.camera_lock])

        self.dt = 1.0 / config.fps
        # self._previous_t = 0.0

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

    # def execute_player_bot(self, team: str, info: dict) -> Instructions:
    #     instructions = None
    #     if self.safe:
    #         try:
    #             instructions = self.bots[team].run(**info)
    #         except:  # noqa
    #             pass
    #     else:
    #         instructions = self.bots[team].run(**info)
    #     return instructions

    def call_player_bots(self, t: float, dt: float):
        # info = {"dt": dt, "board": self.board_new.copy()}
        # info["players"] = {
        #     team: PlayerInfo(**p.to_dict()) for team, p in self.players.items()
        # }
        # info["powerups"] = [PowerupInfo(**p.to_dict()) for p in self.powerups]
        # for player in (p for p in self.active_players() if p.team != self._manual):
        player_info = [p.as_dict() for p in self.players.values()]
        for name in self.bots:
            if self.safe:
                try:
                    move = self.bots[name].run(
                        t=t, dt=dt, monsters=None, players=player_info
                    )
                    self.players[name].execute_bot_instructions(move)
                except:  # noqa
                    pass
            else:
                move = self.bots[name].run(
                    t=t, dt=dt, monsters=None, players=player_info
                )
                self.players[name].execute_bot_instructions(move)

    def fight(self, t: float):
        # Make a list of all the players and the projectiles their weapon has fired.
        # Then make a list of all the monsters from all the hordes.
        # Compute a matrix of distances between (players + projectiles) and monsters.
        # If any monster is within 5 pixels of a projectile, the monster takes damage
        # equal to the projectile's damage.
        # If the monster's health is less than or equal to zero, the monster is
        # destroyed.
        # If any monster is within 5 pixels of a player, the player takes damage equal
        # to the monster's damage. If the player's health is less than or equal to
        # zero, the player is destroyed.
        # # Combine all monster positions, healths, and attacks
        # evil_positions = np.concatenate([horde.positions for horde in self.monsters])
        # evil_healths = np.concatenate([horde.healths for horde in self.monsters])
        # evil_attacks = np.concatenate([horde.attacks for horde in self.monsters])
        # evil_radius = np.concatenate([horde.radii for horde in self.monsters])

        # Combine all hero and projectile positions
        # player_list = list(self.players.values())
        player_list = [p for p in self.players.values() if p.alive]

        # TODO: remove this once we exit game when all players are dead
        if len(player_list) == 0:
            return

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
        for horde in self.monsters:
            distances = np.linalg.norm(horde.positions - center, axis=1)
            mask = distances < max_radius + 100.0
            # print(mask.shape)
            evil_positions.append(horde.positions[mask, :])
            evil_healths.append(horde.healths[mask])
            evil_attacks.append(horde.attacks[mask])
            evil_radius.append(horde.radii[mask])
            evil_masks.append(mask)

        # print(
        #     "selected",
        #     sum([m.sum() for m in evil_masks]),
        #     "monsters within r=",
        #     max_radius + 100.0,
        # )

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

        # Find indices where distances are less than 5
        # mask = (distances < config.hit_radius * config.scaling).astype(int)
        # mask = (distances < config.hit_radius).astype(int)
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
        distances = np.linalg.norm(
            np.concatenate([pp.position.reshape(1, 2) for pp in player_list])[
                :, np.newaxis, :
            ]
            - np.concatenate([proj.position.reshape(1, 2) for proj in projectiles])[
                np.newaxis, :, :
            ],
            axis=2,
        )
        mask = (distances < np.array([proj.radius for proj in projectiles])).astype(int)
        healing = (
            np.broadcast_to(
                np.array([proj.healing for proj in projectiles]).reshape(1, -1),
                mask.shape,
            )
            * mask
        ).sum(axis=1)

        # # Find the closest monster to each player
        # closest_monster_indices = np.argmin(distances, axis=0)
        # print(closest_monster_indices)
        # closest_monster_positions = evil_positions[closest_monster_indices, :]

        # for i, player in enumerate(self.players.values()):
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
        for i, horde in enumerate(self.monsters):
            # horde.healths = evil_healths[i * horde.size : (i + 1) * horde.size]
            size = evil_masks[i].sum()
            # horde.healths[evil_masks[i]] = evil_healths[n : n + horde.size]
            horde.healths[evil_masks[i]] = evil_healths[n : n + size]
            horde.freezes[evil_masks[i]] = np.maximum(
                horde.freezes[evil_masks[i]], evil_freeze[n : n + size]
            )
            inds = np.where(horde.healths <= 0)[0]
            ndead = len(inds)
            # print("ndead", ndead)
            if ndead > 0:
                new_pos = horde.positions.copy()
                new_pos[inds, :] = horde.make_positions(
                    ndead, offset=horde.positions[inds]
                )
                horde.positions = new_pos
                # horde.positions[inds, :] = horde.make_positions(
                #     ndead, offset=player.position
                # )
                horde.healths[inds] = horde.xp
                self.xp += ndead * horde.xp
            n += size

        # if len(evil_indices) > 0:
        #     print("distances.shape", distances.shape)
        #     print("evil_indices", evil_indices)
        #     print("good_indices", good_indices)
        #     # Resolve damage
        #     # Deduct health from monsters

        return

        # good_troops = np.concatenate(
        #     [
        #         np.array([p.position for p in self.players]),
        #         *[p.weapon.positions[: p.weapon.nprojectiles] for p in self.players],
        #     ]
        # )
        # bad_troops = np.concatenate([m.positions for m in self.monsters])
        # print(good_troops.shape, bad_troops.shape)
        # assert False

    def resolve_xp(self, t: float):
        # print("self.xp", self.xp, "self.next_xp", self.next_xp)
        if self.xp < self.next_xp:
            return
        self.xp_step *= self.dxp
        self.next_xp += self.xp_step
        print("Leveling up:", self.xp, self.next_xp, self.xp_step)
        player_info = [p.as_dict() for p in self.players.values()]
        lup = self.team.strategist.levelup(
            t=t,
            info={"xp": float(self.xp), "next_levelup": float(self.next_xp)},
            players=player_info,
        )
        if lup is not None:
            print(f"Leveling up {lup.hero} with {lup.what}")
            self.players[lup.hero].levelup(lup.what)
            print(self.players[lup.hero].as_dict())

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
                self.xp += maybe_xp

    def update(self):
        t = self.elapsed_timer.elapsed() / 1000.0
        # print("dt", t - self._previous_t)
        # self._previous_t = t
        self.call_player_bots(t=t, dt=self.dt)
        alive_players = [p for p in self.players.values() if p.alive]
        dead_players = [p for p in self.players.values() if not p.alive]
        for player in alive_players:
            player.move(self.dt)
            if t > player.weapon.timer:
                player.weapon.fire(player.position, t)
            player.weapon.update(t, self.dt)
        # if self.camera_lock.value:
        #     # player center of mass
        #     x, y = np.mean([[p.x, p.y] for p in self.players], axis=0)
        #     self.graphics.camera.position = [x, y, self.graphics.camera.position[2]]
        #     lookat = [x, y, 0]
        #     self.graphics.controller.target = lookat
        #     self.graphics.camera.lookAt(lookat)
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

        # # Set camera position to player center of mass
        # x, y = np.mean([[p.x, p.y] for p in self.players], axis=0)

        if self._manual:
            self.graphics.update()

    def run(self):
        # if playsound is not None and self._music:
        #     self.music = playsound(
        #         str(config.resources / "levels" / "forest" / "forest.mp3")
        #     )
        #     # self.music.play()
        # # else:
        # #     self.music = None
        if mixer is not None and self._music:
            mixer.init()
            mixer.music.load(
                str(config.resources / "worlds" / self.world / f"{self.world}.mp3")
            )
            mixer.music.play(-1)

        # # for playing note.wav file
        # playsound('/path/note.wav')
        # print('playing sound using  playsound')

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
