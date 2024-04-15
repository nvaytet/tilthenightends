# SPDX-License-Identifier: BSD-3-Clause

import pythreejs as p3
import numpy as np
from PIL import Image

from . import config


class Monsters:

    def __init__(self, n, kind):

        self.positions = np.random.normal(scale=10, size=(n, 3)).astype("float32") * 5.0
        self.positions[:, 2] = 0
        self.speed = 0.3

        # Create a position buffer geometry
        self.geometry = p3.BufferGeometry(
            attributes={"position": p3.BufferAttribute(array=self.positions)}
        )
        # Create a points material
        im = Image.open(config.resources / f"{kind}.png").convert("RGBA")
        a = np.flipud(np.array(im).astype("float32")) / 255
        self.texture = p3.DataTexture(data=a, format="RGBAFormat", type="FloatType")
        self.material = p3.PointsMaterial(size=2, map=self.texture, transparent=True)
        # Combine the geometry and material into a Points object
        self.sprites = p3.Points(geometry=self.geometry, material=self.material)

    def move(self, dt, players):
        # Compute vectors from current position to target position
        p = players[0]
        target = np.array([p.x, p.y], dtype="float32")
        v = target - self.positions[:, :2]
        # Normalize vectors
        v = v / np.linalg.norm(v, axis=1).reshape(-1, 1)
        # Update positions
        self.positions[:, :2] += v * dt * self.speed
        self.geometry.attributes["position"].array = self.positions.astype("float32")
