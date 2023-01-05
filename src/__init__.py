from . import pytk as tk
from .menu import Menu
# from .game import Game


class Window(tk.Window):
    width = 720
    height = 480
    fullscreen = False
    nickname = 'kali'

    def __init__(self):
        super().__init__(width=self.width, height=self.height, fullscreen=self.fullscreen)
        self.view = Menu()
    #
    # def quit(self):
    #     if self.view.__class__ == Game:
    #         self.view.socket.close()
    #     self.active = False


def main():
    Window()
    tk.run()
