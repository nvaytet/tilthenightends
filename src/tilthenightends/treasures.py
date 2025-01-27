# SPDX-License-Identifier: BSD-3-Clause


from . import config
from .graphics import make_sprites


class Loot:
    def __init__(self, size, kind):
        self.positions = config.rng.uniform(
            -config.map_size, config.map_size, (size, 2)
        )

        self.dx = 32
        self.trash = config.map_size * 2

        self.locations = {
            (
                (self.positions[i, 0] + config.map_size) // self.dx,
                (self.positions[i, 1] + config.map_size) // self.dx,
            ): i
            for i in range(size)
        }

        self.sprites = make_sprites(
            sprite_path=config.resources / "other" / f"{kind}.png",
            positions=self.positions,
        )

    def pickup(self, player):
        x, y = player.position
        x = (x + config.map_size) // self.dx
        y = (y + config.map_size) // self.dx
        ind = self.locations.get((x, y))
        if ind is not None:
            self.apply(player)
            self.positions[ind, :] = [self.trash, self.trash]
            self.sprites.setData(self.positions)
            del self.locations[(x, y)]
        # if (x, y) in self.locations:
        #     self.positions[self.locations[(x, y)]] = [0, 0]
        #     del self.locations[(x, y)]
        #     self.apply(player)


class Chicken(Loot):
    def __init__(self, size):
        super().__init__(size, "chicken")

    def apply(self, player):
        player.health += 0.5 * player.max_health


class Treasure(Loot):
    def __init__(self, size):
        super().__init__(size, "treasure")

    def apply(self, player):
        player.score += 100
