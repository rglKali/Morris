import time as tm
import random as rd
import dataclasses as dc
from typing import Optional

from .fltk import CustomCanvas, type_ev, touche, abscisse, ordonnee


__all__ = [
    # Data
    'config',
    'palette',
    # Classes
    'Window',
    'View',
    'Sprite',
    'SpriteList',
    # Commands
    # 'get_window', Not sure, it would be useful, but it gives the possibility to get the current window
    'run',
    'get_random_color',
    'draw_line',
    'draw_circle',
    'draw_rect',
    'draw_text',
    'hitbox_rect',
    'hitbox_circle'
]
__version__ = 1.1
__license__ = 'MIT'

"""
pytk is a package created by rglKali on top of the fltk library to turn it into an OOP library
"""


_window: Optional['Window'] = None


@dc.dataclass
class config:
    dev_width = 720
    dev_height = 480
    font_name = 'JetBrains Mono'
    font_size = 20
    outline = 5


@dc.dataclass
class palette:
    black = "#000000"
    dark_blue = "#1D2B53"
    dark_purple = "#7E2553"
    dark_green = "#008751"
    brown = "#AB5236"
    dark_grey = "#5F574F"
    light_grey = "#C2C3C7"
    white = "#FFF1E8"
    red = "#FF004D"
    orange = "#FFA300"
    yellow = "#FFEC27"
    green = "#00E436"
    blue = "#29ADFF"
    lavender = "#83769C"
    pink = "#FF77A8"
    light_peach = "#FFCCAA"


# Classes
class Window(CustomCanvas):
    def __init__(self, width: int = config.dev_width, height: int = config.dev_height,
                 fullscreen: bool = False, bg: str = palette.white, refresh_rate: int = 120):
        super().__init__(width, height, refresh_rate)
        self.bg = bg
        if fullscreen:
            self.root.attributes('-fullscreen', True)
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.canvas.config(width=width, height=height)
        self.dx = width / config.dev_width
        self.dy = height / config.dev_height

        self.active = True
        self.view = None
        set_window(self)

    def draw_bg(self):
        draw_rect(360, 240, 720, 480, self.bg, thickness=0)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key):
        pass

    def on_mouse_press(self, x, y, key):
        pass

    def quit(self):
        self.active = False


class View:
    def __init__(self):
        self.window = get_window()
        self.bg = self.window.bg

    def draw_bg(self):
        draw_rect(360, 240, 720, 480, self.bg, thickness=0)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key: str):
        pass

    def on_mouse_press(self, x: int, y: int, key):
        pass


class Sprite:
    def __init__(self, x: int, y: int, hitbox: list = None):
        self.window = get_window()
        self.x, self.y = x, y
        if hitbox:
            self.hitbox = [(self.x + i, self.y + j) for i, j in hitbox]
        else:
            self.hitbox = [(self.x, self.y)]

    def update(self):
        pass

    def draw(self):
        pass

    def collides_with_point(self, x: int, y: int):
        if (x, y) in self.hitbox:
            return True
        else:
            return False


class SpriteList(list):
    def __init__(self, *sprites):
        super().__init__(sprites)

    def update(self):
        [sprite.update() for sprite in self]

    def draw(self):
        [sprite.draw() for sprite in self]


# Commands
def get_window() -> 'Window':
    if _window is None:
        raise RuntimeError(
            (
                'No window is active'
            )
        )
    return _window


def set_window(window) -> None:
    global _window
    _window = window


def run():
    w = get_window()
    fps = list()
    while w.active:
        start = tm.time()
        if len(w.ev_queue):
            ev = w.ev_queue.popleft()
            if type_ev(ev) == 'Quitte':
                w.quit()
            elif type_ev(ev) == 'Touche':
                key = touche(ev)
                w.on_key_press(key)
                if w.view:
                    w.on_key_press(key)
            elif type_ev(ev) == 'ClicGauche':
                x = round(abscisse(ev) / w.dx)
                y = round(ordonnee(ev) / w.dy)
                w.on_mouse_press(x, y, key='Left')
                if w.view:
                    w.view.on_mouse_press(x, y, key='Left')
            elif type_ev(ev) == 'ClicDroit':
                x = round(abscisse(ev) / w.dx)
                y = round(ordonnee(ev) / w.dy)
                w.on_mouse_press(x, y, key='Right')
                if w.view:
                    w.view.on_mouse_press(x, y, key='Right')

        w.on_update(tm.time() - w.last_update)
        if w.view:
            w.view.on_update(tm.time() - w.last_update)

        w.canvas.delete('all')

        w.draw_bg()
        w.on_draw()
        if w.view:
            w.view.draw_bg()
            w.view.on_draw()

        w.root.update()
        tm.sleep(max(0., w.interval - (tm.time() - w.last_update)))
        w.last_update = tm.time()

        if not w.active:
            w.root.destroy()
            set_window(None)

        end = tm.time()
        fps.append(end - start)

    print(f'Average FPS: {round(len(fps)/sum(fps), 2)}')


def get_random_color(colors: list[str] = None):
    if colors:
        return rd.choice(colors)
    else:
        return rd.choice([color for color in vars(palette).values() if isinstance(color, str) and color[0] == '#'])


def hitbox_circle(radius: int):
    hitbox = list()
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 <= radius ** 2 and (x, y) not in hitbox:
                hitbox.append((x, y))
    return hitbox


def hitbox_rect(width: int, height: int):
    hitbox = list()
    for w in range(-(width//2), (width//2) + 1):
        for h in range(-(height//2), (height//2) + 1):
            hitbox.append((w, h))
    return hitbox


def draw_line(ax: int, ay: int, bx: int, by: int,
              color: str = palette.black, thickness: int = config.outline):
    w = get_window()
    w.canvas.create_line(ax * w.dx, ay * w.dy, bx * w.dx, by * w.dy, fill=color, width=thickness * min(w.dx, w.dy))


def draw_circle(x: int, y: int, radius: int, color: str = get_random_color(),
                outline: str = palette.black, thickness: int = config.outline):
    w = get_window()
    w.canvas.create_oval((x - radius) * w.dx, (y - radius) * w.dy, (x + radius) * w.dx, (y + radius) * w.dy,
                         fill=color, outline=outline, width=thickness * min(w.dx, w.dy))


def draw_rect(x: int, y: int, width: int, height: int, color: str = palette.light_grey,
              outline: str = palette.black, thickness: int = config.outline):
    w = get_window()
    w.canvas.create_rectangle((x - width//2) * w.dx, (y - height//2) * w.dy,
                              (x + width//2) * w.dx, (y + height//2) * w.dy,
                              fill=color, outline=outline, width=thickness * min(w.dx, w.dy))


def draw_text(x: int, y: int, text: str, font_name: str = config.font_name, font_size: int = config.font_size,
              color: str = palette.black, location: str = 'center'):
    w = get_window()
    w.canvas.create_text(x * w.dx, y * w.dy, text=text, font=(font_name, round(font_size * min(w.dx, w.dy))),
                         fill=color, anchor=location)
