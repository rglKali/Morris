from time import perf_counter
from typing import Optional

from .fltk import cree_fenetre, ferme_fenetre, mise_a_jour, efface_tout, donne_ev, type_ev, touche, abscisse, ordonnee
from .data import palette

__all__ = [
    'Window',
    'View',
    'Sprite',
    'SpriteList'
]

_window: Optional['Window'] = None


def set_window(window) -> None:
    global _window
    if _window is None:
        _window = window
    else:
        raise Exception('Window was already created')


def get_window() -> 'Window':
    if _window is not None:
        return _window
    else:
        raise Exception('Window was not created yet')


# Main classes
class Window:
    dev_width = 720
    dev_height = 480

    def __init__(self, width: int = dev_width, height: int = dev_height,
                 refresh: int = 120, bg: str = palette.white):

        # Save given width and height, and refresh rate value
        self.width, self.height, self.refresh = width, height, refresh

        # Get dx and dy for further resizing algorithms
        self.dx = width / self.dev_width
        self.dy = height / self.dev_height

        # Set the background
        self.bg = bg

        # Set the timer for the first time
        self.timer = perf_counter()

        # By default, window is active
        self.active = True

        # By default, no view attached to the window
        self.view = None

        # Save the window to global variable
        set_window(self)

    def _draw(self):
        # Clear the screen
        efface_tout()

        # Fill the background
        pass

        # Call view's on_draw function, if any
        if self.view is not None:
            self.view.on_draw()

        # Call user's on_draw function
        self.on_draw()

    def on_draw(self):
        pass

    def _update(self):
        # Get the current time
        timer = perf_counter()

        # Get the delta time
        delta = timer - self.timer

        # Update the timer
        self.timer = timer

        # Call user's on_update function
        self.on_update(delta)

        # Call view's on_update function, if any
        if self.view is not None:
            self.view.on_update(delta)

        # Update the root
        mise_a_jour()

    def on_update(self, delta_time: float):
        pass

    def _key_press(self, key):
        # Call user's on_update function
        self.on_key_press(key)

        # Call view's on_update function, if any
        if self.view is not None:
            self.view.on_key_press(key)

    def on_key_press(self, key: str):
        pass

    def _mouse_press(self, x, y, key):
        # Get x and y coordinates of the click
        x, y = round(x / self.dx), round(y / self.dy)

        # If the key name
        if key == 'ClicGauche':
            key = 'Left'
        else:
            key = 'Right'

        # Call user's on_update function
        self.on_mouse_press(x, y, key)

        # Call view's on_update function, if any
        if self.view is not None:
            self.view.on_mouse_press(x, y, key)

    def on_mouse_press(self, x: int, y: int, key: str):
        pass

    def quit(self):
        self.active = False
        ferme_fenetre()

    def run(self):
        # Create fltk window
        cree_fenetre(self.width, self.height, self.refresh)

        # Start main loop
        while self.active:

            # Call the built-in draw function
            self._draw()

            # Call the built-in update function
            self._update()

            # Manage events
            ev = donne_ev()
            if ev is not None:

                # If event was quit, we should close the window
                if type_ev(ev) == 'Quitte':
                    self.quit()
                    break

                # If event was key_press, call on_key_press
                elif type_ev(ev) == 'Touche':
                    self._key_press(touche(ev))

                # If event was a click
                else:
                    self._mouse_press(abscisse(ev), ordonnee(ev), type_ev(ev))


class View:
    def __init__(self):
        self.window = get_window()

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key: str):
        pass

    def on_mouse_press(self, x: int, y: int, key: str):
        pass


class Sprite:
    def __init__(self, x: int = None, y: int = None, hitbox: set = None):
        self.window = get_window()
        self.x, self.y = x, y
        self.hitbox = set()
        if hitbox is not None:
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

    def update(self):
        [sprite.update() for sprite in self if isinstance(sprite, Sprite)]

    def draw(self):
        [sprite.draw() for sprite in self if isinstance(sprite, Sprite)]
