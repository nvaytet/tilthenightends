# SPDX-License-Identifier: BSD-3-Clause


# import pythreejs as p3

# # import pyglet
# from matplotlib.colors import hex2color

# from .tools import Instructions, image_to_sprite, recenter_image, text_to_raw_image

from typing import Any
import numpy as np

from . import config
from .graphics import make_sprites
from .tools import Vector, Towards, LevelupOptions
from .weapons import Weapon

# MAX_PROJECTILES = 100


class Player:
    def __init__(
        self,
        # vector: np.ndarray,
        # weapon: str,
        health: float,
        speed: float,
        hero: str,
        x: float,
        y: float,
        positions: np.ndarray,
        healths: np.ndarray,
        attacks: np.ndarray,
        radii: np.ndarray,
        vectors: np.ndarray,
        # speeds: np.ndarray,
        weapon: Weapon,
        storage_position: float,
    ):
        self.hero = hero
        self.timer = 0.0
        # self.x = x
        # self.y = y
        # self.speed = speed  # 5.0  # * config.scaling
        # self._vector = np.array([0.0, 1.0])  # vector / np.linalg.norm(vector)
        # self.max_health = health
        # self.health = health  # 100.0
        # self.defense = 0.0
        # self.weapon = arsenal[weapon.lower()](owner=self)
        # self.attack = 0.0
        # self.radius = 20.0
        # print(self.position)
        self.weapon = weapon
        self.storage_position = storage_position
        # self.weapon_timer =

        self.positions = positions
        self.healths = healths
        self.attacks = attacks
        self.radii = radii
        self.vectors = vectors
        self.speeds = np.zeros_like(self.attacks).reshape(-1, 1)
        self.expire = np.zeros_like(self.attacks)

        # self._positions = np.full((MAX_PROJECTILES + 1, 2), np.nan)
        # self._vectors = np.full((MAX_PROJECTILES + 1, 2), np.nan)
        # self._healths = np.zeros(MAX_PROJECTILES + 1)
        # self._attacks = np.zeros(MAX_PROJECTILES + 1)

        self.position = np.array([x, y])
        self.health = health
        self.attacks[0] = 0.0
        self.radii[0] = 20.0
        self.speeds[0] = speed
        self.expire[0] = np.inf

        # self.weapon = arsenal[weapon.lower()](owner=self)
        # self.healths[1:] = self.weapon.health
        self.attacks[1:] = self.weapon.damage
        self.radii[1:] = self.weapon.radius
        self.speeds[1:] = self.weapon.speed

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

        # print("position", self.positions[0:1, :])

        self.avatar = make_sprites(
            sprite_path=config.resources / "heroes" / f"{self.hero}.png",
            positions=self.positions[0:1, :],
        )
        # print(config.resources / "weapons" / f"{self.weapon.name}.png")
        # print(self.positions[1:, :])
        # print(

        # self.fire(t=0.0)

        self.weapon_sprites = make_sprites(
            sprite_path=config.resources / "weapons" / f"{self.weapon.name}.png",
            positions=self.positions[1:, :],
            width=self.weapon.radius * 2,
            height=self.weapon.radius * 2,
        )

    @property
    def position(self):
        return self.positions[0, :]

    @position.setter
    def position(self, xy):
        self.positions[0, :] = xy

    @property
    def health(self):
        return self.healths[0]

    @health.setter
    def health(self, value):
        self.healths[0] = value

    @property
    def attack(self):
        return self.attacks[0]

    # @attack.setter
    # def attack(self, value):
    #     self.attacks[0] = value

    @property
    def radius(self):
        return self.radii[0]

    @property
    def speed(self):
        return self.speeds[0]

    @speed.setter
    def speed(self, value):
        self.speeds[0] = value

    # def add_to_graphics(self):
    #     self.avatar = make_sprites(
    #         sprite_path=config.resources / "heroes" / f"{self.hero}.png",
    #         positions=self._positions[0, :],
    #     )
    #     self.weapon_sprites = make_sprites(
    #         sprite_path=config.resources / "weapons" / f"{self.name.lower()}.png",
    #         positions=self._positions[1:, :],
    #         width=self.weapon.radius * 2,
    #         height=self.weapon.radius * 2,
    #     )

    def execute_bot_instructions(self, direction: Vector | Towards | None):
        if direction is None:
            return
        if isinstance(direction, Vector):
            self.vector = np.array([direction.x, direction.y])
        elif isinstance(direction, Towards):
            x, y = self.position
            self.vector = np.array([direction.x - x, direction.y - y])

        # self.vector = np.array(
        #     [int(move.right) - int(move.left), int(move.up) - int(move.down)]
        # )

    @property
    def alive(self) -> bool:
        return self.health > 0

    def move(self, dt: float):
        # self.x += self.speed * dt * self.vector[0]
        # self.y += self.speed * dt * self.vector[1]
        # self.position += self.speed * dt * self.vector
        # self.geometry.attributes["position"].array = np.array(
        #     [[self.x, self.y, 0.0], [self.x - 1.0, self.y - 1.0, 0.0]]
        # ).astype("float32")
        # self.avatar.position = [self.x, self.y, 0.0]
        # print(f"Player moved to {self.x}, {self.y}.")

        # self.position += self.speed * dt * self.vector
        self.positions += self.speeds * dt * self.vectors

        self.avatar.setData(pos=self.positions[0:1, :])
        self.weapon_sprites.setData(pos=self.positions[1:, :])

    # @property
    # def position(self) -> np.ndarray:
    #     return np.array([self.x, self.y])

    @property
    def vector(self) -> np.ndarray:
        return self.vectors[0, :]

    @vector.setter
    def vector(self, value: np.ndarray):
        v = np.asarray(value)
        norm = np.linalg.norm(v)
        if norm > 0.0:
            v = v / norm
        self.vectors[0, :] = v

    def die(self, t):
        # Start countdown to respawn
        return

    def as_dict(self):
        return {
            "hero": self.hero,
            "position": self.position,
            # "y": self.y,
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

    def fire(self, t):
        print("t, self.timer", t, self.timer)
        # Find an empty slot in the arrays
        ind = np.squeeze(np.where(np.isnan(self.healths)))[0]
        self.positions[ind, :] = self.position
        print("ind", ind, self.positions[ind, :], self.position)
        v = np.random.uniform(-1, 1, 2)
        norm = np.linalg.norm(v)
        if norm > 0.0:
            v /= norm
        self.vectors[ind, :] = v
        # print(self.vectors)
        self.healths[ind] = self.weapon.health
        # self._active_slots[ind] = True
        # self.projectile_counter = np.sum(self._active_slots)

        # self.positions[: self.nprojectiles, 0] = x
        # self.positions[: self.nprojectiles, 1] = y
        # self.tstart = t
        # self.tend = t + self.longevity
        # self.sprites.setData(pos=self.positions)
        # self.draw_sprites()
        self.timer = t + self.weapon.cooldown
        self.expire[ind] = t + self.weapon.duration

    def expire_projectiles(self, t):
        inds = (self.expire < t) | (self.healths < 0.0)
        inds[0] = False
        self.healths[inds] = np.nan
        self.positions[inds, :] = self.storage_position

    # def kill_projectiles(self):
    #     inds = self.healths


# class Runetracer(Player):
#     def __init__(
#         self,
#         *args,
#         weapon=Weapon(
#             name="runetracer",
#             cooldown=5,
#             damage=10,
#             speed=100.0,
#             health=30,
#             radius=12,
#             max_projectiles=5,
#         ),
#         **kwargs,
#     ):
#         super().__init__(
#             *args,
#             weapon=weapon,
#             **kwargs,
#         )


# heroes = {
#     "alaric": partial(Runetracer, health=100.0, speed=25.0, hero="alaric"),
#     "cedric": partial(Runetracer, health=100.0, speed=25.0, hero="cedric"),
#     "evelyn": partial(Runetracer, health=100.0, speed=25.0, hero="evelyn"),
#     "garron": partial(Runetracer, health=100.0, speed=25.0, hero="garron"),
#     "isolde": partial(Runetracer, health=100.0, speed=25.0, hero="isolde"),
#     "kaelen": partial(Runetracer, health=100.0, speed=25.0, hero="kaelen"),
#     "lyra": partial(Runetracer, health=100.0, speed=25.0, hero="lyra"),
#     "selene": partial(Runetracer, health=100.0, speed=25.0, hero="selene"),
#     "seraphina": partial(Runetracer, health=100.0, speed=25.0, hero="seraphina"),
#     "theron": partial(Runetracer, health=100.0, speed=25.0, hero="theron"),
# }

# heroes = {
#     "alaric": partial(
#         Player, weapon="fireball", health=100.0, speed=25.0, hero="alaric"
#     ),
#     "cedric": partial(
#         Player, weapon="runetracer", health=100.0, speed=25.0, hero="cedric"
#     ),
#     "evelyn": partial(
#         Player, weapon="runetracer", health=100.0, speed=25.0, hero="evelyn"
#     ),
#     "garron": partial(Player, weapon="dove", health=100.0, speed=25.0, hero="garron"),
#     "isolde": partial(
#         Player, weapon="holywater", health=100.0, speed=25.0, hero="isolde"
#     ),
#     "kaelen": partial(
#         Player, weapon="lightning", health=100.0, speed=25.0, hero="kaelen"
#     ),
#     "lyra": partial(Player, weapon="runetracer", health=100.0, speed=25.0, hero="lyra"),
#     "selene": partial(
#         Player, weapon="runetracer", health=100.0, speed=25.0, hero="selene"
#     ),
#     "seraphina": partial(
#         Player, weapon="runetracer", health=100.0, speed=25.0, hero="seraphina"
#     ),
#     "theron": partial(Player, weapon="garlic", health=100.0, speed=25.0, hero="theron"),
# }


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
