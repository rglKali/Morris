from . import pytk as tk


class Window(tk.Window):
    width = 720
    height = 480
    fullscreen = False
    lang = 'EN'
    features = False
    if features:
        nickname = 'kali'
        color = tk.palette.orange

    def __init__(self):
        super().__init__(width=self.width, height=self.height, fullscreen=self.fullscreen)
        from .menu import Menu
        self.view = Menu()


def main():
    Window()
    tk.run()
