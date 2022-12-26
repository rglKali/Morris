from time import time

from .. import pytk as tk
from .... import cfg


__all__ = [
    'Button',
    'CheckBox',
    'InputField'
]


class Button(tk.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: str = cfg.gui.palette.white):
        super().__init__(x, y, hitbox=tk.hitbox_rect(width, height))
        self.color = color
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        tk.draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=2)
        tk.draw_text(self.x, self.y, self.text)

    def click(self, x: int, y: int):
        if (x, y) in self.hitbox:
            self.on_click()

    def on_click(self):
        # Here should be some action
        pass


class CheckBox(tk.Sprite):
    def __init__(self, x: int, y: int, size: int, color: str = cfg.gui.palette.white):
        super().__init__(x, y, hitbox=tk.hitbox_rect(size, size))
        self.color = color
        self.size = size
        self.value = None

    def __bool__(self):
        return not not self.value

    def draw(self):
        tk.draw_rect(self.x, self.y, self.size, self.size, color=self.color, thickness=2)

        if self.value is None:
            return

        if self.value:
            tk.draw_line(self.x - self.size // 2, self.y,
                         self.x, self.y + self.size // 2,
                         thickness=2)
            tk.draw_line(self.x, self.y + self.size // 2,
                         self.x + self.size // 2, self.y - self.size // 2,
                         thickness=3)
        else:
            tk.draw_line(self.x - self.size // 2, self.y - self.size // 2,
                         self.x + self.size // 2, self.y + self.size // 2,
                         thickness=2)
            tk.draw_line(self.x + self.size // 2, self.y - self.size // 2,
                         self.x - self.size // 2, self.y + self.size // 2,
                         thickness=2)

    def click(self, x: int, y: int):
        if (x, y) in self.hitbox:
            self.value = not self.value


class InputField(tk.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: str = cfg.gui.palette.white,
                 allowed_chars: str = ' azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN', max_length: int = 12):
        super().__init__(x, y, hitbox=tk.hitbox_rect(width, height))
        self.color = color
        self.width = width
        self.height = height
        self.text = text
        self.value = str()
        self.chars = allowed_chars
        self.length = max_length
        self.selected = False
        self.selector = int()

    def __str__(self):
        return self.value

    def draw(self):
        tk.draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=2)
        if not self.selected:
            tk.draw_text(self.x, self.y, self.text + self.value)
        else:
            if int(time()) % 2:
                text = self.value[:self.selector] + '|' + self.value[self.selector:]
            else:
                text = self.value[:self.selector] + ' ' + self.value[self.selector:]
            tk.draw_text(self.x, self.y, self.text + text)

    def click(self, x: int, y: int):
        if (x, y) in self.hitbox:
            self.selected = True
        else:
            self.selected = False

    def move_selector_right(self):
        self.selector += 1

    def move_selector_left(self):
        self.selector -= 1

    def remove_char(self):
        if self.selected and self.selector > 0:
            lst = list(self.value)
            lst.pop(self.selector - 1)
            self.value = ''.join(lst)
            self.selector -= 1

    def add_char(self, char: str):
        if char == 'space':
            char = ' '

        if self.selected and char in self.chars and len(self.value) < self.length and self.selector < len(self.value) + 1:
            lst = list(self.value)
            lst.insert(self.selector, char)
            self.value = ''.join(lst)
            self.selector += 1
