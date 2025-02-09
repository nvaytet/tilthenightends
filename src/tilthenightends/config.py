# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import dataclass
from pathlib import Path
import importlib_resources as ir
import numpy as np


@dataclass(frozen=True)
class Config:
    fps: int = 24
    resources: Path = ir.files("tilthenightends") / "resources"
    view_radius: float = 1000.0
    rng: np.random.Generator = np.random.default_rng()  # seed=21)
    map_size: int = 30000
    respawn_time: float = 15.0
    time_limit: float = 10 * 60.0
