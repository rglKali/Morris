import time as tm

from . import fltk as tk
from . import palette as pal
from .utils import text, wh


class NoViewInTheWindow(Exception):
    pass


class Window:
    def __init__(self, engine, cfg, bg: str = pal.LIGHT_PEACH):
        self.view = None
        self.active = True
        self.fps = list()
        self.bg = bg
        self.engine = engine

        # Manage Settings
        self.cfg = cfg.gui
        self.cfg.width = self.cfg.scale * 16 if not self.cfg.fullscreen else None
        self.cfg.height = self.cfg.scale * 9 if not self.cfg.fullscreen else None

    def update(self):
        ev = tk.donne_ev()
        if ev:
            if ev[0] == 'Quitte' or (ev[0] == 'Touche' and ev[1].keysym == 'Escape'):
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
        tk.cree_fenetre(self.cfg.width, self.cfg.height, fullscreen=self.cfg.fullscreen)
        self.cfg.width, self.cfg.height = wh()

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
        self.cfg = window.cfg

    def draw(self):
        pass

    def update(self, ev):
        pass


class Widget:
    def __init__(self, x: int, y: int, active: bool = True, parent=None):
        if parent:
            self.x, self.y = parent.x + x, parent.y + y
            parent.children.append(self)
        else:
            self.x, self.y = x, y
        self.active = active
        self.children = WidgetGroup()

    def activate(self):
        self.active = not self.active
        self.children.activate()

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


class Button(Widget):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color):
        super().__init__(x, y)

        self.text = text
        self.ax, self.ay, self.bx, self.by = x - width/2, y - height/2, x + width/2, y + height/2
        self.color = color

    def click(self):
        pass

    def draw(self):
        tk.rectangle(self.ax, self.ay, self.bx, self.by, '#000000', self.color)
        text(self.x, self.y, self.text, location='center')
