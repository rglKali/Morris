import time as tm
import random as rd
import dataclasses as dc
from typing import Optional

from .fltk import CustomCanvas, type_ev, touche, abscisse, ordonnee


__all__ = [
    # Data
    'palette',

    # Classes
    'Window',
    'View',
    'Sprite',
    'SpriteList',

    # Commands
    'get_random_color',
    'draw_line',
    'draw_circle',
    'draw_rect',
    'draw_text',
    'hitbox_rect',
    'hitbox_circle',
    'run'
]


_window: Optional['Window'] = None


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
    dev_width = 720
    dev_height = 480
    font_name = 'JetBrains Mono'
    font_size = 20
    outline = 5

    def __init__(self, width: int = dev_width, height: int = dev_height,
                 fullscreen: bool = False, bg: str = palette.white, refresh_rate: int = 120):
        super().__init__(width, height, refresh_rate)
        self.bg = bg

        self.dx = float()
        self.dy = float()
        self.resize(width, height, fullscreen)

        self.active = True
        self.view = None
        set_window(self)

    def resize(self, width: int = None, height: int = None, fullscreen: bool = None):
        self.root.attributes('-fullscreen', fullscreen)

        if fullscreen:
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()

        self.canvas.config(width=width, height=height)
        self.dx = width / self.dev_width
        self.dy = height / self.dev_height

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
    def __init__(self, x: int = None, y: int = None, hitbox: list = None):
        self.window = get_window()
        self.x, self.y = x, y
        self.hitbox = set()
        if hitbox:
            [self.hitbox.add((self.x + i, self.y + j)) for i, j in hitbox]

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
        self.window = get_window()

    def update(self, *args):
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


def get_random_color(colors: list[str] = None):
    if colors:
        return rd.choice(colors)
    else:
        return rd.choice([color for color in vars(palette).values() if isinstance(color, str) and color[0] == '#'])


def hitbox_circle(radius: int):
    hitbox = set()
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 <= radius ** 2:
                hitbox.add((x, y))
    return hitbox


def hitbox_rect(width: int, height: int):
    hitbox = set()
    for w in range(-(width//2), (width//2) + 1):
        for h in range(-(height//2), (height//2) + 1):
            hitbox.add((w, h))
    return hitbox


def draw_line(ax: int, ay: int, bx: int, by: int,
              color: str = palette.black, thickness: int = None):
    w = get_window()
    if thickness is None:
        thickness = w.outline
    w.canvas.create_line(ax * w.dx, ay * w.dy, bx * w.dx, by * w.dy, fill=color, width=thickness * min(w.dx, w.dy))


def draw_circle(x: int, y: int, radius: int, color: str = get_random_color(),
                outline: str = palette.black, thickness: int = None):
    w = get_window()
    if thickness is None:
        thickness = w.outline
    w.canvas.create_oval((x - radius) * w.dx, (y - radius) * w.dy, (x + radius) * w.dx, (y + radius) * w.dy,
                         fill=color, outline=outline, width=thickness * min(w.dx, w.dy))


def draw_rect(x: int, y: int, width: int, height: int, color: str = palette.light_grey,
              outline: str = palette.black, thickness: int = None):
    w = get_window()
    if thickness is None:
        thickness = w.outline
    w.canvas.create_rectangle((x - width//2) * w.dx, (y - height//2) * w.dy,
                              (x + width//2) * w.dx, (y + height//2) * w.dy,
                              fill=color, outline=outline, width=thickness * min(w.dx, w.dy))


def draw_text(x: int, y: int, text: str, font_name: str = None, font_size: int = None,
              color: str = palette.black, location: str = 'center'):
    w = get_window()
    if font_name is None:
        font_name = w.font_name
    if font_size is None:
        font_size = w.font_size
    w.canvas.create_text(x * w.dx, y * w.dy, text=text, font=(font_name, round(font_size * min(w.dx, w.dy))),
                         fill=color, anchor=location)


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
                    w.view.on_key_press(key)

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
