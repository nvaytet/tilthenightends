# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional

import numpy as np

# import pyglet

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

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
        # manual: bool = False,
        # crater_scaling: float = 1.0,
        # player_collisions: bool = True,
        # asteroid_collisions: bool = True,
        # speedup: float = 1.0,
    ):
        if seed is not None:
            np.random.seed(seed)

        self.graphics = Graphics()

        self.players = [Player()]

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
            Monsters(n=2000, kind="bat", distance=400.0, scale=100),
            Monsters(n=2000, kind="rottingghoul", distance=600, scale=100),
            Monsters(n=500, kind="giantbat", distance=800, scale=100),
            Monsters(n=500, kind="thereaper", distance=1000, scale=100),
        ]
        for horde in self.monsters:
            self.graphics.add(horde.sprites)

        for player in self.players:
            self.graphics.add(player.avatar)

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
        # Compute distances between players and monsters. If any monster is within 5
        # pixels of a hero, the monster is destroyed.
        for player in self.players:
            for horde in self.monsters:
                distances = np.linalg.norm(player.position - horde.positions, axis=1)
                inds = np.where(distances < config.hit_radius * config.scaling)[0]
                ndead = len(inds)
                if ndead > 0:
                    horde.positions[inds, :] = horde.make_positions(
                        ndead, offset=player.position
                    )

    def update(self):
        for player in self.players:
            player.move(self.dt)
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

        # self.graphics.update()

    def run(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(33)
        pg.exec()

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
