# SPDX-License-Identifier: BSD-3-Clause


# import pyglet

# from pyglet.gl import *

# from .terrain import Terrain
# from .tools import text_to_image


import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


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


def make_sprites(sprite_path, positions):
    spots = [{"pos": pos, "data": 1} for pos in positions]
    return SpriteScatterPlotItem(sprite_path, spots=spots)


class Graphics:
    def __init__(self):
        self.app = pg.mkQApp("Til the Night Ends")
        self.window = pg.GraphicsLayoutWidget()
        self.window.setBackground("#808080")
        self.canvas = self.window.addPlot()
        self.monsters = {}
        self.heroes = {}

        self.canvas.getViewBox().setAspectLocked(True)
        self.canvas.hideAxis("left")
        self.canvas.hideAxis("bottom")
        self.canvas.hideAxis("right")
        self.canvas.hideAxis("top")
        self.window.show()

    def add(self, sprites):
        # n = 10000
        # pos = np.random.normal(size=(2, n)) * 1000.0
        # spots = [{"pos": pos, "data": 1} for pos in monsters.positions]
        # sprite_path = config.resources / "monsters" / f"{monsters.kind}.png"
        # self.monsters[monsters.kind] = SpriteScatterPlotItem(sprite_path, spots=spots)
        self.canvas.addItem(sprites)

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
