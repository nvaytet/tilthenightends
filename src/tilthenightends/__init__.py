# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa

from .config import Config

config = Config()

from .engine import Engine
from .player import Player, Strategist, Team
from .tools import Move, Levelup, LevelupOptions


def play(*args, **kwargs):
    eng = Engine(*args, **kwargs)
    return eng.run()


__all__ = [
    "Config",
    "config",
    "Engine",
    "Player",
    "Strategist",
    "Team",
    "Move",
    "Levelup",
    "LevelupOptions",
    "play",
]
