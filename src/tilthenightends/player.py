# SPDX-License-Identifier: BSD-3-Clause


# import pythreejs as p3

# # import pyglet
# from matplotlib.colors import hex2color

# from .tools import Instructions, image_to_sprite, recenter_image, text_to_raw_image

from functools import partial
from typing import Any
import numpy as np

from . import config
from .graphics import make_sprites
from .tools import Vector, Towards, LevelupOptions
from .weapons import arsenal

MAX_PROJECTILES = 100


class Player:
    def __init__(
        self,
        # vector: np.ndarray,
        weapon: str,
        health: float,
        speed: float,
        hero: str,
        x: float = 0.0,
        y: float = 0.0,
        # number: int,
        # name: str,
        # color: str,
        # avatar: Union[int, str],
        # position: float,
        # back_batch: pyglet.graphics.Batch,
        # main_batch: pyglet.graphics.Batch,
    ):
        self.hero = hero
        # self.x = x
        # self.y = y
        self.speed = speed  # 5.0  # * config.scaling
        self.vector = np.array([0.0, 0.0])  # vector / np.linalg.norm(vector)
        self.max_health = health
        self.health = health  # 100.0
        # self.defense = 0.0
        self.weapon = arsenal[weapon.lower()](owner=self)
        self.attack = 0.0
        self.radius = 20.0

        self._positions = np.full((MAX_PROJECTILES + 1, 2), np.nan)
        self._vectors = np.full((MAX_PROJECTILES + 1, 2), np.nan)
        self._healths = np.zeros(MAX_PROJECTILES + 1)
        self._attacks = np.zeros(MAX_PROJECTILES + 1)

        self._positions[0, :] = np.array([x, y])

        self.levels = {
            # "attack": 0,
            "health": 0,
            "speed": 0,
            "weapon_speed": 0,
            "weapon_health": 0,
            "weapon_damage": 0,
            "weapon_cooldown": 0,
            "weapon_nprojectiles": 0,
        }

    def add_to_graphics(self):
        self.avatar = make_sprites(
            sprite_path=config.resources / "heroes" / f"{self.hero}.png",
            positions=self._positions[0, :],
        )
        self.weapon_sprites = make_sprites(
            sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
            positions=self._positions[1:, :],
            width=self.weapon.radius * 2,
            height=self.weapon.radius * 2,
        )

    def execute_bot_instructions(self, direction: Vector | Towards | None):
        if direction is None:
            return
        if isinstance(direction, Vector):
            self.vector = np.array([direction.x, direction.y])
        elif isinstance(direction, Towards):
            self.vector = np.array([direction.x - self.x, direction.y - self.y])

        # self.vector = np.array(
        #     [int(move.right) - int(move.left), int(move.up) - int(move.down)]
        # )

    @property
    def alive(self) -> bool:
        return self.health > 0

    def move(self, dt: float):
        self.x += self.speed * dt * self.vector[0]
        self.y += self.speed * dt * self.vector[1]
        # self.geometry.attributes["position"].array = np.array(
        #     [[self.x, self.y, 0.0], [self.x - 1.0, self.y - 1.0, 0.0]]
        # ).astype("float32")
        # self.avatar.position = [self.x, self.y, 0.0]
        # print(f"Player moved to {self.x}, {self.y}.")
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
        return

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
        }

    def levelup(self, what):
        if what == LevelupOptions.player_health:
            self.max_health *= 1.05
            self.levels["health"] += 1
        elif what == LevelupOptions.player_speed:
            self.speed += 1.0
            self.levels["speed"] += 1
        elif what == LevelupOptions.weapon_health:
            self.weapon.health *= 1.05
            self.levels["weapon_health"] += 1
        elif what == LevelupOptions.weapon_speed:
            self.weapon.speed += 1.0
            self.levels["weapon_speed"] += 1
        elif what == LevelupOptions.weapon_damage:
            self.weapon.damage *= 1.02
            self.levels["weapon_damage"] += 1
        elif what == LevelupOptions.weapon_cooldown:
            self.weapon.cooldown *= 0.9
            self.levels["weapon_cooldown"] += 1
        elif what == LevelupOptions.weapon_nprojectiles:
            if self.weapon.nprojectiles < self.weapon.max_projectiles:
                self.weapon.nprojectiles += 1
                self.levels["weapon_nprojectiles"] += 1

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
        Player, weapon="runetracer", health=100.0, speed=25.0, hero="evelyn"
    ),
    "garron": partial(Player, weapon="dove", health=100.0, speed=25.0, hero="garron"),
    "isolde": partial(
        Player, weapon="holywater", health=100.0, speed=25.0, hero="isolde"
    ),
    "kaelen": partial(
        Player, weapon="lightning", health=100.0, speed=25.0, hero="kaelen"
    ),
    "lyra": partial(Player, weapon="runetracer", health=100.0, speed=25.0, hero="lyra"),
    "selene": partial(
        Player, weapon="runetracer", health=100.0, speed=25.0, hero="selene"
    ),
    "seraphina": partial(
        Player, weapon="runetracer", health=100.0, speed=25.0, hero="seraphina"
    ),
    "theron": partial(Player, weapon="garlic", health=100.0, speed=25.0, hero="theron"),
}


# class Strategist:
#     def __init__(self, team):
#         self.team = team
#         self.xp = 0
#         self.next_player_to_levelup = 0

#     def levelup(self, players):
#         self.next_player_to_levelup = (self.next_player_to_levelup + 1) % len(players)

#         list(players.values())[self.next_player_to_levelup].levelup()


class Team:
    def __init__(self, players: list, strategist: Any):
        self.players = players
        self.strategist = strategist
