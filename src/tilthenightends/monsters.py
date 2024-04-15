import pythreejs as p3
import numpy as np


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

        self.texture = p3.ImageTexture(imageUri=f"{kind}.png")
        self.material = p3.PointsMaterial(size=2, map=self.texture, transparent=True)
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
