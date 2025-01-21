# SPDX-License-Identifier: BSD-3-Clause

from multiprocessing import Process
import numpy as np

import tilthenightends as tne
from survivor_bot import team

team1 = team
team2 = team

music = False


if __name__ == "__main__":
    seed = np.random.randint(0, 2**32 - 1)
    p1 = Process(
        target=tne.play,
        kwargs=dict(
            team=team1, world="mine", manual=False, music=music, side="left", seed=seed
        ),
    )
    p2 = Process(
        target=tne.play,
        kwargs=dict(
            team=team2, world="mine", manual=False, music=music, side="right", seed=seed
        ),
    )

    p1.start()
    p2.start()
    p1.join()
    p2.join()
