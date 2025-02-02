# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass

import numpy as np

from . import config
from .graphics import make_sprites


class Loot:
    def __init__(self, size, kind):
        self.kind = kind
        self.positions = config.rng.uniform(
            -config.map_size, config.map_size, (size, 2)
        )

        r = np.linalg.norm(self.positions, axis=1)
        self.xp = r * 0.05

        self.dx = 32
        self.trash = config.map_size * 2

        self.locations = {
            (
                (self.positions[i, 0] + config.map_size) // self.dx,
                (self.positions[i, 1] + config.map_size) // self.dx,
            ): i
            for i in range(size)
        }

        self.sprites = make_sprites(
            sprite_path=config.resources / "other" / f"{kind}.png",
            positions=self.positions,
        )

    def maybe_pickup(self, player_position):
        x, y = player_position
        x = (x + config.map_size) // self.dx
        y = (y + config.map_size) // self.dx
        ind = self.locations.get((x, y))
        if ind is not None:
            # print("picking up", self.kind, x, y)
            self.positions[ind, :] = [self.trash, self.trash]
            self.sprites.setData(pos=self.positions)
            del self.locations[(x, y)]
            return self.xp[ind]
        return False


@dataclass(frozen=True)
class LootInfo:
    kind: str
    x: np.ndarray
    y: np.ndarray
    xp: np.ndarray | None = None
