# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass

import numpy as np

from . import config
from .graphics import make_sprites


@dataclass(frozen=True)
class WeaponInfo:
    name: str
    cooldown: float
    damage: float
    speed: float
    health: float
    size: float


@dataclass(frozen=True)
class ProjectileInfo:
    position: np.ndarray
    vector: np.ndarray
    speed: float
    tstart: float
    tend: float
    health: float
    attack: float
    radius: float
    owner: str
    healing: float = 0.0
    freeze: float = 0.0


class Projectile:
    def __init__(
        self,
        position,
        vector,
        speed,
        tstart,
        tend,
        health,
        attack,
        radius,
        owner,
        healing=0.0,
        freeze=0.0,
    ):
        self.position = position.copy()
        self.vector = vector / np.linalg.norm(vector)
        self.speed = speed
        self.tstart = tstart
        self.tend = tend
        self.health = health
        self.attack = attack
        self.radius = radius
        self.owner = owner
        self.healing = healing
        self.freeze = freeze

    def move(self, t, dt):
        self.position = self.position + (self.vector * dt * self.speed)

    def as_dict(self):
        return {
            "position": self.position,
            "vector": self.vector,
            "speed": self.speed,
            "tstart": self.tstart,
            "tend": self.tend,
            "health": self.health,
            "attack": self.attack,
            "radius": self.radius,
            "owner": self.owner,
            "healing": self.healing,
            "freeze": self.freeze,
        }

    def as_info(self):
        return ProjectileInfo(
            position=self.position,
            vector=self.vector,
            speed=self.speed,
            tstart=self.tstart,
            tend=self.tend,
            health=self.health,
            attack=self.attack,
            radius=self.radius,
            owner=self.owner.name,
            healing=self.healing,
            freeze=self.freeze,
        )


class Weapon:
    def __init__(
        self,
        name,
        cooldown,
        damage,
        speed,
        health,
        radius,
        owner,
        longevity,
        projectile=Projectile,
    ):
        self.name = name
        self.cooldown = cooldown
        self.damage = damage
        self.speed = speed
        self.longevity = longevity
        self.health = health
        self.projectiles = []
        self.timer = 0
        self.radius = radius
        self.owner = owner
        self.projectile = projectile

    def add_to_graphics(self):
        self.sprites = make_sprites(
            sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
            positions=np.array([[0, 0]]),
            width=self.radius * 2,
            height=self.radius * 2,
        )

    def fire(self, position, t):
        self.projectiles.append(
            self.projectile(
                position=position,
                vector=config.rng.uniform(-1, 1, 2),
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
            )
        )
        self.draw_sprites()
        self.timer = t + self.cooldown

    def draw_sprites(self):
        pos = [p.position for p in self.projectiles]
        if pos:
            self.sprites.setOpacity(1.0)
            self.sprites.setData(pos=np.array(pos))
        else:
            self.sprites.setOpacity(0.0)

    def update(self, t, dt):
        self.projectiles = [p for p in self.projectiles if t < p.tend]
        for p in self.projectiles:
            p.move(t, dt)
        self.draw_sprites()

    def as_dict(self):
        return {
            "name": self.name,
            "cooldown": self.cooldown,
            "damage": self.damage,
            "speed": self.speed,
            "health": self.health,
            "size": self.radius,
        }

    def as_info(self):
        return WeaponInfo(
            name=self.name,
            cooldown=self.cooldown,
            damage=self.damage,
            speed=self.speed,
            health=self.health,
            size=self.radius,
        )

    @property
    def size(self):
        return


class RunetracerProjectile(Projectile):
    def __init__(self, *args, tstart, **kwargs):
        super().__init__(*args, tstart=tstart, **kwargs)
        self.period = 2.0
        self.next_move = tstart + self.period

    def move(self, t, dt):
        super().move(t, dt)
        if t > self.next_move:
            self.vector = config.rng.uniform(-1, 1, 2)
            self.vector /= np.linalg.norm(self.vector)
            self.next_move += self.period


class Runetracer(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Runetracer",
            cooldown=5,
            damage=12,
            speed=100.0,
            longevity=10,
            health=30,
            radius=12,
            projectile=RunetracerProjectile,
            **kwargs,
        )


class Fireball(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Fireball",
            cooldown=5,
            damage=15,
            speed=75.0,
            health=10,
            longevity=6,
            radius=16,
            **kwargs,
        )


class GarlicProjectile(Projectile):
    def move(self, t, dt):
        self.position = self.owner.position


class Garlic(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Garlic",
            cooldown=4,
            damage=8,
            speed=0.0,
            health=20,
            longevity=6,
            radius=40,
            projectile=GarlicProjectile,
            **kwargs,
        )

    def fire(self, *args, **kwargs):
        super().fire(*args, **kwargs)
        self.timer += self.longevity


