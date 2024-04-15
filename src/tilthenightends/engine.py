# SPDX-License-Identifier: BSD-3-Clause

import time
from dataclasses import dataclass
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as ipw

# import pyglet

from PIL import Image

# from pyglet.window import key


from . import config

# from .asteroid import Asteroid
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
        self.graphics = Graphics()

        # self.key_state_handler = key.KeyStateHandler()
        # self.graphics.window.push_handlers(self.key_state_handler)

        # zombie_image = Image.open(config.resources / "bat.png").convert("RGBA")

        self.monsters = Monsters(n=2000, kind="bat")
        self.graphics.add(self.monsters.sprites)
        self.button = ipw.Button(description="Start!")
        self.button.on_click(self.run)

    def run(self, owner):
        import time

        dt = 1.0 / config.fps

        for i in range(1000):
            for player in self.players:
                player.move(dt)
            self.monsters.move(dt, players=self.players)
            time.sleep(dt)

    def display(self):
        return ipw.VBox([self.graphics.renderer, self.button])
