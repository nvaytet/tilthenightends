from dataclasses import dataclass
import numpy as np


# MAX_PROJECTILES = 100


class Projectile:
    def __init__(self, position, vector, speed, tstart, health, attack, radius, owner):
        self.position = position
        self.vector = vector / np.linalg.norm(vector)
        self.speed = speed
        self.tstart = tstart
        # self.tend = tend
        self.health = health
        self.attack = attack
        self.radius = radius
        self.owner = owner

    def move(self, dt):
        self.position += self.vector * dt * self.speed


@dataclass
class Weapon:
    name: str
    cooldown: float
    damage: float
    speed: float
    health: float
    max_projectiles: int
    radius: float
    duration: float
    # owner: Any
    # projectile: Type[Projectile] = Projectile
    nprojectiles: int = 1
    timer: float = 0
    # duration: float = 0
    # _active_slots: np.ndarray = field(init=False)

    def as_dict(self):
        return {
            "name": self.name,
            "cooldown": self.cooldown,
            "damage": self.damage,
            "speed": self.speed,
            "health": self.health,
            "max_projectiles": self.max_projectiles,
            "nprojectiles": self.nprojectiles,
            # "levels": self.levels.copy(),
        }


# class Weapon:
#     def __init__(
#         self,
#         name,
#         cooldown,
#         damage,
#         speed,
#         health,
#         max_projectiles,
#         radius,
#         owner,
#         projectile=Projectile,
#         nprojectiles=1,
#     ):
#         self.name = name
#         self.cooldown = cooldown
#         self.damage = damage
#         self.speed = speed
#         # self.radius = radius
#         # self.longevity = longevity
#         self.health = health
#         self.projectile_counter = 0
#         self.nprojectiles = nprojectiles
#         self.max_projectiles = max_projectiles
#         # self.projectiles = []
#         # self._vectors = np.zeros((MAX_PROJECTILES, 2))
#         # self._positions = np.full((MAX_PROJECTILES, 2), np.nan)
#         # self._healths = np.full(MAX_PROJECTILES, self.max_health)
#         # self._radii = np.full(MAX_PROJECTILES, radius)
#         self.timer = 0
#         self.radius = radius
#         self.owner = owner
#         self.projectile = projectile
#         self._active_slots = np.zeros(config.max_projectiles, dtype=bool)

#         # self.hea

#     # @property
#     # def positions(self):
#     #     return self._positions[self._active_slots, :]

#     # @property
#     # def vectors(self):
#     #     return self._vectors[self._active_slots, :]

#     # @property
#     # def healths(self):
#     #     return self._healths[self._active_slots]

#     # @healths.setter
#     # def healths(self, value):
#     #     self._healths[self._active_slots] = value

#     # @property
#     # def attacks(self):
#     #     return np.full(self.projectile_counter, self.damage)

#     # @property
#     # def radii(self):
#     #     return np.full(self.projectile_counter, self.radius)

#     # def add_to_graphics(self):
#     #     self.sprites = make_sprites(
#     #         sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
#     #         positions=self.positions,
#     #         width=self.radius * 2,
#     #         height=self.radius * 2,
#     #     )
#     # self.levels = {
#     #     "speed": 0,
#     #     "health": 0,
#     #     "damage": 0,
#     #     "cooldown": 0,
#     #     "nprojectiles": 0,
#     # }

#     def fire(self, position, t):
#         print("t, self.timer", t, self.timer)
#         # self.projectiles.extend(
#         # self.projectiles = [
#         #     self.projectile(
#         #         position=position,
#         #         vector=np.random.uniform(-1, 1, 2),
#         #         speed=self.speed,
#         #         tstart=t,
#         #         # tend=t + self.longevity,
#         #         attack=self.damage,
#         #         health=self.health,
#         #         radius=self.radius,
#         #         owner=self.owner,
#         #     )
#         #     for _ in range(self.nprojectiles)
#         # ]

#         # Find an empty slot in the arrays
#         ind = np.where(np.isnan(self.owner.positions[1:, 0]))[0]
#         self._positions[ind, :] = position
#         self._vectors[ind, :] = np.random.uniform(-1, 1, 2)
#         self._healths[ind] = self.max_health
#         self._active_slots[ind] = True
#         self.projectile_counter = np.sum(self._active_slots)

#         # self.positions[: self.nprojectiles, 0] = x
#         # self.positions[: self.nprojectiles, 1] = y
#         # self.tstart = t
#         # self.tend = t + self.longevity
#         # self.sprites.setData(pos=self.positions)
#         self.draw_sprites()
#         self.timer = t + self.cooldown

#     def draw_sprites(self):
#         # pos = [p.position for p in self.projectiles]
#         # # print(pos.shape)
#         # # print("len(pos)", len(pos), np.array(pos).shape, self.projectiles[0].position)
#         # if pos:
#         #     self.sprites.setData(pos=np.array(pos))
#         self.sprites.setData(pos=self._positions)

