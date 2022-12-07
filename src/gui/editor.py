import json

from . import fltk as tk

from .settings import settings as cfg
from .utils import text
from .objects import View, Input, Button, WidgetGroup, Point


class Editor(View):
    def __init__(self, window):
        super().__init__(window)
        self.screen = int()

        self.name = None
        self.size = None
        self.points = None
        self.connects = None
        self.pieces = None
        self.unite = None
        self.skip = None
        self.point = None
        self.buttons = WidgetGroup()

        self.new_screen(1)

    def new_screen(self, screen):
        if screen == 1:
            if not self.name:
                self.name = Input(230, 50, selected=True)
            else:
                self.name.activate()
            if not self.size:
                self.size = Input(230, 100, length=1, chars='3579')
            else:
                self.size.activate()

            if self.points or self.connects:
                self.points.activate()
                self.connects.activate()

        elif screen == 2:
            if not self.points:
                self.points = WidgetGroup()
                [self.points.extend([Point(x*100 + 50, y*100 + 50, active=True) for x in range(int(
                    self.size))]) for y in range(int(self.size))]
            else:
                self.points.activate()
            if not self.connects:
                self.connects = WidgetGroup()
            else:
                self.connects = WidgetGroup()

            if self.name.active or self.size.active:
                self.name.activate()
                self.size.activate()

            elif self.pieces.active or self.unite.active or self.skip.active:
                self.pieces.activate()
                self.unite.activate()
                self.skip.activate()

        elif screen == 3:
            pass

        self.screen = screen

    def update(self, ev):
        if self.screen == 1:
            if ev[0] == 'Touche':
                key = ev[1].keysym

                if (key == 'Down' and self.name.selected) or (key == 'Up' and self.size.selected):
                    self.name.select()
                    self.size.select()
                elif key == 'Return' and bool(self.name) and bool(self.size):
                    self.new_screen(2)

                elif self.name.selected:
                    self.name.update(key)
                elif self.size.selected:
                    self.size.update(key)

        elif self.screen == 2:
            x, y = ev[1].x, ev[1].y
            if ev[0] == 'ClicGauche':
                for point in self.points:
                    if (x - point.x) * (x - point.x) + (y - point.y) * (y - point.y) < point.radius * point.radius:
                        point.exists = not point.exists
            elif ev[0] == 'ClicDroite':
                for point in self.points:
                    if (x - point.x) * (x - point.x) + (y - point.y) * (y - point.y) < point.radius * point.radius:
                        if self.point:
                            self.connects.append()
                            self.point = None
                        else:
                            self.point = point

        elif self.screen == 3:
            pass

    def draw(self):
        if self.screen == 1:
            text(50, 50, 'Board name: ')
            text(50, 100, 'Board size: ')
            self.name.draw()
            self.size.draw()

        elif self.screen == 2:
            self.points.draw()

        elif self.screen == 3:
            pass
