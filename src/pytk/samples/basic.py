from ... import pytk as tk


class Button(tk.Button):
    def on_click(self):
        self.color = tk.palette.random()


class MagicCircle(tk.Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 10
        self.color = tk.palette.random()

    def update(self):
        self.radius += 0.4

    def draw(self):
        tk.draw_circle(self.x, self.y, self.radius, color=self.color, thickness=2)


class Win(tk.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.button = Button(360, 240, width=200, height=50, text='PyTk')
        self.circles = tk.SpriteList()

    def on_draw(self):
        self.circles.draw()
        self.button.draw()

    def on_update(self, delta_time: float):
        self.circles.update()
        for circle in self.circles:
            if round(circle.radius, 1) == 50.0:
                self.circles.remove(circle)

    def on_key_press(self, key):
        print(key)

    def on_mouse_press(self, x: int, y: int, key: str):
        if not self.button.click(x, y):
            self.circles.append(MagicCircle(x, y))


def basic():
    win = Win(800, 450)
    win.run()
