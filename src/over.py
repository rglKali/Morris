from . import pytk as tk

__all__ = ['Over']


class lang:
    gm = {'EN': 'Game Over!', 'FR': 'Fin de partie!'}
    win = {'EN': 'wins', 'FR': 'victoire'}
    ret = {'EN': 'Press any key to return to menu', 'FR': 'Appuyer sur n\'importe quelle touche \npour retourner au menu'}


class Over(tk.View):
    def __init__(self, winner):
        super().__init__()
        self.winner = winner

    def on_draw(self):
        tk.draw_text(360, 240, f'{lang.gm[self.window.lang]}\n{self.winner.data.name} {lang.win[self.window.lang]}\n'
                               f'{lang.ret[self.window.lang]}')

    def on_key_press(self, key: str):
        from .menu import Menu
        self.window.view = Menu()

    def on_mouse_press(self, x: int, y: int, key):
        from .menu import Menu
        self.window.view = Menu()
