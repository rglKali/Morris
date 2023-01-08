from ... import pytk as tk


class Circle(tk.Sprite):
    def __init__(self, color):
        self.radius = 0
        self.color = color
        super().__init__(x=360, y=240)

    def update(self):
        self.radius += 1

    def draw(self):
        tk.draw_circle(self.x, self.y, self.radius, self.color, thickness=1)


class View(tk.View):
    def __init__(self):
        super().__init__()
        self.circles = tk.SpriteList()
        self.delta = 10
        self.color = False

    def on_update(self, delta_time: float):
        if not self.delta % 10:
            self.circles.append(Circle(tk.palette.white if self.color else tk.palette.black))
            self.color = not self.color
        self.delta += 1

        if (self.circles[0].radius * 2) ** 2 > self.window.width ** 2 + self.window.height ** 2:
            self.circles.pop(0)

        self.circles.update()

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.window.quit()

    def on_draw(self):
        self.circles.draw()


def illusion():
    win = tk.Window()
    win.view = View()
    win.run()
