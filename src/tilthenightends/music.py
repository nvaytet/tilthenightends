# SPDX-License-Identifier: BSD-3-Clause

try:
    from pygame import mixer
except ImportError:
    mixer = None

from . import config


def play_music(world, match=False):
    if mixer is not None:
        mixer.init()
        mixer.music.load(str(config.resources / "worlds" / world / f"{world}.mp3"))
        mixer.music.play(-1)
        if match:
            while True:
                pass
