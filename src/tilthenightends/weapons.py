import numpy as np

from . import config
from .graphics import make_sprites

MAX_PROJECTILES = 100


class Weapon:
    def __init__(self, name, cooldown, damage, speed, longevity):
        self.name = name
        self.cooldown = cooldown
        self.damage = damage
        self.speed = speed
        self.longevity = longevity
        self.nprojectiles = 1
        self.projectiles = []
        self.vectors = np.zeros((MAX_PROJECTILES, 2))
        self.positions = np.full((MAX_PROJECTILES, 2), np.nan)
        self.timer = 0
        self.sprites = make_sprites(
            sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
            positions=self.positions,
        )

    def fire(self, x, y, t):
        self.positions[: self.nprojectiles, 0] = x
        self.positions[: self.nprojectiles, 1] = y
        self.tstart = t
        self.tend = t + self.longevity
        self.sprites.setData(pos=self.positions)
        self.timer = self.cooldown

    def update(self, dt):
        self.positions += self.vectors * dt * self.speed
        self.sprites.setData(pos=self.positions)
        self.timer -= dt


class Runetracer(Weapon):
    def __init__(self):
        super().__init__(
            name="Runetracer",
            cooldown=5,
            damage=10,
            speed=10 * config.scaling,
            longevity=5,
        )

    def fire(self, x, y, t):
        super().fire(x, y, t)
        self.vectors = np.random.uniform(-1, 1, (self.nprojectiles, 2))
        self.vectors /= np.linalg.norm(self.vectors, axis=1)  # [:, None]


arsenal = {
    "runetracer": Runetracer,
}
