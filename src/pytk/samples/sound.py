from ... import pytk as tk


def action(obj):
    tk.play_sound()


class Window(tk.Window):
    def __init__(self):
        super().__init__()
        self.button = tk.Button(x=360, y=240, width=360, height=120, text='Sound!', action=action)

    def on_draw(self):
        self.button.draw()

    def on_mouse_press(self, x, y, key):
        self.button.click(x, y)


def sound():
    win = Window()
    tk.run()
