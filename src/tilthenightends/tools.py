# SPDX-License-Identifier: BSD-3-Clause

from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class Vector:
    """
    Set a player's vector.
    """

    x: float
    y: float


@dataclass
class Towards:
    """
    Target for the player to move towards.
    """

    x: float
    y: float


class LevelupOptions(Enum):
    player_health = auto()
    player_speed = auto()
    weapon_health = auto()
    weapon_speed = auto()
    weapon_damage = auto()
    weapon_cooldown = auto()
    weapon_size = auto()
    weapon_longevity = auto()


@dataclass
class Levelup:
    """
    Level up instructions for the player.
    """

    hero: str
    what: LevelupOptions
