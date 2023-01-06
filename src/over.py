from . import pytk as tk


class Over(tk.View):
    def __init__(self, winner):
        super().__init__()
        self.winner = winner

    def on_draw(self):
        tk.draw_text(360, 240, f'Game Over!\n{self.winner.data.name} won!\nPress any key to return to menu')

    def on_key_press(self, key: str):
        from .menu import Menu
        self.window.view = Menu()

    def on_mouse_press(self, x: int, y: int, key):
        from .menu import Menu
        self.window.view = Menu()
