from ... import pytk as tk


__all__ = ['basic']


class Button(tk.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, hitbox=tk.hitbox_rect(width, height))
        self.color = 'white'
        self.width = width
        self.height = height

    def draw(self):
        tk.draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=2)
        tk.draw_text(self.x, self.y, 'Hello World')


class MagicCircle(tk.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 10

    def update(self):
        if self.radius < 30:
            self.radius += 0.4

    def draw(self):
        if self.radius < 30:
            tk.draw_circle(self.x, self.y, self.radius, color='white', thickness=2)


class Win(tk.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.button = Button(360, 240, width=200, height=50)
        self.circles = tk.SpriteList()
        print(self.width, self.height, self.dx, self.dy)

    def on_draw(self):
        self.circles.draw()
        self.button.draw()

    def on_update(self, delta_time: float):
        self.circles.update()
        for circle in self.circles:
            if circle.radius == 30:
                del circle

    def on_key_press(self, key):
        print(key)

    def on_mouse_press(self, x: int, y: int, key: str):
        if self.button.collides_with_point(x, y):
            self.button.color = tk.get_random_color()
        else:
            self.circles.append(MagicCircle(x, y))


def basic():
    win = Win(1600, 900)
    tk.run()
