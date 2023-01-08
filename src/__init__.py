from . import pytk as tk
from .menu import Menu


class Window(tk.Window):
    width = 720
    height = 480
    lang = 'EN'
    features = True
    if features:
        nickname = 'kali'
        color = tk.palette.orange

    def __init__(self):
        super().__init__(width=self.width, height=self.height)
        self.view = Menu()


def main():
    win = Window()
    win.run()
