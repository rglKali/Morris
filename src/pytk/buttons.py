from time import time
import string

from .core import Sprite
from .data import palette, config
from .draw import draw_rect, draw_text, draw_text_flex, draw_line
from .hitbox import hitbox_rect


__all__ = [
    'Button',
    'CheckBox',
    'InputField',
    # 'Slider'        # May cause issues, still in development
]


class Button(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, text: str = str(),
                 color: str = palette.white, flex: bool = True):
        super().__init__(x, y, hitbox=hitbox_rect(width, height))
        self.color = color
        self.width = width
        self.height = height
        self.text = text
        self.flex = flex

    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=config.outline_thickness)
        if self.flex:
            draw_text_flex(self.x, self.y, self.text, self.width, self.height)
        else:
            draw_text(self.x, self.y, self.text)

    def click(self, x: int, y: int):
        if self.collides_with_point(x, y):
            self.on_click()
            return True
        else:
            return False

    def on_click(self):
        pass


class CheckBox(Sprite):
    def __init__(self, x: int, y: int, size: int, color: str = palette.white, default: bool = None):
        super().__init__(x, y, hitbox=hitbox_rect(size, size))
        self.color = color
        self.size = size
        self.value = default

    def __bool__(self):
        return not not self.value

    def draw(self):
        draw_rect(self.x, self.y, self.size, self.size, color=self.color, thickness=config.outline_thickness)

        if self.value is None:
            return

        if self.value:
            draw_line(self.x - self.size // 2, self.y,
                      self.x, self.y + self.size // 2,
                      thickness=config.outline_thickness)
            draw_line(self.x, self.y + self.size // 2,
                      self.x + self.size // 2, self.y - self.size // 2,
                      thickness=config.outline_thickness)
        else:
            draw_line(self.x - self.size // 2, self.y - self.size // 2,
                      self.x + self.size // 2, self.y + self.size // 2,
                      thickness=config.outline_thickness)
            draw_line(self.x + self.size // 2, self.y - self.size // 2,
                      self.x - self.size // 2, self.y + self.size // 2,
                      thickness=config.outline_thickness)

    def click(self, x: int, y: int):
        if (x, y) in self.hitbox:
            self.value = not self.value


class InputField(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: str = palette.white,
                 allowed_chars: str = string.printable,
                 max_length: int = 12, default: str = str()):
        super().__init__(x, y, hitbox=hitbox_rect(width, height))
        self.color = color
        self.width = width
        self.height = height
        self.text = text
        self.value = default
        self.chars = allowed_chars
        self.length = max_length
        self.selected = False
        self.selector = len(self)

    def __len__(self):
        return len(self.value)

    def __int__(self):
        if self.value.isnumeric():
            return int(self.value)
        else:
            return 0

    def __str__(self):
        return self.value

    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=config.outline_thickness)
        if not self.selected:
            draw_text(self.x, self.y, self.text + self.value)
        else:
            if int(time()) % 2:
                text = self.value[:self.selector] + '|' + self.value[self.selector:]
            else:
                text = self.value[:self.selector] + ' ' + self.value[self.selector:]
            draw_text(self.x, self.y, self.text + text)

    def click(self, x: int, y: int):
        if self.collides_with_point(x, y):
            self.selected = True
        else:
            self.selected = False

    def move_selector_right(self):
        if self.selected and self.selector < len(self.value):
            self.selector += 1

    def move_selector_left(self):
        if self.selected and self.selector > 0:
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

        if self.selected and char in self.chars and len(self.value) < self.length and \
                self.selector < len(self.value) + 1:
            lst = list(self.value)
            lst.insert(self.selector, char)
            self.value = ''.join(lst)
            self.selector += 1


class Slider(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, values: list):
        super().__init__(x, y, hitbox=hitbox_rect(width, height))
        self.width = width
        self.height = height
        self.values = values
        self.selected = True
        self.selector = 0

    def __float__(self):
        return self.values[self.selector]

    def move_right(self):
        if self.selected and self.selector < len(self.values) - 1:
            self.selector += 1

    def move_left(self):
        if self.selected and self.selector > 0:
            self.selector -= 1

    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height)
        draw_line(round(self.x - self.width * 0.4), self.y, round(self.x + self.width * 0.4), self.y)
        draw_rect(self.x + round(self.selector * self.width * 0.1), self.y,
                  round(self.width * 0.1), round(self.height * 0.7))
