from . import fltk as tk
from .objects import View
from .editor import Editor


class Menu(View):
    def __init__(self, window):
        super().__init__(window)

    def draw(self):
        pass

    def update(self, ev):
        if ev[0] == 'Touche' and ev[1].keysym == 'e':
            self.window.view = Editor(self.window)