class HolyWater(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HolyWater",
            cooldown=4,
            damage=5,
            speed=0.0,
            health=50,
            longevity=8,
            radius=40,
            **kwargs,
        )

    def fire(self, position, t):
        phi = config.rng.uniform(0, 2 * np.pi)
        self.projectiles.append(
            self.projectile(
                position=position
                + np.array([np.cos(phi), np.sin(phi)]) * self.radius * 2,
                vector=np.array([1.0, 0]),
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
                healing=self.damage,
            )
        )

        self.draw_sprites()
        self.timer = t + self.cooldown


class LightningBolt(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="LightningBolt",
            cooldown=4,
            damage=15,
            speed=0.0,
            health=1,
            radius=32,
            longevity=0.2,
            **kwargs,
        )
        self.nprojectiles = 1

    def fire(self, position, t):
        y = np.arange(self.nprojectiles) * self.radius * 2
        x = np.zeros_like(y)
        pos = (position + config.rng.uniform(-400, 400, 2)) + np.array([x, y]).T
        self.projectiles = [
            self.projectile(
                position=p,
                vector=np.array([1.0, 0]),
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
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
    def move(self, t, dt):
        self.phi = (self.phi + self.speed * dt) % (2 * np.pi)
        self.position = (
            self.owner.position
            + np.array([np.cos(self.phi), np.sin(self.phi)]) * self.radius * 2.5
        )


class Dove(Weapon):
    # Doves circle around the player
    def __init__(self, **kwargs):
        super().__init__(
            name="Dove",
            cooldown=4,
            damage=12,
            speed=2.0,
            health=10,
            radius=15,
            longevity=5,
            projectile=DoveProjectile,
            **kwargs,
        )

    def fire(self, position, t):
        phi = config.rng.uniform(0, 2 * np.pi)
        proj = self.projectile(
            position=position
            + np.array([np.cos(phi), np.sin(phi)]) * self.radius * 2.5,
            vector=np.array([1.0, 0]),
            speed=self.speed,
            tstart=t,
            tend=t + self.longevity,
            attack=self.damage,
            health=self.health,
            radius=self.radius,
            owner=self.owner,
        )
        proj.phi = phi
        self.projectiles.append(proj)

        self.draw_sprites()
        self.timer = t + self.cooldown


class PlasmaGun(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="PlasmaGun",
            cooldown=5,
            damage=10,
            speed=100.0,
            health=1,
            longevity=5,
            radius=8,
            **kwargs,
        )

    def fire(self, position, t):
        phi = config.rng.uniform(0, 2 * np.pi)
        # 5 projectiles in a star shaped pattern
        for i in range(5):
            pp = (phi + i * 2 * np.pi / 5) % (2 * np.pi)
            vx = np.cos(pp)
            vy = np.sin(pp)
            self.projectiles.append(
                self.projectile(
                    position=position,
                    vector=np.array([vx, vy]),
                    speed=self.speed,
                    tstart=t,
                    tend=t + self.longevity,
                    attack=self.damage,
                    health=self.health,
                    radius=self.radius,
                    owner=self.owner,
                )
            )

        self.draw_sprites()
        self.timer = t + self.cooldown


class MagicWand(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="MagicWand",
            cooldown=5,
            damage=15,
            speed=50.0,
            health=10,
            longevity=5,
            radius=16,
            **kwargs,
        )

    def fire(self, position, t):
        target = self.owner._closest_monster
        if target is None:
            return
        self.projectiles.append(
            self.projectile(
                position=position,
                vector=target - position,
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
                healing=self.damage,
            )
        )

        self.draw_sprites()
        self.timer = t + self.cooldown


class FrozenShard(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="FrozenShard",
            cooldown=4,
            damage=0,
            speed=400.0,
            health=np.inf,
            longevity=5,
            radius=16,
            **kwargs,
        )

    def fire(self, position, t):
        phi = config.rng.uniform(0, 2 * np.pi)
        print("frozen shard phi", phi, t)
        self.projectiles.append(
            self.projectile(
                position=position,
                vector=np.array([np.cos(phi), np.sin(phi)]),
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
                freeze=self.longevity,
            )
        )

        self.draw_sprites()
        self.timer = t + self.cooldown


class ProximityMine(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="ProximityMine",
            cooldown=5,
            damage=100,
            speed=0.0,
            health=1,
            longevity=6.0,
            radius=16,
            **kwargs,
        )

    def fire(self, position, t):
        self.projectiles.append(
            self.projectile(
                position=position,
                vector=np.array([1, 0]),
                speed=self.speed,
                tstart=t,
                tend=t + self.longevity,
                attack=self.damage,
                health=self.health,
                radius=self.radius,
                owner=self.owner,
            )
        )

        self.draw_sprites()
        self.timer = t + self.cooldown


arsenal = {
    "runetracer": Runetracer,
    "fireball": Fireball,
    "garlic": Garlic,
    "holywater": HolyWater,
    "dove": Dove,
    "lightningbolt": LightningBolt,
    "plasmagun": PlasmaGun,
    "magicwand": MagicWand,
    "frozenshard": FrozenShard,
    "proximitymine": ProximityMine,
}
