# SPDX-License-Identifier: BSD-3-Clause


import tilthenightends as tne
from survivor_bot import team


tne.play(
    team=team,  # Must be a Team instance with players and a strategist
    world="forest",  # "forest", "mountain", "desert", "mine"
    music=False,
    seed=None,
    xp_cheat=1.0,
    show_scenery=True,  # Set to False to hide the scenery for better performance
    speedup=1.0,  # Set to 2.0 for double speed
)
