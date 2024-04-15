# SPDX-License-Identifier: BSD-3-Clause

import uuid
from typing import Tuple

import numpy as np
import pyglet

from . import config
from .tools import recenter_image


class Asteroid:
    def __init__(
        self,
        x: float,
        y: float,
        v: float,
        heading: float,
        size: float,
        batch: pyglet.graphics.Batch,
    ):
        self.id = uuid.uuid4().hex
        self.v = v
        self.size = int(size)
        self.heading = heading
        self.make_avatar(x, y, batch)

    def make_avatar(self, x: float, y: float, batch: pyglet.graphics.Batch):
        img = pyglet.image.load(config.resources / "asteroid.png")
        self.avatar = pyglet.sprite.Sprite(
            img=recenter_image(img),
            x=x,
            y=y,
            batch=batch,
        )
        self.avatar.width = self.size
        self.avatar.height = self.size
        self.avatar.rotation = -self.heading

    @property
    def x(self) -> float:
        return self.avatar.x

    @x.setter
    def x(self, value: float):
        self.avatar.x = value

    @property
    def y(self) -> float:
        return self.avatar.y

    @y.setter
    def y(self, value: float):
        self.avatar.y = value

    def velocity_vector(self) -> Tuple[float, float]:
        return (
            self.v * np.cos(np.radians(self.heading)),
            self.v * np.sin(np.radians(self.heading)),
        )

    def move(self, dt: float):
        vx, vy = self.velocity_vector()
        self.x += vx * dt
        self.y += vy * dt
        self.x = self.x % config.nx

    def tip(self) -> Tuple[float, float]:
        tipx = self.x + self.size * np.cos(np.radians(self.heading)) / 2
        tipy = self.y + self.size * np.sin(np.radians(self.heading)) / 2
        return tipx % config.nx, tipy

    def to_dict(self) -> dict:
        x, y = self.tip()
        return {
            "id": self.id,
            "position": (x, y),
            "velocity": self.velocity_vector(),
            "heading": self.heading,
            "size": self.size * config.asteroid_tip_size,
        }
