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
    restart=False,
    xp_cheat=1.0,
    save_state_on_exit=True,
)
