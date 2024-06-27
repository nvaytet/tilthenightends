# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional

import numpy as np

# import pyglet

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

try:
    # import vlc
    from playsound import playsound
    from pygame import mixer  # Load the popular external library
except ImportError:
    # vlc = None
    playsound = None
    mixer = None
# from pyglet.window import key


# from .asteroid import Asteroid
from . import config
from .graphics import Graphics
from .player import Player
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
        # safe: bool = False,
        # test: bool = True,
        seed: Optional[int] = None,
        # fullscreen: bool = False,
        manual: bool = False,
        music: bool = False,
        # crater_scaling: float = 1.0,
        # player_collisions: bool = True,
        # asteroid_collisions: bool = True,
        # speedup: float = 1.0,
    ):
        if seed is not None:
            np.random.seed(seed)
        self._manual = manual
        self._music = music

        self.graphics = Graphics(manual=manual)

        v1 = np.array([1.0, 1.0])
        v2 = np.array([0.9, 1.0])

        self.players = [
            Player(vector=v1 / np.linalg.norm(v1), weapon="runetracer"),
            Player(vector=v2 / np.linalg.norm(v2), weapon="runetracer"),
        ]

        if self._manual:
            self.graphics.set_hero(self.players[0])

        # self.nx = config.nx
        # self.ny = config.ny
        # self.start_time = None
        # # self._test = test
        # # self.asteroids = []
        # # self.safe = safe
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

        self.monsters = [
            Monsters(size=2000, kind="bat", distance=400.0, scale=100),
            Monsters(size=2000, kind="rottingghoul", distance=600, scale=100),
            Monsters(size=500, kind="giantbat", distance=800, scale=100),
            Monsters(size=500, kind="thereaper", distance=1000, scale=100),
        ]
        for horde in self.monsters:
            self.graphics.add(horde.sprites)

        for player in self.players:
            self.graphics.add(player.avatar)
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

    def fight(self):
        # # Compute distances between players and monsters. If any monster is within 5
        # # pixels of a hero, the monster is destroyed.
        # for player in self.players:
        #     for horde in self.monsters:
        #         distances = np.linalg.norm(player.position - horde.positions, axis=1)
        #         inds = np.where(distances < config.hit_radius * config.scaling)[0]
        #         ndead = len(inds)
        #         if ndead > 0:
        #             horde.positions[inds, :] = horde.make_positions(
        #                 ndead, offset=player.position
        #             )

        # Make a list of all the players and the projectiles their weapon has fired.
        # Then make a list of all the monsters from all the hordes.
        # Compute a matrix of distances between (players + projectiles) and monsters.
        # If any monster is within 5 pixels of a projectile, the monster takes damage
        # equal to the projectile's damage. If the monster's health is less than or equal
        # to zero, the monster is destroyed.
        # If any monster is within 5 pixels of a player, the player takes damage equal to
        # the monster's damage. If the player's health is less than or equal to zero, the
        # player is destroyed.
        # Combine all monster positions, healths, and attacks
        evil_positions = np.concatenate([horde.positions for horde in self.monsters])
        evil_healths = np.concatenate([horde.healths for horde in self.monsters])
        evil_attacks = np.concatenate([horde.attacks for horde in self.monsters])

        # Combine all hero and projectile positions
        players_and_projectiles = self.players + [
            proj for player in self.players for proj in player.weapon.projectiles
        ]
        good_positions = np.concatenate(
            [pp.position.reshape(1, 2) for pp in players_and_projectiles]
        )
        good_healths = np.array([pp.health for pp in players_and_projectiles])
        good_attacks = np.array([pp.attack for pp in players_and_projectiles])
        #     [player.position.reshape(1, 2) for player in self.players]
        # )
        # projectile_positions = np.concatenate(
        #     [
        #         proj.position.reshape(1, 2)
        #         for player in self.players
        #         for proj in player.weapon.projectiles
        #     ]
        # )
        # good_positions = np.concatenate([player_positions, projectile_positions])
        # good_healths = np.concatenate(
        #     [player.health for player in self.players]
        #     + [
        #         proj.health
        #         for player in self.players
        #         for proj in player.weapon.projectiles
        #     ]
        # )
        # good_attacks = np.concatenate(
        #     [player.attack for player in self.players]
        #     + [
        #         proj.attack
        #         for player in self.players
        #         for proj in player.weapon.projectiles
        #     ]
        # )

        # print("good_positions.shape", good_positions.shape)

        # print((evil_positions[:, np.newaxis] - good_positions[np.newaxis, :]).shape)

        # Compute pairwise distances
        distances = np.linalg.norm(
            evil_positions[:, np.newaxis, :] - good_positions[np.newaxis, :, :], axis=2
        )

        # distances = np.linalg.norm(
        #     evil_positions[, np.newaxis] - good_positions[np.newaxis, :],
        #     axis=2,
        # )

        # Find indices where distances are less than 5
        # evil_indices, good_indices = np.where(distances < 5)
        mask = (distances < config.hit_radius * config.scaling).astype(int)
        monster_damage = np.broadcast_to(good_attacks.reshape(1, -1), mask.shape) * mask
        player_damage = np.broadcast_to(evil_attacks.reshape(-1, 1), mask.shape) * mask
        evil_healths -= monster_damage.sum(axis=1)
        good_healths -= player_damage.sum(axis=0)

        for pp, health in zip(players_and_projectiles, good_healths):
            pp.health = health
            # if pp.health <= 0:
            #     pp.die()
        for player in self.players:
            if player.health <= 0:
                player.die()
            player.weapon.projectiles = [
                proj for proj in player.weapon.projectiles if proj.health > 0
            ]

        for i, horde in enumerate(self.monsters):
            horde.healths = evil_healths[i * horde.size : (i + 1) * horde.size]
            inds = np.where(horde.healths <= 0)[0]
            ndead = len(inds)
            if ndead > 0:
                horde.positions[inds, :] = horde.make_positions(
                    ndead, offset=player.position
                )

        # if len(evil_indices) > 0:
        #     print("distances.shape", distances.shape)
        #     print("evil_indices", evil_indices)
        #     print("good_indices", good_indices)
        #     # Resolve damage
        #     # Deduct health from monsters

        return

        good_troops = np.concatenate(
            [
                np.array([p.position for p in self.players]),
                *[p.weapon.positions[: p.weapon.nprojectiles] for p in self.players],
            ]
        )
        bad_troops = np.concatenate([m.positions for m in self.monsters])
        print(good_troops.shape, bad_troops.shape)
        assert False

    def update(self):
        t = self.elapsed_timer.elapsed() / 1000.0
        for player in self.players:
            player.move(self.dt)
            if t > player.weapon.timer:
                player.weapon.fire(player.position, t)
            player.weapon.update(self.dt)
        # if self.camera_lock.value:
        #     # player center of mass
        #     x, y = np.mean([[p.x, p.y] for p in self.players], axis=0)
        #     self.graphics.camera.position = [x, y, self.graphics.camera.position[2]]
        #     lookat = [x, y, 0]
        #     self.graphics.controller.target = lookat
        #     self.graphics.camera.lookAt(lookat)
        for horde in self.monsters:
            horde.move(self.dt, players=self.players)

        self.fight()

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
            mixer.music.load(str(config.resources / "levels" / "forest" / "forest.mp3"))
            mixer.music.play()

        # # for playing note.wav file
        # playsound('/path/note.wav')
        # print('playing sound using  playsound')

        timer = QtCore.QTimer()
        self.elapsed_timer = QtCore.QElapsedTimer()
        timer.timeout.connect(self.update)
        timer.start(33)
        # timer.start(330)
        self.elapsed_timer.start()
        pg.exec()

        # if self.music is not None:
        #     self.music.stop()

    #     self.streaming_task = asyncio.create_task(self.loop())

    # async def async_range(self, count):
    #     # dt = 1.0 / config.fps
    #     for i in range(count):
    #         yield (i)
    #         await asyncio.sleep(self.dt * 0.1)

    # async def loop(self):
    #     # dt = 1.0 / config.fps
    #     async for i in self.async_range(1000):
    #         for player in self.players:
    #             player.move(self.dt)
    #         if self.camera_lock.value:
    #             # player center of mass
    #             x, y = np.mean([[p.x, p.y] for p in self.players], axis=0)
    #             self.graphics.camera.position = [x, y, self.graphics.camera.position[2]]
    #             lookat = [x, y, 0]
    #             self.graphics.controller.target = lookat
    #             self.graphics.camera.lookAt(lookat)
    #         for monster_group in self.monsters:
    #             monster_group.move(self.dt, players=self.players)
    #         # time.sleep(dt)

    # def display(self):
    #     return ipw.VBox([self.graphics.renderer, self.toolbar])
