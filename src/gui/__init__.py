from . import fltk as tk
from . import palette as pl


class Game:
    def __init__(self):
        self.active = True

    def draw(self):
        tk.efface_tout()
        # Drawing the board
        tk.mise_a_jour()

    def update(self):
        ev = tk.donne_ev()
        if ev and ev[0] == 'Quitte':
            self.active = False

    def run(self):
        tk.cree_fenetre(640, 640)

        while self.active:
            self.draw()
            self.update()

        tk.ferme_fenetre()
