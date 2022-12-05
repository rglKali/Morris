from . import fltk as tk
from . import palette as pl
from .objects import Window, View
from .editor import Editor


class Menu(View):
    def __init__(self, window):
        super().__init__(window)
        self.board = self.window.engine.board

    def draw(self):
        tk.rectangle(0, 0, self.board.size * 50, self.board.size * 50)

    def update(self, ev):
        if ev[0] == 'ClicGauche':
            self.window.view = Settings(self.window)
        if ev[0] == 'Touche':
            self.window.view = Editor(self.window)


class Settings(View):
    def __init__(self, window):
        super().__init__(window)
        self.circles = list()

    def draw(self):
        [tk.cercle(x, y, 10) for x, y in self.circles]

    def update(self, ev):
        print(ev)
        if ev[0] == 'ClicDroit':
            self.window.view = Menu(self.window)

        elif ev[0] == 'ClicGauche':
            self.circles.append([ev[1].x, ev[1].y])

