# SPDX-License-Identifier: BSD-3-Clause


# import pyglet

# from pyglet.gl import *

# from .terrain import Terrain
# from .tools import text_to_image

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Qt.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)


# from PyQt5.QtWidgets import (
#         QCheckBox,
#         QFrame,
#         QHBoxLayout,
#         QLabel,
#         QMainWindow,
#         QSizePolicy,
#         QSlider,
#         QVBoxLayout,
#         QWidget,
#         QPushButton,
#     )
#     from PyQt5.QtCore import Qt

from . import config


class SpriteScatterPlotItem(pg.ScatterPlotItem):
    def __init__(self, sprite_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprite = QtGui.QPixmap(str(sprite_path)).transformed(
            QtGui.QTransform().scale(1, -1)
        )
        self.sprite_size = self.sprite.size()

    def paint(self, p, opt, widget):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        for i in range(len(self.data)):
            spot = self.data[i]
            x, y = spot[0], spot[1]
            p.drawPixmap(
                QtCore.QPointF(
                    x - self.sprite_size.width() / 2, y - self.sprite_size.height() / 2
                ),
                self.sprite,
            )


# class KeyPressWindow(pg.GraphicsLayoutWidget):
#     sigKeyPress = QtCore.pyqtSignal(object)

#     def keyPressEvent(self, ev):
#         self.scene().keyPressEvent(ev)
#         self.sigKeyPress.emit(ev)


class KeyPressWindow(pg.GraphicsLayoutWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.hero = None
        self.pressed_keys = set()

    def keyPressEvent(self, event):
        self.pressed_keys.add(event.key())
        event.accept()

    def keyReleaseEvent(self, event):
        if event.key() in self.pressed_keys:
            self.pressed_keys.remove(event.key())
        event.accept()

    # def update_position(self):
    #     # if self.hero is None:
    #     #     return

    #     dx, dy = 0, 0
    #     if QtCore.Qt.Key_Left in self.pressed_keys:
    #         dx -= self.step_size
    #     if QtCore.Qt.Key_Right in self.pressed_keys:
    #         dx += self.step_size
    #     if QtCore.Qt.Key_Up in self.pressed_keys:
    #         dy -= self.step_size
    #     if QtCore.Qt.Key_Down in self.pressed_keys:
    #         dy += self.step_size

    # def keyPressEvent(self, event):
    #     if self.hero is None:
    #         return

    #     key = event.key()

    #     if key == QtCore.Qt.Key_Left:
    #         self.hero.vector = np.array([-1, 0])
    #     elif key == QtCore.Qt.Key_Right:
    #         self.hero.vector = np.array([1, 0])
    #     elif key == QtCore.Qt.Key_Up:
    #         self.hero.vector = np.array([0, 1])
    #     elif key == QtCore.Qt.Key_Down:
    #         self.hero.vector = np.array([0, -1])
    #     else:
    #         super().keyPressEvent(event)


def make_sprites(sprite_path, positions):
    spots = [{"pos": pos, "data": 1} for pos in positions]
    return SpriteScatterPlotItem(sprite_path, spots=spots)


class Graphics:
    def __init__(self, players: dict, manual=False):
        self._manual = manual
        self._title = "Til the Night Ends"

        self.app = pg.mkQApp()

        self.main_window = QMainWindow()
        self.main_window.setWindowTitle(self._title)
        self.main_window.setGeometry(0, 0, 1400, 900)

        # Create a central widget to hold the two widgets
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        self.window = KeyPressWindow() if self._manual else pg.GraphicsLayoutWidget()
        self.window.setBackground("#808080")

        # window_widget = QWidget()
        # window_widget_layout = QVBoxLayout(window_widget)
        # window_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        # window_widget_layout.addWidget(self.window)
        # # self.window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # self.window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        # self.window.setMinimumHeight(int(self.main_window.height() * 0.85))
        # layout.addWidget(window_widget)

        layout.addWidget(self.window)

        # Bottom bar for player status
        bottom_bar = QWidget()
        layout.addWidget(bottom_bar)
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        bottom_bar.setMinimumHeight(int(self.main_window.height() * 0.1))
        # bottom_bar_layout.setColumnStretch(','.join(['1'] * len(players)))

        # For each player, add a widget to the bottom bar.
        # The widget will contain (from top to bottom):
        # - The player's name
        # - The player's hero image
        # - The player's health as a bar that is green when above 50% and red when below

        self.player_status = {}

        # bottom_bar_layout.addStretch()
        for name, player in players.items():
            widget = QWidget()
            widget_layout = QVBoxLayout(widget)
            widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            header = QLabel(f"{name}")
            widget_layout.addWidget(header)
            path = config.resources / "heroes" / f"{player.hero}.png"
            image = QLabel(f'<img src="{path}" width="32" height="32">')
            widget_layout.addWidget(image)
            # health = player.health
            footer = QLabel(
                # f'<img src="{config.resources / "other" / "green_pixel.png"}" width="{health // 2}" height="4">'
            )
            widget_layout.addWidget(footer)
            widget.setMinimumWidth(int(self.main_window.width() * 0.95 / len(players)))
            bottom_bar_layout.addWidget(widget)
            # bottom_bar_layout.addStretch()
            self.player_status[name] = {
                "header": header,
                "footer": footer,
                "image": image,
            }

        self.canvas = self.window.addPlot()
        self.monsters = {}
        self.heroes = {}
        self.hero = None

        self.canvas.getViewBox().setAspectLocked(True)
        self.canvas.hideAxis("left")
        self.canvas.hideAxis("bottom")
        self.canvas.hideAxis("right")
        self.canvas.hideAxis("top")
        self.main_window.show()

    def update_player_status(self, players):
        for name, player in players.items():
            img = "green_pixel.png" if player.health > 50 else "red_pixel.png"
            self.player_status[name]["footer"].setText(
                f'<img src="{config.resources / "other" / img}" '
                f'width="{player.health // 2}" height="4">'
            )

    def update_time(self, t):
        # Format time in minutes and seconds
        time = f"{int(t // 60):02}:{int(t % 60):02}"
        self.main_window.setWindowTitle(f"{self._title} -- {time}")

    def add(self, sprites):
        # n = 10000
        # pos = np.random.normal(size=(2, n)) * 1000.0
        # spots = [{"pos": pos, "data": 1} for pos in monsters.positions]
        # sprite_path = config.resources / "monsters" / f"{monsters.kind}.png"
        # self.monsters[monsters.kind] = SpriteScatterPlotItem(sprite_path, spots=spots)
        self.canvas.addItem(sprites)

    def set_hero(self, hero):
        self.hero = hero

    def update(self):
        dx, dy = 0.0, 0.0
        if QtCore.Qt.Key_Left in self.window.pressed_keys:
            dx -= 1.0
        if QtCore.Qt.Key_Right in self.window.pressed_keys:
            dx += 1.0
        if QtCore.Qt.Key_Up in self.window.pressed_keys:
            dy += 1.0
        if QtCore.Qt.Key_Down in self.window.pressed_keys:
            dy -= 1.0

        if self.hero is not None:
            self.hero.vector = np.array([dx, dy])

    # def update(self):
    #     for monster in self.monsters.values():
    #         monster.setData(pos=monster.positions.T)

    # # Create the scene and the renderer
    # view_width = 1000
    # view_height = 800
    # self.camera = p3.PerspectiveCamera(
    #     position=[0, 0, 100], aspect=view_width / view_height, near=0.001, far=10000
    # )

    # im = Image.open("dirt.jpg").convert("RGBA")
    # a = np.flipud(np.array(im).astype("float32")) / 255
    # texture = p3.DataTexture(data=a, format="RGBAFormat", type="FloatType")
    # material = p3.SpriteMaterial(map=texture, transparent=True)
    # s = 50
    # w, h = im.width / s, im.height / s
    # background = p3.Sprite(
    #     material=material,
    #     position=[-0.25 * w, -0.25 * h, -1.0],
    #     scale=[w, h, 1],
    # )

    # # camera = p3.OrthographicCamera(-10, 10, -10, 10, -1, 300)
    # self.scene = p3.Scene(background="#DDDDDD")
    # self.scene.add(background)
    # # self.scene = p3.Scene(background=texture)
    # self.controller = p3.OrbitControls(
    #     controlling=self.camera,
    #     enableRotate=False,
    # )
    # self.renderer = p3.Renderer(
    #     camera=self.camera,
    #     scene=self.scene,
    #     controls=[self.controller],
    #     width=view_width,
    #     height=view_height,
    # )

    # def add(self, obj):
    #     self.scene.add(obj)
