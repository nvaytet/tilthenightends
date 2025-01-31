# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from . import config
from .graphics import make_sprites


bestiary = {
    "bat": {"health": 10.0, "attack": 5.0, "speed": 20.0, "radius": 15.0},
    "rottingghoul": {"health": 20.0, "attack": 10.0, "speed": 18.0, "radius": 15.0},
    "warewolf": {"health": 20.0, "attack": 20.0, "speed": 20.0, "radius": 15.0},
    "giantbat": {"health": 60.0, "attack": 40.0, "speed": 20.0, "radius": 30.0},
    "thereaper": {"health": 150.0, "attack": 50.0, "speed": 15.0, "radius": 50.0},
    "zombie": {"health": 10.0, "attack": 5.0, "speed": 20.0, "radius": 15.0},
    "lizard": {"health": 20.0, "attack": 10.0, "speed": 18.0, "radius": 15.0},
    "sigrarossi": {"health": 20.0, "attack": 20.0, "speed": 20.0, "radius": 15.0},
    "orochimario": {"health": 60.0, "attack": 40.0, "speed": 20.0, "radius": 30.0},
    "mantis": {"health": 150.0, "attack": 50.0, "speed": 15.0, "radius": 50.0},
    "skeleton": {"health": 10.0, "attack": 5.0, "speed": 20.0, "radius": 15.0},
    "mamba": {"health": 20.0, "attack": 10.0, "speed": 18.0, "radius": 15.0},
    "volcano": {"health": 20.0, "attack": 20.0, "speed": 50.0, "radius": 15.0},
    "snake": {"health": 60.0, "attack": 40.0, "speed": 20.0, "radius": 30.0},
    "minotaur": {"health": 150.0, "attack": 50.0, "speed": 15.0, "radius": 50.0},
    "ghost": {"health": 10.0, "attack": 5.0, "speed": 20.0, "radius": 15.0},
    "molisano": {"health": 20.0, "attack": 10.0, "speed": 18.0, "radius": 15.0},
    "swordgardian": {"health": 20.0, "attack": 20.0, "speed": 30.0, "radius": 15.0},
    "thehag": {"health": 60.0, "attack": 40.0, "speed": 20.0, "radius": 30.0},
    "medusa": {"health": 150.0, "attack": 50.0, "speed": 15.0, "radius": 50.0},
    "thedrowner": {"health": 300.0, "attack": 100.0, "speed": 15.0, "radius": 100.0},
}


class Monsters:
    def __init__(self, size, kind, distance, scale=10.0, clumpy=False):
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
        self.clumpy = clumpy
        self.positions = self.make_positions(self.size)
        self.vectors = np.zeros((self.size, 2), dtype="float32")
        self.healths = np.full(self.size, bestiary[kind]["health"])
        self.attacks = np.full(self.size, bestiary[kind]["attack"])
        self.radii = np.full(self.size, bestiary[kind]["radius"])
        self.freezes = np.zeros(self.size)

        # self.positions = np.random.normal(scale=10, size=(n, 3)).astype("float32") * 5.0
        # self.positions[:, 2] = 0.0
        # self.speed = 4.0  # * config.scaling
        self.speed = bestiary[kind]["speed"]
        self.xp = bestiary[kind]["health"]

        self.kind = kind

    def make_sprites(self):
        self.sprites = make_sprites(
            sprite_path=config.resources / "monsters" / f"{self.kind}.png",
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
        if self.clumpy:
            n1 = int(n * 0.04)
            n2 = n // n1
            # Make some seeding positions
            r = config.rng.normal(scale=self.scale, loc=self.distance, size=n1)
            theta = config.rng.uniform(0, 2 * np.pi, n1)
            positions1 = np.zeros((n1, 2), dtype="float32")
            positions1[:, 0] = r * np.cos(theta)
            positions1[:, 1] = r * np.sin(theta)
            offsets = config.rng.normal(
                # scale=config.rng.uniform(
                #     self.scale * 0.05, self.scale * 0.2, n2
                # ).reshape(-1, 1, 1),
                scale=0.05 * self.scale,
                loc=0,
                size=(n2, n1, 2),
            )

            pos = positions1 + offsets
            pos = pos.reshape(-1, 2)
            positions = np.concatenate([pos, positions1[: (n - pos.shape[0])]])
            if offset is not None:
                positions += offset

        else:
            r = config.rng.normal(scale=self.scale, loc=self.distance, size=n)
            theta = config.rng.uniform(0, 2 * np.pi, n)
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

    def move(self, t, dt, players):
        # Target the player with the least health
        alive_players = [p for p in players if p.alive]
        if alive_players:
            p = min(alive_players, key=lambda p: p.health)
            target = np.array([p.x, p.y])
            v = target - self.positions
            # Normalize vectors
            self.vectors[...] = v / np.linalg.norm(v, axis=1).reshape(-1, 1)
        # Update positions
        self.positions += (
            self.vectors * dt * self.speed * (self.freezes <= t).reshape(-1, 1)
        )
        self.sprites.setData(pos=self.positions)

    def as_dict(self):
        return {
            "kind": self.kind,
            "size": self.size,
            "positions": self.positions,
            "healths": self.healths,
            "attacks": self.attacks,
            "radii": self.radii,
            "freezes": self.freezes,
            "speed": self.speed,
            "xp": self.xp,
        }
