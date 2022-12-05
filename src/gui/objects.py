from . import fltk as tk
from . import palette as pal
from ..engine import Engine


class NoViewInTheWindow(Exception):
    pass


class Window:
    def __init__(self, width: int, height: int, bg: str = pal.LIGHT_PEACH):
        self.view = None
        self.active = True
        self.width, self.height = width, height
        self.bg = bg
        self.engine = Engine()
        self.engine.open_board('Classic')

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
        tk.rectangle(0, 0, self.width, self.height, self.bg, self.bg)

        if self.view:
            self.view.draw()
        else:
            raise NoViewInTheWindow

        tk.mise_a_jour()

    def run(self):
        tk.cree_fenetre(self.width, self.height)

        while self.active:
            self.update()
            self.draw()

        tk.ferme_fenetre()


class View:
    def __init__(self, window, *args):
        self.window = window

    def draw(self):
        pass

    def update(self, ev):
        pass
