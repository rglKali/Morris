import time as tm

from . import fltk as tk
from . import palette as pal
from .utils import text


class NoViewInTheWindow(Exception):
    pass


class InputError(Exception):
    pass


class Window:
    def __init__(self, engine, cfg, bg: str = pal.LIGHT_PEACH):
        self.view = None
        self.active = True
        self.fps = list()
        self.bg = bg
        self.engine = engine
        self.cfg = cfg.gui

    def update(self):
        ev = tk.donne_ev()
        if ev:
            if ev[0] == 'Quitte':
                self.active = False

            elif self.view:
                self.view.update(ev)

            else:
                raise NoViewInTheWindow

    def draw(self):
        tk.efface_tout()
        # Background
        tk.rectangle(0, 0, self.cfg.width, self.cfg.height, self.bg, self.bg)

        if self.view:
            self.view.draw()
        else:
            raise NoViewInTheWindow

        tk.mise_a_jour()

    def run(self):
        tk.cree_fenetre(self.cfg.width, self.cfg.height)

        while self.active:
            start = tm.time()
            self.update()
            self.draw()
            end = tm.time()
            self.fps.append(end - start)
            # print(f'Current FPS: {1 / self.fps[-1]}')

        tk.ferme_fenetre()
        print(f'Average FPS: {len(self.fps) / sum(self.fps)}')


class View:
    def __init__(self, window, *args):
        self.window = window
        self.engine = window.engine

    def draw(self):
        pass

    def update(self, ev):
        pass


class Widget:
    def __init__(self, x: any([float, int]), y: any([float, int]), active: bool = True, *args):
        self.x, self.y = x, y
        self.active = active

    def activate(self):
        self.active = not self.active

    def update(self, *args):
        pass

    def draw(self, *args):
        pass


class WidgetGroup(list):
    def __init__(self, *widgets):
        super().__init__()
        self.extend(widgets)
        [print(widget.w, widget.y) for widget in self]
        self.active = True

    def __bool__(self):
        return True

    def activate(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            [widget.draw() for widget in self]

    def update(self):
        pass


class Input(Widget):
    def __init__(self, x: any([int, float]), y: any([int, float]), active: bool = True,
                 length: int = None, spaces: bool = True, selected: bool = False,
                 chars: str = 'azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890'):
        super().__init__(x, y, active)
        self.data = str()
        self.selector = int()
        self.length = length
        self.spaces = spaces
        self.selected = selected
        self.chars = chars

    def __str__(self):
        if len(self.data) != 0:
            return self.data
        else:
            raise InputError

    def __int__(self):
        if self.data.isnumeric():
            return int(self.data)
        else:
            raise InputError

    def __bool__(self):
        return bool(len(self.data))

    def select(self):
        self.selected = not self.selected

    def update(self, key):
        if key == 'Left' and self.selector > 0:
            self.selector -= 1
        elif key == 'Right' and self.selector < len(self.data):
            self.selector += 1
        elif key == 'BackSpace' and len(self.data) > 0:
            self.data = self.data[:-1]
        elif key in self.chars and (not self.length or len(self.data) < self.length):
            self.data = self.data[:self.selector] + key + self.data[self.selector:]
            self.selector += 1
        elif key == 'space' and self.spaces:
            self.data = self.data[:self.selector] + ' ' + self.data[self.selector:]
            self.selector += 1

    def draw(self):
        if self.active:
            if round(tm.time()) % 2 and self.selected:
                text(self.x, self.y, self.data[:self.selector] + '|' + self.data[self.selector:])
            elif self.selected:
                text(self.x, self.y, self.data[:self.selector] + ' ' + self.data[self.selector:])
            else:
                text(self.x, self.y, self.data)


class CheckBox(Widget):
    def __init__(self, x: any([int, float]), y: any([int, float]), active: bool = True,
                 state: any([bool, None]) = None, size: any([int, float]) = 10):
        super().__init__(x, y, active)
        self.state = state
        self.size = size

    def __bool__(self):
        if type(self.state) is bool:
            return self.state
        else:
            raise InputError

    def select(self):
        if type(self.state) is bool:
            self.state = not self.state
        else:
            self.state = True

    def draw(self):
        if self.active:
            tk.rectangle(self.x, self.y, self.x + self.size, self.y + self.size)
            if self.state is True:
                tk.ligne(self.x, self.y + self.size/2, self.x + self.size/2, self.y + self.size)
                tk.ligne(self.x + self.size/2, self.y + self.size, self.x + self.size, self.y)
            elif self.state is False:
                tk.ligne(self.x, self.y, self.x + self.size, self.y + self.size)
                tk.ligne(self.x + self.size, self.y, self.x, self.y + self.size)


class Button(Widget):
    def __init__(self, x1: any([int, float]), y1: any([int, float]), x2: any([int, float]), y2: any([int, float]),
                 active: bool = True, text: str = '', color: str = pal.GREEN):
        super().__init__([(x1 + x2) / 2, (y1 + y2) / 2], active)
        self.text = text
        self.color = color
        self.hitbox = [range(min(x1, x2), max(x1, x2)), range(min(y1, y2), max(y1, y2))]

    def __str__(self):
        return self.text

    def draw(self):
        if self.active:
            tk.rectangle(self.hitbox[0][0], self.hitbox[0][-1], self.hitbox[-1][0], self.hitbox[-1][-1])
            text(self.x, self.y, self.text, location='center')


class Point(Widget):
    def __init__(self, x: any([int, float]), y: any([int, float]), radius: int, active: bool = True):
        super().__init__(x, y, active)
        self.exists = False
        self.radius = radius

    def update(self):
        pass

    def draw(self):
        if self.active:
            if self.exists:
                tk.cercle(self.x, self.y, self.radius, remplissage=pal.DARK_GREY)
            else:
                tk.cercle(self.x, self.y, self.radius, remplissage=pal.LIGHT_GREY)
