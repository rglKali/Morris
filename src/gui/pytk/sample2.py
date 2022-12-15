from . import pytk as tk


class Button(tk.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, hitbox=tk.hitbox_rect(width, height))
        self.color = 'white'
        self.width = width
        self.height = height

    def draw(self):
        tk.draw_rect(self.x, self.y, self.width, self.height, color=self.color, thickness=2)
        tk.draw_text(self.x, self.y, 'Hello World')


class Win(tk.Window):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.button = Button(400, 225, width=200, height=50)

    def on_draw(self):
        self.button.draw()

    def on_key_press(self, key):
        print(key)

    def on_mouse_press(self, x: int, y: int, key: str):
        if self.button.collides_with_point(x, y):
            self.button.color = tk.get_random_color()


def run_sample():
    w = Win(800, 450)
    tk.run()
