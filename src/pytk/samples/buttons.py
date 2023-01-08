from ... import pytk as tk


class ColorfulButton(tk.Button):
    def __init__(self):
        super().__init__(360, 360, width=200, height=50, text='Click!!')

    def on_click(self):
        self.color = tk.palette.random()


class Win(tk.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.input = tk.InputField(360, 240, width=400, height=50, text='Name: ')
        self.checkbox = tk.CheckBox(360, 120, size=50)
        self.button = ColorfulButton()

    def on_draw(self):
        self.input.draw()
        self.checkbox.draw()
        self.button.draw()

    def on_key_press(self, key):
        if key == 'Left':
            self.input.move_selector_left()
        elif key == 'Right':
            self.input.move_selector_right()
        elif key == 'BackSpace':
            self.input.remove_char()
        else:
            self.input.add_char(key)

    def on_mouse_press(self, x: int, y: int, key: str):
        self.input.click(x, y)
        self.checkbox.click(x, y)
        self.button.click(x, y)


def buttons():
    win = Win(720, 480)
    win.run()
