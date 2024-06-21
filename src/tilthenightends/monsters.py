# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from . import config
from .graphics import make_sprites


bestiary = {
    "bat": {"health": 10.0, "attack": 5.0, "speed": 4.0},
    "rottingghoul": {"health": 20.0, "attack": 10.0, "speed": 3.5},
    "giantbat": {"health": 60.0, "attack": 40.0, "speed": 4.0},
    "thereaper": {"health": 150.0, "attack": 50.0, "speed": 3.0},
}


class Monsters:
    def __init__(self, size, kind, distance, scale=10.0):
        # Create positions in a ring that has a gaussian profile in radius which peaks
        # at distance
        # r = np.random.normal(
        #     scale=scale * config.scaling, loc=distance * config.scaling, size=n
        # )
        # theta = np.random.uniform(0, 2 * np.pi, n)
        # self.positions = np.zeros((n, 2), dtype="float32")
        # self.positions[:, 0] = r * np.cos(theta)
        # self.positions[:, 1] = r * np.sin(theta)

        self.size = size
        self.distance = distance
        self.scale = scale
        self.positions = self.make_positions(self.size)
        self.healths = np.full(self.size, bestiary[kind]["health"])
        self.attacks = np.full(self.size, bestiary[kind]["attack"])

        # self.positions = np.random.normal(scale=10, size=(n, 3)).astype("float32") * 5.0
        # self.positions[:, 2] = 0.0
        self.speed = 4.0 * config.scaling
        self.kind = kind

        self.sprites = make_sprites(
            sprite_path=config.resources / "monsters" / f"{kind}.png",
            positions=self.positions,
        )

        # # Create a position buffer geometry
        # self.geometry = p3.BufferGeometry(
        #     attributes={"position": p3.BufferAttribute(array=self.positions)}
        # )
        # # Create a points material
        # im = Image.open(config.resources / "monsters" / f"{kind}.png").convert("RGBA")
        # a = np.flipud(np.array(im).astype("float32")) / 255
        # self.texture = p3.DataTexture(data=a, format="RGBAFormat", type="FloatType")
        # self.material = p3.PointsMaterial(
        #     size=(im.width * 2) // 64, map=self.texture, transparent=True
        # )
        # # Combine the geometry and material into a Points object
        # self.sprites = p3.Points(geometry=self.geometry, material=self.material)

    def make_positions(self, n, offset=None):
        r = np.random.normal(
            scale=self.scale * config.scaling,
            loc=self.distance * config.scaling,
            size=n,
        )
        theta = np.random.uniform(0, 2 * np.pi, n)
        positions = np.zeros((n, 2), dtype="float32")
        positions[:, 0] = r * np.cos(theta)
        positions[:, 1] = r * np.sin(theta)
        if offset is not None:
            positions += offset
        return positions

    @property
    def x(self):
        return self.positions[:, 0]

    @property
    def y(self):
        return self.positions[:, 1]

    def move(self, dt, players):
        # Compute vectors from current position to target position
        p = players[0]
        target = np.array([p.x, p.y])
        v = target - self.positions
        # Normalize vectors
        v = v / np.linalg.norm(v, axis=1).reshape(-1, 1)
        # Update positions
        self.positions += v * dt * self.speed
        # self.geometry.attributes["position"].array = self.positions.astype("float32")
        self.sprites.setData(pos=self.positions)
