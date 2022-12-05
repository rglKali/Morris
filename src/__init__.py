from .gui import Window, Menu


def main():
    window = Window(width=640, height=640)
    window.view = Menu(window)
    window.run()
