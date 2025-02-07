# SPDX-License-Identifier: BSD-3-Clause

import argparse
from multiprocessing import Process
import numpy as np

import tilthenightends as tne
from survivor_bot import team
from tilthenightends.music import play_music

team1 = team
team2 = team

music = True


parser = argparse.ArgumentParser()
parser.add_argument("world")
args = parser.parse_args()


if __name__ == "__main__":
    seed = np.random.randint(0, 2**32 - 1)
    p1 = Process(
        target=tne.play,
        kwargs=dict(
            team=team1,
            world=args.world,
            music=False,
            side="left",
            seed=seed,
        ),
    )
    p2 = Process(
        target=tne.play,
        kwargs=dict(
            team=team2,
            world=args.world,
            music=False,
            side="right",
            seed=seed,
        ),
    )
    p3 = Process(
        target=play_music if music else lambda: None,
        kwargs=dict(world=args.world, match=True),
    )

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