#     def update(self, dt):
#         # self.positions += self.vectors * dt * self.speed
#         for p in self.projectiles:
#             p.move(dt)
#         # self.sprites.setData(pos=self.positions)
#         self.draw_sprites()
#         # self.timer -= dt

#     def as_dict(self):
#         return {
#             "name": self.name,
#             "cooldown": self.cooldown,
#             "damage": self.damage,
#             "speed": self.speed,
#             "health": self.health,
#             "max_projectiles": self.max_projectiles,
#             "nprojectiles": self.nprojectiles,
#             # "levels": self.levels.copy(),
#         }


class Runetracer(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Runetracer",
            cooldown=5,
            damage=10,
            speed=100.0,  # * config.scaling,
            # longevity=5,
            health=30,
            radius=12,
            max_projectiles=5,
            **kwargs,
        )

    def fire(self, position, t):
        super().fire(position, t)
        self.vectors = np.random.uniform(-1, 1, (self.nprojectiles, 2))
        self.vectors /= np.linalg.norm(self.vectors, axis=1)  # [:, None]


class Fireball(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Fireball",
            cooldown=4,
            damage=15,
            speed=75.0,
            health=40,
            max_projectiles=10,
            radius=16,
            **kwargs,
        )

    def fire(self, position, t):
        super().fire(position, t)
        self.vectors = np.random.uniform(-1, 1, (self.nprojectiles, 2))
        self.vectors /= np.linalg.norm(self.vectors, axis=1)  # [:, None]


class GarlicProjectile(Projectile):
    def move(self, dt):
        # vector must follow owner
        self.position = self.owner.position


class Garlic(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Garlic",
            cooldown=4,
            damage=15,
            speed=0.0,
            health=100,
            max_projectiles=1,
            radius=40,
            projectile=GarlicProjectile,
            **kwargs,
        )


class HolyWater(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HolyWater",
            cooldown=4,
            damage=15,
            speed=0.0,
            health=40,
            max_projectiles=10,
            radius=40,
            **kwargs,
        )

    def fire(self, position, t):
        phi = np.random.uniform(0, 2 * np.pi, self.nprojectiles)
        self.projectiles = [
            self.projectile(
                position=position + np.array([np.cos(p), np.sin(p)]) * self.radius * 2,
                vector=np.array([1.0, 0]),
                speed=self.speed,
                tstart=t,
                # tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
            )
            for p in phi
        ]

        self.draw_sprites()
        self.timer = t + self.cooldown


class Lightning(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Lightning",
            cooldown=4,
            damage=15,
            speed=0.0,
            health=40,
            max_projectiles=10,
            radius=32,
            nprojectiles=5,
            **kwargs,
        )

    def fire(self, position, t):
        # phi = np.random.uniform(0, 2 * np.pi, self.nprojectiles)
        y = np.arange(self.nprojectiles) * self.radius * 2
        x = np.zeros_like(y)
        pos = (position + np.random.uniform(-400, 400, 2)) + np.array([x, y]).T
        self.projectiles = [
            self.projectile(
                position=p,
                vector=np.array([1.0, 0]),
                speed=self.speed,
                tstart=t,
                # tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
            )
            for p in pos
        ]

        self.draw_sprites()
        self.timer = t + self.cooldown


class DoveProjectile(Projectile):
    def move(self, dt):
        # for p in self.projectiles:
        self.phi = (self.phi + self.speed * dt) % (2 * np.pi)
        # print("p.phi", p.phi)
        self.position = (
            self.owner.position
            + np.array([np.cos(self.phi), np.sin(self.phi)]) * self.radius * 2
        )


class Dove(Weapon):
    # Doves circle around the player
    def __init__(self, **kwargs):
        super().__init__(
            name="Dove",
            cooldown=4,
            damage=15,
            speed=2.0,
            health=40,
            max_projectiles=10,
            radius=15,
            projectile=DoveProjectile,
            **kwargs,
        )

    def fire(self, position, t):
        # phi = np.random.uniform(0, 2 * np.pi, self.nprojectiles)
        phi = (
            np.linspace(0, 2 * np.pi, self.nprojectiles)
            + np.random.uniform(0, 2 * np.pi, self.nprojectiles)
        ) % (2 * np.pi)
        self.projectiles = []
        for p in phi:
            proj = self.projectile(
                position=position + np.array([np.cos(p), np.sin(p)]) * self.radius * 2,
                vector=np.array([1.0, 0]),
                speed=self.speed,
                tstart=t,
                # tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
            )
            proj.phi = p
            self.projectiles.append(proj)

        self.draw_sprites()
        self.timer = t + self.cooldown

    # def move(self, dt):
    #     for p in self.projectiles:
    #         p.phi = (p.phi + self.speed * dt) % (2 * np.pi)
    #         print("p.phi", p.phi)
    #         p.position = (
    #             self.owner.position
    #             + np.array([np.cos(p.phi), np.sin(p.phi)]) * p.radius * 2
    #         )


arsenal = {
    "runetracer": Runetracer,
    "fireball": Fireball,
    "garlic": Garlic,
    "holywater": HolyWater,
    "dove": Dove,
    "lightning": Lightning,
}
