import tkinter
import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .map_widget import TkinterMapView

from .utility_functions import decimal_to_osm, osm_to_decimal


class CanvasPoint:
    def __init__(self,
                 map_widget: "TkinterMapView",
                 position: tuple,
                 color: str = "#9B261E",
                 active_color: str = "C5542D",
                 scale: float = 1.0,
                 data: any = None):

        self.map_widget = map_widget
        self.position = position
        self.color = color
        self.active_color = active_color
        self.deleted = False
        self.data = data
        self.scale = scale

        self.circle = None

    def delete(self):
        if self in self.map_widget.canvas_point_list:
            self.map_widget.canvas_point_list.remove(self)

        self.map_widget.canvas.delete(self.circle)
        self.circle = None
        self.deleted = True
        self.map_widget.canvas.update()

    def set_position(self, deg_x, deg_y):
        self.position = (deg_x, deg_y)
        self.draw()

    def set_color(self, color):
        self.map_widget.canvas.itemconfigure(self.circle, outline=color)

    def get_canvas_pos(self, position):
        tile_position = decimal_to_osm(*position, round(self.map_widget.zoom))

        widget_tile_width = self.map_widget.lower_right_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]
        widget_tile_height = self.map_widget.lower_right_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]

        canvas_pos_x = ((tile_position[0] - self.map_widget.upper_left_tile_pos[0]) / widget_tile_width) * self.map_widget.width
        canvas_pos_y = ((tile_position[1] - self.map_widget.upper_left_tile_pos[1]) / widget_tile_height) * self.map_widget.height

        return canvas_pos_x, canvas_pos_y

    def draw(self, event=None):
        canvas_pos_x, canvas_pos_y = self.get_canvas_pos(self.position)

        if not self.deleted:
            if 0 - 50 < canvas_pos_x < self.map_widget.width + 50 and 0 < canvas_pos_y < self.map_widget.height + 70:

                if self.circle is None:
                    self.circle = self.map_widget.canvas.create_oval(canvas_pos_x - 5*self.scale, canvas_pos_y - 5*self.scale,
                                                                         canvas_pos_x + 5*self.scale, canvas_pos_y + 5*self.scale,
                                                                         activefill=self.active_color,
                                                                         fill=self.color, width=1, tag="point")
                else:
                    self.map_widget.canvas.coords(self.circle,
                                                  canvas_pos_x - 5*self.scale, canvas_pos_y - 5*self.scale,
                                                  canvas_pos_x + 5*self.scale, canvas_pos_y + 5*self.scale)

            else:
                self.map_widget.canvas.delete(self.circle)
                self.circle = None

            self.map_widget.manage_z_order()
