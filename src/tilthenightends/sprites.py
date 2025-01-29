# SPDX-License-Identifier: BSD-3-Clause

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class SpriteScatterPlotItem(pg.ScatterPlotItem):
    def __init__(
        self, sprite_path, scale=1.0, width=None, height=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Load the sprite and flip it vertically
        self.original_sprite = QtGui.QPixmap(str(sprite_path)).transformed(
            QtGui.QTransform().scale(1, -1)
        )

        # Determine scaling
        if width is not None and height is not None:
            self.sprite_size = QtCore.QSize(width, height)
        elif scale != 1.0:
            self.sprite_size = self.original_sprite.size() * scale
        else:
            self.sprite_size = self.original_sprite.size()

        # Scale the sprite to the desired size
        self.sprite = self.original_sprite.scaled(
            self.sprite_size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio
        )

    def paint(self, p, opt, widget):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        for i in range(len(self.data)):
            spot = self.data[i]
            x, y = spot[0], spot[1]
            # Draw the scaled sprite
            p.drawPixmap(
                QtCore.QPointF(
                    x - self.sprite_size.width() / 2,
                    y - self.sprite_size.height() / 2,
                ),
                self.sprite,
            )


def make_sprites(sprite_path, positions, **kwargs):
    spots = [{"pos": pos, "data": 1} for pos in positions]
    return SpriteScatterPlotItem(sprite_path, spots=spots, **kwargs)
