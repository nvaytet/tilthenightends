# SPDX-License-Identifier: BSD-3-Clause


import tilthenightends as tne
from survivor_bot import team

# bots = []
# for repo in glob.glob("*_bot"):
#     module = importlib.import_module(f"{repo}")
#     bots.append(module.Bot())

tne.play(
    team=team,  # Must be a Team instance with players and a strategist
    world="forest",  # "forest", "mountain", "desert", "mine"
    music=False,
    seed=None,
    # follow=True,
    xp_cheat=1.0,
    restart=False,  # Set to -1 to restart from last run, or filename otherwise
    save_state_on_exit=True,
    show_scenery=True,  # Set to False to hide the scenery for better performance
    speedup=1.0,  # Set to 2.0 for double speed
)
