from . import pytk as tk
from .data import Board, Player, Point


class Action(tk.Sprite):
    def __init__(self, order: int, player: 'Player', from_point: 'Point' = None, to_point: 'Point' = None):
        super().__init__()
        self.order = order
        if from_point is not None and to_point is not None:
            self.text = f'{player.name}, move badge: {from_point.name} -> {to_point.name}'
        elif from_point is not None:
            self.text = f'{player.name}, new badge: {to_point.name}'
        elif to_point is not None:
            self.text = f'{player.name}, remove badge: {from_point.name}'

    def draw(self):
        tk.draw_text(0, self.order, self.text, font_size=10, location='nw')


class History(tk.SpriteList):
    def __init__(self):
        super().__init__()

    def draw(self):
        tk.draw_rect(590, 240, 240, 460)
        super().draw()


class GPoint(tk.Sprite):
    def __init__(self, data: 'Point'):
        super().__init__()
        self.data = data


class GBoard(tk.SpriteList):
    def __init__(self, data: 'Board'):
        super().__init__()
        self.data = data
        self.delta = None

    def draw(self):
        pass


class Game(tk.View):
    def __init__(self, board: 'Board', players:list['Player'] = None):
        super().__init__()
        self.board = GBoard(board)
        if self.window.features:
            self.history = History()

    def on_draw(self):
        if self.window.features:
            self.history.draw()
