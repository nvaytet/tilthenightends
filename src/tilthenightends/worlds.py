# SPDX-License-Identifier: BSD-3-Clause

from . import config
from .monsters import Monsters

nsprites = {"forest": 7, "mountain": 7, "desert": 9, "mine": 7}
backgrounds = {
    "forest": "#1a4a0b",
    "mountain": "#d9dbf0",
    "desert": "#e5a253",
    "mine": "#808080",
}


s = 0.1067 * config.map_size  # 32.0
d = 25.0


monsters = {
    "forest": [
        Monsters(size=2000, kind="bat", distance=config.map_size / 3, scale=s),
        Monsters(size=2000, kind="rottingghoul", distance=config.map_size / 2, scale=s),
        Monsters(size=500, kind="giantbat", distance=2 * config.map_size / 3, scale=s),
        Monsters(
            size=500, kind="thereaper", distance=0.833 * config.map_size / 3, scale=s
        ),
    ]
}
