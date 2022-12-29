from . import pytk as tk


class Window(tk.Window):
    def __init__(self):
        super().__init__(width=720, height=480)

    def on_mouse_press(self, x, y, key):
        print(x, y, key)

    def on_key_press(self, key):
        print(key)


def run():
    # win = Window()
    # tk.run()
    tk.samples.buttons()
