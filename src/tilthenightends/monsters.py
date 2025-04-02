# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass
import numpy as np

from . import config
from .graphics import make_sprites


bestiary = {
    "bat": {"health": 10.0, "attack": 5.0, "radius": 15.0},
    "rottingghoul": {"health": 20.0, "attack": 10.0, "radius": 15.0},
    "warewolf": {"health": 20.0, "attack": 20.0, "radius": 15.0},
    "giantbat": {"health": 60.0, "attack": 40.0, "radius": 30.0},
    "thereaper": {"health": 150.0, "attack": 50.0, "radius": 50.0},
    "zombie": {"health": 10.0, "attack": 5.0, "radius": 15.0},
    "lizard": {"health": 20.0, "attack": 10.0, "radius": 15.0},
    "sigrarossi": {"health": 20.0, "attack": 20.0, "radius": 15.0},
    "orochimario": {"health": 60.0, "attack": 40.0, "radius": 30.0},
    "mantis": {"health": 150.0, "attack": 50.0, "radius": 50.0},
    "skeleton": {"health": 10.0, "attack": 5.0, "radius": 15.0},
    "mamba": {"health": 20.0, "attack": 10.0, "radius": 15.0},
    "volcano": {"health": 20.0, "attack": 20.0, "radius": 15.0},
    "snake": {"health": 60.0, "attack": 40.0, "radius": 30.0},
    "minotaur": {"health": 150.0, "attack": 50.0, "radius": 50.0},
    "ghost": {"health": 10.0, "attack": 5.0, "radius": 15.0},
    "molisano": {"health": 20.0, "attack": 10.0, "radius": 15.0},
    "swordgardian": {"health": 20.0, "attack": 20.0, "radius": 15.0},
    "thehag": {"health": 60.0, "attack": 40.0, "radius": 30.0},
    "medusa": {"health": 150.0, "attack": 50.0, "radius": 50.0},
    "thedrowner": {"health": 300.0, "attack": 100.0, "radius": 100.0},
}


class Monsters:
    def __init__(self, size, kind, distance, scale=10.0, clumpy=False):
        self.size = size
        self.distance = distance
        self._starting_distance = distance
        self._distance_gradient = (100.0 - self._starting_distance) / (
            config.time_limit
        )
        self.scale = scale
        self._starting_scale = scale
        self._scale_gradient = (
            0.01 * self._starting_scale - self._starting_scale
        ) / config.time_limit
        self.positions = self.make_positions(self.size, clumpy=clumpy)
        self.vectors = np.zeros((self.size, 2), dtype="float32")
        self.healths = np.full(self.size, bestiary[kind]["health"])
        self.attacks = np.full(self.size, bestiary[kind]["attack"])
        self.radii = np.full(self.size, bestiary[kind]["radius"])
        self.freezes = np.zeros(self.size)
        self.speed = max(20.0, distance / config.time_limit)
        self.xp = bestiary[kind]["health"]

        self.kind = kind

    def make_sprites(self):
        self.sprites = make_sprites(
            sprite_path=config.resources / "monsters" / f"{self.kind}.png",
            positions=self.positions,
        )

    def make_positions(
        self, n, clumpy: bool = False, offset: np.ndarray | None = None, t: float = 0.0
    ) -> np.ndarray:
        self.distance = self._starting_distance + self._distance_gradient * t
        self.scale = self._starting_scale + self._scale_gradient * t
        if clumpy:
            n1 = int(n * 0.04)
            n2 = n // n1
            # Make some seeding positions
            r = np.abs(config.rng.normal(scale=self.scale, loc=self.distance, size=n1))
            theta = config.rng.uniform(0, 2 * np.pi, n1)
            positions1 = np.zeros((n1, 2), dtype="float32")
            positions1[:, 0] = r * np.cos(theta)
            positions1[:, 1] = r * np.sin(theta)
            offsets = config.rng.normal(
                scale=0.05 * self.scale, loc=0, size=(n2, n1, 2)
            )

            pos = positions1 + offsets
            pos = pos.reshape(-1, 2)
            positions = np.concatenate([pos, positions1[: (n - pos.shape[0])]])
        else:
            r = np.abs(config.rng.normal(scale=self.scale, loc=self.distance, size=n))
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
            "positions": self.positions.tolist(),
            "healths": self.healths.tolist(),
            "attacks": self.attacks.tolist(),
            "radii": self.radii.tolist(),
            "freezes": self.freezes.tolist(),
            "speed": self.speed,
            "xp": self.xp,
        }

    def from_dict(self, data):
        self.kind = data["kind"]
        self.size = data["size"]
        self.positions = np.array(data["positions"])
        self.healths = np.array(data["healths"])
        self.attacks = np.array(data["attacks"])
        self.radii = np.array(data["radii"])
        self.freezes = np.array(data["freezes"])
        self.speed = data["speed"]
        self.xp = data["xp"]
        self.move(0, 0, [])


@dataclass(frozen=True)
class MonsterInfo:
    x: np.ndarray
    y: np.ndarray
    healths: np.ndarray
    attacks: np.ndarray
    radii: np.ndarray
    speeds: np.ndarray
