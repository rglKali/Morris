from . import pytk as tk
from .data import Board, Player


class Lobby(tk.View):
    def __init__(self, board: 'Board', host: 'Player' = None):
        super().__init__()

    def on_draw(self):
        tk.draw_text(360, 240, 'Lobby')
