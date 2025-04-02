# SPDX-License-Identifier: BSD-3-Clause

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)


from . import config
from .sprites import make_sprites
from .worlds import World


class Graphics:
    def __init__(
        self, players: dict, world: World, side: str = None, show_scenery: bool = True
    ):
        self._title = "Til the Night Ends"

        self.app = pg.mkQApp()

        self.main_window = QMainWindow()
        self.main_window.setWindowTitle(self._title)
        width = 1900
        left = 0
        if side is not None:
            width = width // 2
        if side == "right":
            left = width + 1
        self.main_window.setGeometry(left, 0, width, 1000)

        # Create a central widget to hold the two widgets
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a widget for the graphics
        self.window = pg.GraphicsLayoutWidget()
        layout.addWidget(self.window)

        # Bottom bar for player status
        bottom_bar = QWidget()
        layout.addWidget(bottom_bar)
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        bottom_bar.setMinimumHeight(int(self.main_window.height() * 0.1))

        # For each player, add a widget to the bottom bar.
        # The widget will contain (from top to bottom):
        # - The player's name
        # - The player's hero image
        # - The player's health as a bar that is green when above 50% and red when below

        self.player_status = {}

        for name, player in players.items():
            widget = QWidget()
            widget_layout = QVBoxLayout(widget)
            widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            header = QLabel(f"{name}")
            widget_layout.addWidget(header)
            body = QWidget()
            body_layout = QHBoxLayout(body)
            path = config.resources / "heroes" / f"{player.hero}.png"
            image = QLabel(f'<img src="{path}" width="32" height="32">')
            body_layout.addWidget(image)
            levels = QLabel()
            body_layout.addWidget(levels)
            body_layout.addStretch()
            widget_layout.addWidget(body)
            footer = QLabel()
            widget_layout.addWidget(footer)
            widget.setMinimumWidth(
                int(self.main_window.width() * 0.95 / (len(players) + 1))
            )
            bottom_bar_layout.addWidget(widget)
            self.player_status[name] = {
                "header": header,
                "footer": footer,
                "image": image,
                "levels": levels,
            }

        # Use large font in label
        self.xp = QLabel()
        self.xp.setFont(QtGui.QFont("", 16))
        bottom_bar_layout.addWidget(self.xp)

        self.canvas = self.window.addPlot()
        self.monsters = {}
        self.heroes = {}
        self.hero = None

        self.viewbox = self.canvas.getViewBox()
        self.viewbox.setAspectLocked(True)
        self.canvas.hideAxis("left")
        self.canvas.hideAxis("bottom")
        self.canvas.hideAxis("right")
        self.canvas.hideAxis("top")

        self.add_scenery(world, show_scenery=show_scenery)

        self.main_window.show()

    def add_scenery(self, world: World, show_scenery: bool = True):
        self.window.setBackground(world.background)
        if not show_scenery:
            return
        self.scenery_sprites = []
        for i in range(world.nsprites):
            self.scenery_sprites.append(
                make_sprites(
                    sprite_path=config.resources
                    / "worlds"
                    / world.name
                    / f"{world.name}{i}.png",
                    positions=config.rng.uniform(
                        -config.map_size, config.map_size, (500, 2)
                    ),
                )
            )

        for sprite in self.scenery_sprites:
            self.add(sprite)

    def update_player_status(self, players, xp, t):
        for name, player in players.items():
            img = "green_pixel.png" if player.health > 50 else "red_pixel.png"
            self.player_status[name]["footer"].setText(
                f'<img src="{config.resources / "other" / img}" '
                f'width="{player.health // 2}" height="4">'
            )

            if not player.alive:
                suffix = "_dead"
                countdown = (
                    f'<span style="font-size: 3em; color: red;">'
                    f"{int(round(player.respawn_time - t))}</span>"
                )
            else:
                suffix = ""
                countdown = ""
            path = config.resources / "heroes" / f"{player.hero}{suffix}.png"
            imgtext = f'<img src="{path}" width="32" height="32">{countdown}'
            self.player_status[name]["image"].setText(imgtext)
            text = [
                f'<img src="{config.resources / "other" / "blank.png"}" '
                f'width="5" height="32">'
            ]
            max_level = max(player.levels.values()) * 2
            scale = 32 / max_level if max_level > 32 else 1
            for i, level in enumerate(player.levels.values()):
                img = f"palette_{i}.png"
                text.append(
                    f'<img src="{config.resources / "other" / img}" '
                    f'width="3" height="{max(int(level * 2 * scale), 1)}">'
                )
            self.player_status[name]["levels"].setText(" ".join(text))
        self.xp.setText(f"XP={int(xp)}")

    def update_time(self, t):
        # Format time in minutes and seconds
        time = f"{int(t // 60):02}:{int(t % 60):02}"
        self.main_window.setWindowTitle(f"{self._title} -- {time}")

    def add(self, sprites):
        self.canvas.addItem(sprites)

    def set_hero(self, hero):
        self.hero = hero
