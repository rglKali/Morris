import time as tm

from . import pytk as tk


__all__ = ['Local']


class lang:
    create = {'EN': 'Create my lobby', 'FR': 'Créer mon lobby'}
    menu = {'EN': 'Return to menu', 'FR': 'Retourner au menu'}


class NetworkGame(tk.Sprite):
    def __init__(self):
        super().__init__()


class Games(tk.SpriteList):
    delta = 1.0

    def __init__(self):
        super().__init__()
        self.absolute = 0
        self.dynamic = 0
        self.length = 5
        self.last_update = tm.time()

    def draw(self):
        tk.draw_rect(x=180, y=240, width=340, height=460)
        tk.draw_text(x=180, y=240, text='Dev')
        super().draw()

    def update(self, filters):
        if tm.time() - self.last_update > self.delta:
            self.last_update = tm.time()
            # print('Scanned')


class Filters(tk.SpriteList):
    def __init__(self):
        super().__init__()

    def draw(self):
        tk.draw_rect(x=540, y=140, width=340, height=260, color=tk.palette.light_peach)
        tk.draw_text(x=540, y=140, text='Dev')
        super().draw()


class Create(tk.Button):
    def on_click(self):
        from .templates import Choice
        self.window.view = Choice()


class Return(tk.Button):
    def on_click(self):
        from .menu import Menu
        self.window.view = Menu()


class Local(tk.View):
    def __init__(self):
        super().__init__()
        self.games = Games()
        self.filters = Filters()
        self.new = Create(x=540, y=380, width=340, height=50, text=lang.create[self.window.lang], color=tk.palette.yellow)
        self.menu = Return(x=540, y=440, width=340, height=50, text=lang.menu[self.window.lang], color=tk.palette.red)

    def on_update(self, delta_time: float):
        self.games.update(self.filters)

    def on_draw(self):
        self.new.draw()
        self.menu.draw()
        self.games.draw()
        self.filters.draw()

    def on_mouse_press(self, x: int, y: int, key):
        self.new.click(x, y)
        self.menu.click(x, y)

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.menu.on_click()
        elif key == 'Return':
            self.new.on_click()
