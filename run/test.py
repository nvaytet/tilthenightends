# SPDX-License-Identifier: BSD-3-Clause


import tilthenightends as tne
from survivor_bot import team

# bots = []
# for repo in glob.glob("*_bot"):
#     module = importlib.import_module(f"{repo}")
#     bots.append(module.Bot())

tne.play(
    team=team,
    world="mine",
    manual=False,  # Set to True to play manually using the keyboard arrow keys
    music=False,
    seed=10,
    # follow=True,
    restart=None,
)
