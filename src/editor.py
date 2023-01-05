import string

from . import pytk as tk
from .data import Board, Point


class Size(tk.SpriteList):
    def __init__(self):
        super().__init__()
        self.y = 125
        self.value = None

        for ind, value in enumerate([3, 5, 7, 9]):
            self.append(tk.Button(x=150 + ind * 50, y=self.y, width=50, height=50,
                                  color=tk.palette.light_peach, text=str(value)))

    def __int__(self):
        return self.value

    def draw(self):
        tk.draw_rect(180, self.y, 320, 70)
        tk.draw_text(80, self.y, 'Size')
        super().draw()

    def click(self, x, y):
        for button in self:
            if button.collides_with_point(x, y):
                for b in self:
                    b.color = tk.palette.light_peach
                self.value = int(button.text)
                button.color = tk.palette.yellow
                return True
        return False


class Unite(tk.CheckBox):
    def __init__(self):
        super().__init__(140, 275, 50, color=tk.palette.light_peach)

    def draw(self):
        tk.draw_rect(100, self.y, 160, 70)
        tk.draw_text(70, self.y, 'Unite')
        super().draw()

    def click(self, x, y):
        super().click(x, y)
        if self.collides_with_point(x, y):
            if self.value:
                self.color = tk.palette.yellow
            else:
                self.color = tk.palette.red


class Skip(tk.CheckBox):
    def __init__(self):
        super().__init__(300, 275, 50, color=tk.palette.light_peach)

    def draw(self):
        tk.draw_rect(260, self.y, 160, 70)
        tk.draw_text(230, self.y, 'Skip')
        super().draw()

    def click(self, x, y):
        super().click(x, y)
        if self.collides_with_point(x, y):
            if self.value:
                self.color = tk.palette.yellow
            else:
                self.color = tk.palette.red


class Confirm(tk.Button):
    pass


class Return(tk.Button):
    def on_click(self):
        from .templates import Choice
        self.window.view = Choice()


class Editor(tk.View):
    def __init__(self):
        super().__init__()
        self.name = tk.InputField(x=180, y=50, width=320, height=50, text='Name: ',
                                  max_length=12, color=tk.palette.light_peach)
        self.size = Size()
        self.pieces = tk.InputField(x=180, y=200, width=320, height=50, text='Pieces amount: ', max_length=2,
                                    color=tk.palette.light_peach, allowed_chars=string.digits)
        self.unite = Unite()
        self.skip = Skip()

        self.templates = Return(x=180, y=440, width=320, height=50, text='Return to templates', color=tk.palette.red)

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.templates.on_click()
        elif key == 'Left':
            self.name.move_selector_left()
        elif key == 'Right':
            self.name.move_selector_right()
        elif key == 'BackSpace':
            self.name.remove_char()
            self.pieces.remove_char()
        else:
            self.name.add_char(key)
            self.pieces.add_char(key)

    def on_mouse_press(self, x: int, y: int, key):
        self.name.click(x, y)
        self.size.click(x, y)
        self.pieces.click(x, y)
        self.unite.click(x, y)
        self.skip.click(x, y)
        self.templates.click(x, y)

    def on_draw(self):
        self.name.draw()
        self.size.draw()
        self.pieces.draw()
        self.unite.draw()
        self.skip.draw()
        self.templates.draw()
