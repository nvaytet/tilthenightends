# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass
from pathlib import Path
import importlib_resources as ir
import numpy as np

# # import pyglet
# from matplotlib import font_manager
# from PIL import ImageFont


# def get_screen_size():
#     display = pyglet.canvas.Display()
#     screen = display.get_default_screen()
#     return screen.width, screen.height


@dataclass(frozen=True)
class Config:
    scoreboard_width: int = 200
    fps: int = 30
    resources: Path = ir.files("tilthenightends") / "resources"
    # scaling = 64.0 / 2.0
    hit_radius: float = 20.0
    rng: np.random.Generator = np.random.default_rng(seed=42)
    map_size: int = 30000
