from ... import pytk as tk


# You can subclass Buttons
class Subclass(tk.Button):
    def __init__(self):
        super().__init__(x=360, y=100, width=200, height=50, text='Subclass')
        self.color = tk.palette.lavender

    def on_click(self):
        self.color = tk.get_random_color()


# Or you can create separate functions and pass them to 'tk.Button' as an action
def function(obj: tk.Button):
    obj.color = tk.get_random_color()


class Menu(tk.View):
    def __init__(self):
        super().__init__()
        self.subclass = Subclass()
        self.function = tk.Button(x=360, y=400, width=200, height=50, text='Function',
                                  color=tk.palette.lavender, action=function)
        self.bg = tk.palette.light_peach

    def on_draw(self):
        self.subclass.draw()
        self.function.draw()

    def on_mouse_press(self, x: int, y: int, key):
        self.subclass.click(x, y)
        self.function.click(x, y)


def sub():
    win = tk.Window(width=720, height=480)
    win.view = Menu()
    tk.run()
