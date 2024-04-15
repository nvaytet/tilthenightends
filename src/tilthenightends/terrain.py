# SPDX-License-Identifier: BSD-3-Clause
from functools import reduce

import numpy as np
import pyglet
from PIL import Image
from scipy.ndimage import gaussian_filter

from . import config


class Terrain:
    def __init__(self):
        profile = np.zeros([config.nx])
        nseeds = 100
        xseed = np.random.randint(config.nx, size=nseeds)
        profile[xseed] = 10000 * np.random.random(nseeds)
        self.smooth = gaussian_filter(profile, sigma=30, mode="wrap")
        self.terrain = self.smooth.copy()
        self.landing_sites = np.zeros_like(self.terrain)

        # img = Image.open(config.resources / "lunar-surface.png")
        # if (img.width != config.nx) or (img.height != config.ny):
        #     img = img.resize((config.nx, config.ny))
        # img = img.convert("RGBA")
        # data = img.getdata()
        # self.raw_background = (
        #     np.array(data).reshape(img.height, img.width, 4).astype(np.uint8)
        # )

        nx, ny = 10000, 10000
        im = Image.open(config.resources / "forest.png").convert("RGB")
        array = np.array(im)
        self.raw_background = np.tile(
            array, (ny // array.shape[0] + 1, nx // array.shape[1] + 1, 1)
        )[:ny, :nx]

        # texture = Image.fromarray(tiled)
        # texture

        self.current_background = self.raw_background[
            5000 : 5000 + config.ny, 5000 : 5000 + config.nx
        ]
        print("current_background", self.current_background.shape)
        #     (config.ny, config.nx + config.scoreboard_width, 4), 20, dtype=np.uint8
        # )
        # self.current_background[..., 3] = 255
        # self.current_background[:, : config.nx, :] = self.raw_background
        # self.y_map = np.broadcast_to(
        #     config.ny - np.arange(config.ny).reshape(config.ny, 1),
        #     (config.ny, config.nx),
        # )

        # self.update_background(slice(0, config.nx), slice(0, config.ny))

        # # Add Earth rise
        # earth = Image.open(config.resources / "earth.png").convert("RGBA")
        # earth_data = earth.getdata()
        # earth_array = (
        #     np.array(earth_data).reshape(earth.height, earth.width, 4).astype(np.uint8)
        # )
        # earth_x = 1400
        # earth_y = 100
        # self.current_background[
        #     earth_y : earth_y + earth_array.shape[0],
        #     earth_x : earth_x + earth_array.shape[1],
        #     :,
        # ] = earth_array
        self.background_image = self.terrain_to_image()

    def update_background(self, x, y) -> None:
        # raw = self.raw_background[yslice, xslice]
        # print(x, y)
        iy = int(y)
        ix = int(x)
        self.current_background = self.raw_background[
            iy : iy + config.ny, ix : ix + config.nx
        ]
        self.background_image = self.terrain_to_image()

    def make_crater(self, x: int, scaling: float = 1.0) -> None:
        r = int(round(config.crater_radius * scaling))
        slices = []
        start = x - r
        end = x + r
        if start < 0:
            slices.append(slice(start, None))
            start = 0
        if end > config.nx:
            slices.append(slice(None, end - config.nx))
            end = config.nx
        slices.append(slice(start, end))
        y_val = reduce(min, [self.terrain[sl].min() for sl in slices])
        yslice = slice(200, config.ny - int(y_val))
        for xslice in slices:
            self.terrain[xslice] = float(self.terrain[x])
            self.update_background(xslice, yslice)
        self.background_image = self.terrain_to_image()
        self.update_landing_sites()

    def update_landing_sites(self):
        # Find largest landing site
        n = len(self.terrain)
        # Find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(self.terrain[:-1], self.terrain[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # Find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        for start, length in zip(run_starts, run_lengths):
            self.landing_sites[start : start + length] = length

    def terrain_to_image(self) -> Image:
        img = Image.fromarray(self.current_background)
        return pyglet.image.ImageData(
            width=img.width,
            height=img.height,
            fmt="RGB",
            data=img.tobytes(),
            pitch=-img.width * 3,
        )
