from . import pytk as tk
from .menu import Menu


class Window(tk.Window):
    width = 720
    height = 480
    fullscreen = False
    nickname = 'kali'
    lang = 'EN'
    features = False

    def __init__(self):
        super().__init__(width=self.width, height=self.height, fullscreen=self.fullscreen)
        self.view = Menu()


def main():
    Window()
    tk.run()
