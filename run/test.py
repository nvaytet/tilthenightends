# SPDX-License-Identifier: BSD-3-Clause


import tilthenightends as tne

# bots = []
# for repo in glob.glob("*_bot"):
#     module = importlib.import_module(f"{repo}")
#     bots.append(module.Bot())

tne.play(
    # bots=[],  # List of bots to use
    # manual=True,  # Set to True to play manually using the keyboard arrow keys
    # crater_scaling=1.0,  # Artificially increase the size of craters
    # player_collisions=True,  # Set to False to disable collisions between players
    # asteroid_collisions=True,  # Set to False to disable being destroyed by asteroids
    # speedup=1.0,  # Increase to speed up the game (no guarantees this works very well)
    # fullscreen=False,  # Set to True to play in fullscreen mode
    # test=True,  # Set to True to run in test mode
)
