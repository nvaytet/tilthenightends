# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa

from .config import Config

config = Config()

from .engine import Engine
from .player import Player, Team
from .tools import Vector, Levelup, LevelupOptions, Towards


def play(*args, **kwargs):
    eng = Engine(*args, **kwargs)
    return eng.run()


__all__ = [
    "Config",
    "config",
    "Engine",
    "Player",
    "Team",
    "Levelup",
    "LevelupOptions",
    "Vector",
    "Towards",
    "play",
]
