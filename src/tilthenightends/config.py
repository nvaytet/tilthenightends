# SPDX-License-Identifier: BSD-3-Clause

import importlib_resources as ir

# # import pyglet
# from matplotlib import font_manager
# from PIL import ImageFont


# def get_screen_size():
#     display = pyglet.canvas.Display()
#     screen = display.get_default_screen()
#     return screen.width, screen.height


class Config:
    def __init__(self):
        self.scoreboard_width = 200
        self.fps = 60
        self.resources = ir.files("tilthenightends") / "resources"
        self.scaling = 64.0 / 2.0
        self.hit_radius = 1.0
        # # self.avatar_size = (25, 25)
        # # file = font_manager.findfont("sans")
        # # self.large_font = ImageFont.truetype(file, size=16)
        # # self.medium_font = ImageFont.truetype(file, size=12)
        # # self.nx = 1920 - self.scoreboard_width
        # # self.ny = 1080
        # self.nx, self.ny = get_screen_size()
        # self.time_limit = 60 * 5
        # self.gravity = np.array([0, -1.62])  # m/s^2
        # self.thrust = np.abs(self.gravity[1]) * 3  # m/s^2
        # self.rotation_speed = 15.0
        # self.max_landing_speed = 5.0
        # self.max_landing_angle = 5.0
        # self.max_fuel = 1000
        # self.main_engine_burn_rate = 5
        # self.rotation_engine_burn_rate = 2
        # self.asteroid_delay = 5.0
        # self.asteroid_tip_size = 0.2
        # # self.crater_radius = self.avatar_size[0] // 2 - 1
        # # self.collision_radius = self.avatar_size[0] * 0.5 * np.sqrt(2)
        # self.twinkle_period = 4.0
        # self.nstars = 500
        # self.score_time_bonus = 5
        # self.score_fuel_bonus = 5
        # self.score_landing_site_bonus = 8
        # self.score_landing_bonus = 5
