# SPDX-License-Identifier: BSD-3-Clause


# import pythreejs as p3

# # import pyglet
# from matplotlib.colors import hex2color

# from .tools import Instructions, image_to_sprite, recenter_image, text_to_raw_image

from dataclasses import dataclass
from functools import partial
from typing import Any
import numpy as np

from . import config
from .graphics import make_sprites
from .tools import Vector, Towards, LevelupOptions
from .weapons import arsenal


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
        self.x = x
        self.y = y
        self.speed = speed  # 5.0  # * config.scaling
        self.vector = np.array([0.0, 0.0])  # vector / np.linalg.norm(vector)
        self.max_health = health
        self.health = health  # 100.0
        self.freeze = 0.0
        # self.defense = 0.0
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
        }

        # Create a position buffer geometry
        # self.geometry = p3.BufferGeometry(
        #     attributes={
        #         "position": p3.BufferAttribute(
        #             array=np.array(
        #                 [[self.x, self.y, 0.0], [self.x - 1.0, self.y - 1.0, 0.0]]
        #             ).astype("float32")
        #         )
        #     }
        # )

        # im = Image.open(config.resources / "heroes" / "pasqualina.png").convert("RGBA")
        # a = np.flipud(np.array(im).astype("float32")) / 255
        # self.texture = p3.DataTexture(data=a, format="RGBAFormat", type="FloatType")
        # # self.material = p3.PointsMaterial(size=2, map=self.texture, transparent=True)
        # # # Combine the geometry and material into a Points object
        # # self.avatar = p3.Points(geometry=self.geometry, material=self.material)

        # self.material = p3.SpriteMaterial(
        #     map=self.texture,
        #     transparent=True,
        # )
        # self.avatar = p3.Sprite(
        #     material=self.material, position=[self.x, self.y, 0.0], scale=[1, 1, 1]
        # )
        # # scale=[size, size, size]
        # # )

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

        # self.vector = np.array(
        #     [int(move.right) - int(move.left), int(move.up) - int(move.down)]
        # )

    def maybe_respawn(self, t):
        if t > self.respawn_time:
            print(f"Player {self.hero} respawning.", t, self.respawn_time)
            self.health = self.max_health * 0.5
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
        # self.geometry.attributes["position"].array = np.array(
        #     [[self.x, self.y, 0.0], [self.x - 1.0, self.y - 1.0, 0.0]]
        # ).astype("float32")
        # self.avatar.position = [self.x, self.y, 0.0]
        # print(f"Player moved to {self.x}, {self.y}.")
        self.avatar.setData(pos=np.array([[self.x, self.y]]))
        # self.dead_avatar.setData(pos=np.array([[self.x, self.y]]))

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
        # print(f"Player {self.hero} DIED.", t)
        # Start countdown to respawn
        self.respawn_time = t + config.respawn_time
        self.dead_avatar.setOpacity(1.0)
        self.dead_avatar.setData(pos=np.array([[self.x, self.y]]))
        self.avatar.setOpacity(0.0)
        print(f"Player {self.hero} DIED.", t, self.respawn_time)
        self.weapon.projectiles = []
        self.weapon.draw_sprites()
        # return

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
            "alive": self.alive,
            "respawn_time": self.respawn_time,
        }

    def levelup(self, what):
        if not self.alive:
            print(f"Player {self.hero} is dead and cannot level up.")
            return
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
        elif what == LevelupOptions.weapon_size:
            if self.weapon.name == "LightningBolt":
                self.weapon.nprojectiles += 1
            else:
                self.weapon.radius *= 1.15
            self.levels["weapon_size"] += 1

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


@dataclass(frozen=True)
class PlayerInfo:
    x: float
    y: float
    speed: float
    vector: np.ndarray
    health: float
    weapon: dict
    levels: dict
    alive: bool
    respawn_time: float
