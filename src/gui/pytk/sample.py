from ... import cfg
from . import *


class SampleCircle(Sprite):
    def __init__(self, x, y, r):
        super().__init__(x, y, hitbox=hitbox_circle(r))
        self.r = r
        self.color = cfg.gui.palette.light_grey

    def draw(self):
        draw_circle(self.x, self.y, self.r, color=self.color, thickness=1)


class SampleRect(Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += 1


class SampleWindow(Window):
    def __init__(self):
        super().__init__()
        self.rect = SampleRect(50, 300, 10, 10)
        self.circle = SampleCircle(100, 400, 20)

    def on_update(self, delta_time: float):
        self.rect.update()

    def on_draw(self):
        draw_text(100, 100, 'Hello World!')
        draw_line(100, 200, 200, 400)
        self.rect.draw()
        self.circle.draw()

    def on_key_press(self, key):
        if key == 'q':
            self.quit()

    def on_mouse_press(self, x, y):
        if self.circle.collides_with_point(x, y):
            self.circle.color = get_random_color()
        print(x, y)


def run_sample():
    w = SampleWindow()
    run()
