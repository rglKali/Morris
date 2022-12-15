from .fltk import CustomCanvas, type_ev, touche, abscisse, ordonnee
import time as tm
import random as rd
from ... import cfg
from typing import Optional


__all__ = [
    # Classes
    'Window',
    'View',
    'Sprite',
    'SpriteList',
    # Commands
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

"""
pytk is a package created by rglKali on top of the fltk library to turn it into an OOP library
"""


_window: Optional['Window'] = None


# Classes
class Window(CustomCanvas):
    def __init__(self, width: int = cfg.gui.width, height: int = cfg.gui.height,
                 fullscreen: bool = cfg.gui.fullscreen, offset: list[int] = (0, 0), refresh_rate: int = 120):
        super().__init__(width, height, refresh_rate)
        self.ox, self.oy = offset
        if fullscreen:
            self.root.attributes('-fullscreen', True)
            self.width = self.root.winfo_screenwidth()
            self.height = self.root.winfo_screenheight()

        self.active = True
        self.view = None
        set_window(self)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key):
        pass

    def on_mouse_press(self, x, y):
        pass

    def quit(self):
        self.active = False


class View:
    def __init__(self):
        self.window = get_window()

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key: str):
        pass

    def on_mouse_press(self, x: int, y: int):
        pass


class Sprite:
    def __init__(self, x: int, y: int, hitbox: list = None):
        self.window = get_window()
        # self.x, self.y = x + self.window.ox, y + self.window.oy
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
        if (x - self.window.ox, y - self.window.oy) in self.hitbox:
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
    window = get_window()
    fps = list()
    while window.active:
        start = tm.time()
        if len(window.ev_queue):
            ev = window.ev_queue.popleft()
            if type_ev(ev) == 'Quitte':
                window.active = False
                return
            elif type_ev(ev) == 'Touche':
                window.on_key_press(touche(ev))
            else:
                window.on_mouse_press(abscisse(ev), ordonnee(ev))

        window.on_update(tm.time() - window.last_update)
        if window.view:
            window.view.on_update(tm.time() - window.last_update)

        window.canvas.delete('all')

        window.on_draw()
        if window.view:
            window.view.on_draw()

        window.root.update()
        tm.sleep(max(0., window.interval - (tm.time() - window.last_update)))
        window.last_update = tm.time()

        if not window.active:
            window.root.destroy()
            set_window(None)

        end = tm.time()
        fps.append(end - start)

    print(f'Average FPS: {round(len(fps)/sum(fps), 2)}')


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
              color: str = cfg.gui.palette.black, thickness: int = cfg.gui.thickness):
    w = get_window()
    w.canvas.create_line(ax + w.ox, ay + w.oy, bx + w.ox, by + w.oy, fill=color, width=thickness)


def draw_circle(x: int, y: int, radius: int = cfg.gui.radius, color: str = cfg.gui.palette.light_grey,
                outline: str = cfg.gui.palette.black, thickness: int = cfg.gui.thickness):
    w = get_window()
    w.canvas.create_oval(x - radius + w.ox, y - radius + w.oy, x + radius + w.ox, y + radius + w.oy,
                         fill=color, outline=outline, width=thickness)


def draw_rect(x: int, y: int, width: int, height: int, color: str = cfg.gui.palette.light_grey,
              outline: str = cfg.gui.palette.black, thickness: int = cfg.gui.thickness):
    w = get_window()
    w.canvas.create_rectangle(x - width//2 + w.ox, y - height//2 + w.oy, x + width//2 + w.ox, y + height//2 + w.oy,
                              fill=color, outline=outline, width=thickness)


def draw_text(x: int, y: int, text: str, font_name: str = cfg.gui.font.name, font_size: int = cfg.gui.font.size,
              color: str = cfg.gui.palette.black, location: str = 'center'):
    w = get_window()
    w.canvas.create_text(x + w.ox, y + w.oy, text=text, font=(font_name, font_size), fill=color, anchor=location)


def get_random_color(colors: list[str] = None):
    if colors:
        return rd.choice(colors)
    else:
        return rd.choice(list(vars(cfg.gui.palette).values()))
