# SPDX-License-Identifier: BSD-3-Clause

from . import config
from .monsters import Monsters


class World:
    def __init__(self, name, nsprites, background, monsters):
        self.name = name
        self.nsprites = nsprites
        self.background = background
        self.monsters = monsters


s = 0.1067 * config.map_size
d = 25.0


class Forest(World):
    def __init__(self):
        super().__init__(
            name="forest",
            nsprites=7,
            background="#1a4a0b",
            monsters=[
                Monsters(size=2000, kind="bat", distance=config.map_size / 3, scale=s),
                Monsters(
                    size=1000,
                    kind="rottingghoul",
                    distance=config.map_size / 2,
                    scale=s,
                ),
                Monsters(
                    size=1000,
                    kind="warewolf",
                    distance=config.map_size / 1.75,
                    scale=s,
                ),
                Monsters(
                    size=500, kind="giantbat", distance=2 * config.map_size / 3, scale=s
                ),
                Monsters(
                    size=500,
                    kind="thereaper",
                    distance=0.833 * config.map_size,
                    scale=s,
                ),
            ],
        )


class Mountain(World):
    def __init__(self):
        super().__init__(
            name="mountain",
            nsprites=7,
            background="#d9dbf0",
            monsters=[
                Monsters(
                    size=2000, kind="zombie", distance=config.map_size / 3, scale=s
                ),
                Monsters(
                    size=1000,
                    kind="lizard",
                    distance=config.map_size / 2,
                    scale=s,
                ),
                Monsters(
                    size=1000,
                    kind="sigrarossi",
                    distance=config.map_size / 1.75,
                    scale=s,
                ),
                Monsters(
                    size=500,
                    kind="orochimario",
                    distance=2 * config.map_size / 3,
                    scale=s,
                ),
                Monsters(
                    size=500,
                    kind="mantis",
                    distance=0.833 * config.map_size,
                    scale=s,
                ),
            ],
        )


class Desert(World):
    def __init__(self):
        super().__init__(
            name="desert",
            nsprites=9,
            background="#e5a253",
            monsters=[
                Monsters(
                    size=2000, kind="skeleton", distance=config.map_size / 3, scale=s
                ),
                Monsters(
                    size=1000, kind="mamba", distance=config.map_size / 2, scale=s
                ),
                Monsters(
                    size=1000, kind="volcano", distance=config.map_size / 1.75, scale=s
                ),
                Monsters(
                    size=500, kind="snake", distance=2 * config.map_size / 3, scale=s
                ),
                Monsters(
                    size=500,
                    kind="minotaur",
                    distance=0.833 * config.map_size,
                    scale=s,
                ),
            ],
        )


class Mine(World):
    def __init__(self):
        super().__init__(
            name="mine",
            nsprites=7,
            background="#808080",
            monsters=[
                Monsters(
                    size=2000,
                    kind="ghost",
                    distance=config.map_size / 3,
                    scale=s,
                    clumpy=False,
                ),
                Monsters(
                    size=1000, kind="molisano", distance=config.map_size / 2, scale=s
                ),
                Monsters(
                    size=1000,
                    kind="swordgardian",
                    distance=config.map_size / 1.75,
                    scale=s,
                ),
                Monsters(
                    size=500, kind="thehag", distance=2 * config.map_size / 3, scale=s
                ),
                Monsters(
                    size=500,
                    kind="medusa",
                    distance=0.833 * config.map_size,
                    scale=s,
                ),
                Monsters(
                    size=500,
                    kind="thedrowner",
                    distance=1.0 * config.map_size,
                    scale=s,
                ),
            ],
        )
