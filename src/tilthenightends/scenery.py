# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from . import config
from .graphics import make_sprites


def make_scenery():
    # self.size = size
    # self.distance = distance
    # self.scale = scale
    # self.positions = self.make_positions(self.size)
    # self.healths = np.full(self.size, bestiary[kind]["health"])
    # self.attacks = np.full(self.size, bestiary[kind]["attack"])

    # # self.positions = np.random.normal(scale=10, size=(n, 3)).astype("float32") * 5.0
    # # self.positions[:, 2] = 0.0
    # # self.speed = 4.0  # * config.scaling
    # self.speed = bestiary[kind]["speed"]
    # self.xp = bestiary[kind]["health"]

    # self.kind = kind

    sprites = []

    for i in range(4):
        sprites.append(
            make_sprites(
                sprite_path=config.resources / "levels" / "forest" / f"forest{i}.png",
                positions=np.random.uniform(-20000, 20000, 2),
            )
        )

    return sprites
