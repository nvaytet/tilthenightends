# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa

from .config import Config

config = Config()

from .engine import Engine

# from .tools import Instructions


def play(*args, **kwargs):
    eng = Engine(*args, **kwargs)
    return eng.run()
