# SPDX-License-Identifier: BSD-3-Clause

import pythreejs as p3
import numpy as np

from . import config


class Monsters:

    def __init__(self, n, kind):

        pos_array = np.random.normal(scale=10, size=(n, 3)).astype("float32") * 5.0
        pos_array[:, 2] = 0

        # Create a position buffer geometry
        self.geometry = p3.BufferGeometry(
            attributes={"position": p3.BufferAttribute(array=pos_array)}
        )
        # Create a points material
        self.speed = 1.0

        print(str(config.resources / f"{kind}.png"))
        path = "../bat.png"

        # self.texture = p3.ImageTexture(imageUri=str(config.resources / f"{kind}.png"))
        self.texture = p3.ImageTexture(imageUri=path)
        print(self.texture)
        # self.texture = p3.ImageTexture(imageUri=f"tilthenightends/resources/{kind}.png")
        self.material = p3.PointsMaterial(size=2, map=self.texture, transparent=True)
        # self.material = p3.PointsMaterial(size=2, color="black")
        # Combine the geometry and material into a Points object
        self.sprites = p3.Points(geometry=self.geometry, material=self.material)

    def move(self, dt):
        # Compute vectors from current position to target position
        target = np.array([0, 0], dtype="float32")
        v = target - self.geometry.attributes["position"].array[:, :2]
        pos_array = self.geometry.attributes["position"].array
        # Normalize vectors
        v = v / np.linalg.norm(v, axis=1).reshape(-1, 1)
        # Update positions
        # print(v.shape, pos_array.shape)
        pos_array[:, :2] += v * dt * self.speed
        print(v)
        # Update the position attribute
        # print(pos_array.dtype, pos_array.shape)
        # assert False
        self.geometry.attributes["position"].array = pos_array
