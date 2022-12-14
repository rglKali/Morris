from . import pytk as tk

__all__ = ['Menu']


class lang:
    nickname = {'EN': 'Nickname', 'FR': 'Surnom'}
    play = {'EN': 'Play Morris', 'FR': 'Jeu du Moulin'}
    quit = {'EN': 'Quit Game', 'FR': 'Quitter le Jeu'}


class Quit(tk.Button):
    def on_click(self):
        self.window.quit()


class Play(tk.Button):
    def on_click(self):
        if self.window.features:
            from .local import Local
            self.window.view = Local()
        else:
            from .templates import Choice
            self.window.view = Choice()


class Lang(tk.Button):
    def on_click(self):
        self.window.lang = 'FR' if self.window.lang == 'EN' else 'EN'
        self.text = self.window.lang
        self.window.view.play.text = lang.play[self.window.lang]
        self.window.view.quit.text = lang.quit[self.window.lang]
        if self.window.features:
            self.window.view.nickname.text = f'{lang.nickname[self.window.lang]}: '


class Menu(tk.View):
    def __init__(self):
        super().__init__()
        if self.window.features:
            self.nickname = tk.InputField(x=360, y=150, width=400, height=50, text=f'{lang.nickname[self.window.lang]}: ',
                                          color=tk.palette.light_peach, max_length=12, default=self.window.nickname)
        self.play = Play(x=360, y=250, width=200, height=50, text=lang.play[self.window.lang], color=tk.palette.yellow)
        self.quit = Quit(x=360, y=350, width=200, height=50, text=lang.quit[self.window.lang], color=tk.palette.red)
        self.lang = Lang(x=40, y=440, width=50, height=50, text=self.window.lang, color=tk.palette.blue)

    def on_draw(self):
        if self.window.features:
            self.nickname.draw()
        self.play.draw()
        self.quit.draw()
        self.lang.draw()

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.quit.on_click()
        elif self.window.features:
            if key == 'Return' and len(self.nickname) >= 4:
                self.play.on_click()
            elif key == 'Left':
                self.nickname.move_selector_left()
            elif key == 'Right':
                self.nickname.move_selector_right()
            elif key == 'BackSpace':
                self.nickname.remove_char()
            else:
                self.nickname.add_char(key)
        elif key == 'Return':
            self.play.on_click()

    def on_mouse_press(self, x: int, y: int, key):
        if self.window.features:
            self.nickname.click(x, y)
            if len(self.nickname) >= 4:
                self.window.nickname = str(self.nickname)
                self.play.click(x, y)
        else:
            self.play.click(x, y)
        self.quit.click(x, y)
        self.lang.click(x, y)
