from . import pytk as tk


__all__ = ['Menu']


class Quit(tk.Button):
    def on_click(self):
        self.window.quit()


class Play(tk.Button):
    def on_click(self):
        from .local import Local
        self.window.view = Local()


class Menu(tk.View):
    def __init__(self):
        super().__init__()
        self.nickname = tk.InputField(x=360, y=150, width=400, height=50, text='Nickname: ',
                                      color=tk.palette.light_peach, max_length=12, default=self.window.nickname)
        self.play = Play(x=360, y=250, width=200, height=50, text='Play Morris', color=tk.palette.yellow)
        self.quit = Quit(x=360, y=350, width=200, height=50, text='Quit game', color=tk.palette.red)

    def on_draw(self):
        self.nickname.draw()
        self.play.draw()
        self.quit.draw()

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.quit.on_click()
        elif key == 'Return' and len(self.nickname) >= 4:
            self.play.on_click()
        elif key == 'Left':
            self.nickname.move_selector_left()
        elif key == 'Right':
            self.nickname.move_selector_right()
        elif key == 'BackSpace':
            self.nickname.remove_char()
        else:
            self.nickname.add_char(key)

    def on_mouse_press(self, x: int, y: int, key):
        self.nickname.click(x, y)
        if len(self.nickname) >= 4:
            self.window.nickname = str(self.nickname)
            self.play.click(x, y)
        self.quit.click(x, y)
