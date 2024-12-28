import numpy as np

from . import config
from .graphics import make_sprites

# MAX_PROJECTILES = 100


class Projectile:
    def __init__(self, position, vector, speed, tstart, health, attack):
        self.position = position
        self.vector = vector / np.linalg.norm(vector)
        self.speed = speed
        self.tstart = tstart
        # self.tend = tend
        self.health = health
        self.attack = attack
        # self.radius = radius

    def move(self, dt):
        self.position += self.vector * dt * self.speed


class Weapon:
    def __init__(self, name, cooldown, damage, speed, health, max_projectiles):
        self.name = name
        self.cooldown = cooldown
        self.damage = damage
        self.speed = speed
        # self.radius = radius
        # self.longevity = longevity
        self.health = health
        self.nprojectiles = 1
        self.max_projectiles = max_projectiles
        self.projectiles = []
        # self.vectors = np.zeros((MAX_PROJECTILES, 2))
        # self.positions = np.full((MAX_PROJECTILES, 2), np.nan)
        self.timer = 0
        self.sprites = make_sprites(
            sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
            positions=np.array([[0, 0]]),
        )
        self.levels = {
            "speed": 0,
            "health": 0,
            "damage": 0,
            "cooldown": 0,
            "nprojectiles": 0,
        }

    def fire(self, position, t):
        print("t, self.timer", t, self.timer)
        self.projectiles.extend(
            [
                Projectile(
                    position=position,
                    vector=np.random.uniform(-1, 1, 2),
                    speed=self.speed,
                    tstart=t,
                    # tend=t + self.longevity,
                    attack=self.damage,
                    health=self.health,
                    # radius=self.radius,
                )
                for _ in range(self.nprojectiles)
            ]
        )
        # self.positions[: self.nprojectiles, 0] = x
        # self.positions[: self.nprojectiles, 1] = y
        # self.tstart = t
        # self.tend = t + self.longevity
        # self.sprites.setData(pos=self.positions)
        self.draw_sprites()
        self.timer = t + self.cooldown

    def draw_sprites(self):
        pos = [p.position for p in self.projectiles]
        # print(pos.shape)
        # print("len(pos)", len(pos), np.array(pos).shape, self.projectiles[0].position)
        if pos:
            self.sprites.setData(pos=np.array(pos))

    def update(self, dt):
        # self.positions += self.vectors * dt * self.speed
        for p in self.projectiles:
            p.move(dt)
        # self.sprites.setData(pos=self.positions)
        self.draw_sprites()
        # self.timer -= dt


class Runetracer(Weapon):
    def __init__(self):
        super().__init__(
            name="Runetracer",
            cooldown=5,
            damage=10,
            speed=10 * config.scaling,
            # longevity=5,
            health=30,
            # radius=20,
            max_projectiles=5,
        )

    def fire(self, position, t):
        super().fire(position, t)
        self.vectors = np.random.uniform(-1, 1, (self.nprojectiles, 2))
        self.vectors /= np.linalg.norm(self.vectors, axis=1)  # [:, None]


arsenal = {
    "runetracer": Runetracer,
}
