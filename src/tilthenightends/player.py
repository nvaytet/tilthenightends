# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass
from functools import partial
from typing import Any
import numpy as np

from . import config
from .graphics import make_sprites
from .tools import Vector, Towards, LevelupOptions
from .weapons import arsenal, WeaponInfo


@dataclass(frozen=True)
class PlayerInfo:
    x: float
    y: float
    speed: float
    vector: np.ndarray
    max_health: float
    health: float
    weapon: WeaponInfo
    levels: dict
    alive: bool
    respawn_time: float


class Player:
    def __init__(
        self,
        weapon: str,
        health: float,
        speed: float,
        hero: str,
        x: float = 0.0,
        y: float = 0.0,
    ):
        self.hero = hero
        self.x = x
        self.y = y
        self.speed = speed
        self.vector = np.array([0.0, 0.0])
        self.max_health = health
        self.health = health
        self.freeze = 0.0
        self.weapon = arsenal[weapon.lower()](owner=self)
        self.attack = 0.0
        self.radius = 20.0
        self._closest_monster = None
        self.respawn_time = np.inf

        self.levels = {
            "health": 0,
            "speed": 0,
            "weapon_speed": 0,
            "weapon_health": 0,
            "weapon_damage": 0,
            "weapon_cooldown": 0,
            "weapon_size": 0,
            "weapon_longevity": 0,
        }

    def add_to_graphics(self):
        self.avatar = make_sprites(
            sprite_path=config.resources / "heroes" / f"{self.hero}.png",
            positions=np.array([[self.x, self.y]]),
        )
        self.dead_avatar = make_sprites(
            sprite_path=config.resources / "heroes" / f"{self.hero}_dead.png",
            positions=np.array([[self.x, self.y]]),
        )
        self.dead_avatar.setOpacity(0.0)

    def execute_bot_instructions(self, direction: Vector | Towards | None):
        if direction is None:
            return
        if isinstance(direction, Vector):
            self.vector = np.array([direction.x, direction.y])
        elif isinstance(direction, Towards):
            self.vector = np.array([direction.x - self.x, direction.y - self.y])

    def maybe_respawn(self, t):
        if t > self.respawn_time:
            print(f"Player {self.hero} respawning.", t, self.respawn_time)
            self.health = self.max_health / 3
            self.respawn_time = np.inf
            self.dead_avatar.setOpacity(0.0)
            self.avatar.setOpacity(1.0)
            self.weapon.timer = t + self.weapon.cooldown

    @property
    def alive(self) -> bool:
        return self.health > 0

    def move(self, dt: float):
        self.x += self.speed * dt * self.vector[0]
        self.y += self.speed * dt * self.vector[1]
        self.avatar.setData(pos=np.array([[self.x, self.y]]))

    @property
    def position(self) -> np.ndarray:
        return np.array([self.x, self.y])

    @property
    def vector(self) -> np.ndarray:
        return self._vector

    @vector.setter
    def vector(self, value: np.ndarray):
        self._vector = np.asarray(value)
        norm = np.linalg.norm(value)
        if norm > 0.0:
            self._vector = self._vector / norm

    def die(self, t):
        # Start countdown to respawn
        self.respawn_time = t + config.respawn_time
        self.dead_avatar.setOpacity(1.0)
        self.dead_avatar.setData(pos=np.array([[self.x, self.y]]))
        self.avatar.setOpacity(0.0)
        print(f"Player {self.hero} DIED.", t, self.respawn_time)
        self.weapon.projectiles = []
        self.weapon.draw_sprites()

    def as_dict(self):
        return {
            "hero": self.hero,
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "vector": self.vector.tolist(),
            "health": self.health,
            "weapon": self.weapon.as_dict(),
            "levels": self.levels.copy(),
            "alive": bool(self.alive),
            "respawn_time": self.respawn_time,
            "max_health": self.max_health,
        }

    def as_info(self):
        return PlayerInfo(
            x=self.x,
            y=self.y,
            speed=self.speed,
            vector=self.vector,
            health=self.health,
            weapon=self.weapon.as_info(),
            levels=self.levels,
            alive=self.alive,
            respawn_time=self.respawn_time,
            max_health=self.max_health,
        )

    def from_dict(self, data):
        self.hero = data["hero"]
        self.x = data["x"]
        self.y = data["y"]
        self.speed = data["speed"]
        self.vector = np.array(data["vector"])
        self.health = data["health"]
        self.weapon.from_dict(data["weapon"])
        self.levels = data["levels"]
        self.respawn_time = data["respawn_time"]
        self.max_health = data["max_health"]
        self.move(0.0)

    def levelup(self, what):
        if not self.alive:
            print(f"Player {self.hero} is dead and cannot level up.")
            return
        if what == LevelupOptions.player_health:
            self.max_health *= 1.05
            self.levels["health"] += 1
        elif what == LevelupOptions.player_speed:
            self.speed += 1.5
            self.levels["speed"] += 1
        elif what == LevelupOptions.weapon_health:
            self.weapon.health *= 1.05
            self.levels["weapon_health"] += 1
        elif what == LevelupOptions.weapon_speed:
            self.weapon.speed *= 1.02
            self.levels["weapon_speed"] += 1
        elif what == LevelupOptions.weapon_damage:
            self.weapon.damage *= 1.02
            self.levels["weapon_damage"] += 1
        elif what == LevelupOptions.weapon_cooldown:
            self.weapon.cooldown *= 0.95
            self.levels["weapon_cooldown"] += 1
        elif what == LevelupOptions.weapon_size:
            if self.weapon.name == "LightningBolt":
                self.weapon.nprojectiles += 1
            else:
                self.weapon.radius *= 1.05
            self.levels["weapon_size"] += 1
        elif what == LevelupOptions.weapon_longevity:
            self.weapon.longevity *= 1.05
            self.levels["weapon_longevity"] += 1
        elif what is not None:
            raise ValueError(f"Unknown levelup option: {what}")

        # Healing bonus for leveling up
        self.health = self.max_health


heroes = {
    "alaric": partial(
        Player, weapon="fireball", health=100.0, speed=25.0, hero="alaric"
    ),
    "cedric": partial(
        Player, weapon="runetracer", health=100.0, speed=25.0, hero="cedric"
    ),
    "evelyn": partial(
        Player, weapon="magicwand", health=100.0, speed=25.0, hero="evelyn"
    ),
    "garron": partial(Player, weapon="dove", health=100.0, speed=25.0, hero="garron"),
    "isolde": partial(
        Player, weapon="holywater", health=100.0, speed=25.0, hero="isolde"
    ),
    "kaelen": partial(
        Player, weapon="lightningbolt", health=100.0, speed=25.0, hero="kaelen"
    ),
    "lyra": partial(
        Player, weapon="frozenshard", health=100.0, speed=25.0, hero="lyra"
    ),
    "selene": partial(
        Player, weapon="proximitymine", health=100.0, speed=25.0, hero="selene"
    ),
    "seraphina": partial(
        Player, weapon="plasmagun", health=100.0, speed=25.0, hero="seraphina"
    ),
    "theron": partial(Player, weapon="garlic", health=100.0, speed=25.0, hero="theron"),
}


class Team:
    def __init__(self, players: list, strategist: Any):
        self.players = players
        self.strategist = strategist
