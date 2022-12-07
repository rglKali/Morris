from .objects import Window
from .menu import Menu
from .editor import Editor


def gui(engine, cfg):
    window = Window(engine, cfg)
    window.view = Menu(window)
    window.run()
