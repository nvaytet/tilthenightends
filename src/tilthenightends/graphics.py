# SPDX-License-Identifier: BSD-3-Clause


# import pyglet

# from pyglet.gl import *
import pythreejs as p3
import numpy as np
from PIL import Image

# from . import config
# from .terrain import Terrain
# from .tools import text_to_image


class Graphics:
    def __init__(self):
        # Create the scene and the renderer
        view_width = 1000
        view_height = 800
        self.camera = p3.PerspectiveCamera(
            position=[0, 0, 100], aspect=view_width / view_height, near=0.001, far=10000
        )

        im = Image.open("dirt.jpg").convert("RGBA")
        a = np.flipud(np.array(im).astype("float32")) / 255
        texture = p3.DataTexture(data=a, format="RGBAFormat", type="FloatType")
        material = p3.SpriteMaterial(map=texture, transparent=True)
        s = 50
        w, h = im.width / s, im.height / s
        background = p3.Sprite(
            material=material,
            position=[-0.25 * w, -0.25 * h, -1.0],
            scale=[w, h, 1],
        )

        # camera = p3.OrthographicCamera(-10, 10, -10, 10, -1, 300)
        self.scene = p3.Scene(background="#DDDDDD")
        self.scene.add(background)
        # self.scene = p3.Scene(background=texture)
        self.controller = p3.OrbitControls(
            controlling=self.camera,
            enableRotate=False,
        )
        self.renderer = p3.Renderer(
            camera=self.camera,
            scene=self.scene,
            controls=[self.controller],
            width=view_width,
            height=view_height,
        )

    def add(self, obj):
        self.scene.add(obj)
