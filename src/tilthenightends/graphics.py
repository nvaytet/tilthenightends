# SPDX-License-Identifier: BSD-3-Clause

import datetime

import numpy as np

# import pyglet

# from pyglet.gl import *
import pythreejs as p3
import ipywidgets as ipw

# from . import config
# from .terrain import Terrain
# from .tools import text_to_image


class Graphics:
    def __init__(self):

        # Create the scene and the renderer
        view_width = 1000
        view_height = 800
        self.camera = p3.PerspectiveCamera(
            position=[0, 0, 100], aspect=view_width / view_height
        )
        # camera = p3.OrthographicCamera(-10, 10, -10, 10, -1, 300)
        self.scene = p3.Scene(background="#DDDDDD")
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
