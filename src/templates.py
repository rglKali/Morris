import json

from . import pytk as tk
from .data import Board, Player


__all__ = ['Choice']


class lang:
    badges = {'EN': 'Badges', 'FR': 'Pions'}
    unite = {'EN': 'Unite', 'FR': 'Réunir'}
    skip = {'EN': 'Skip', 'FR': 'Sauter'}
    play = {'EN': 'Play selected', 'FR': 'Jouer la sélection'}
    delete = {'EN': 'Delete selected', 'FR': 'Supprimer la sélection'}
    lan = {'EN': 'Return to LAN games', 'FR': 'Revenir aux locales'}
    menu = {'EN': 'Return to main menu', 'FR': 'Revenir au menu principal'}
    editor = {'EN': 'Create my template', 'FR': 'Créer mon modèle'}


class Template(tk.Button):
    radius = 5

    def __init__(self, data: dict, order: int):
        self.data = data
        super().__init__(105 + order * 170, 160, 160, 280)
        self.description = f"{order + 1}. {data['name']}\n" \
                           f"{lang.badges[self.window.lang]}: {data['badges']}\n" \
                           f"{lang.unite[self.window.lang]}: {data['unite']}\n" \
                           f"{lang.skip[self.window.lang]}: {data['skip']}"
        self.board = Board(data)
        self.delta = 60 / (self.board.size // 2)

    def move_left(self):
        self.x -= 170
        self.hitbox = [(self.x + i, self.y + j) for i, j in tk.hitbox_rect(self.width, self.height)]

    def move_right(self):
        self.x += 170
        self.hitbox = [(self.x + i, self.y + j) for i, j in tk.hitbox_rect(self.width, self.height)]

    def draw(self):
        if 0 < self.x < 720:
            super().draw()
            tk.draw_text(self.x, self.y + 100, self.description, font_size=10)
            tk.draw_rect(self.x, self.y - 60, 160, 160, self.color)

            for ind, point in enumerate(self.board.points):
                tk.draw_circle(self.x + self.delta * point.x, self.y - 60 + self.delta * point.y,
                               self.radius, color=tk.palette.black)
                for neighbor in point.neighbors:
                    tk.draw_line(self.x + self.delta * point.x, self.y - 60 + self.delta * point.y,
                                 self.x + self.delta * neighbor.x, self.y - 60 + self.delta * neighbor.y)

    def on_click(self):
        if self.window.features:
            from .lobby import Lobby
            self.window.view = Lobby(self.board)
        else:
            from .game import Game
            self.window.view = Game(self.board, [Player()])


class Templates(tk.SpriteList):
    def __init__(self):
        super().__init__()
        self._raw = json.load(open('data/boards.json'))
        for num, board in enumerate(self._raw):
            self.append(Template(board, num))

        self.selector = 0
        self.local = 0
        self[0].color = tk.palette.yellow

    def move_right(self):
        if self.selector + self.local < len(self) - 1:
            self[self.selector + self.local].color = tk.palette.white
            if self.local < 3:
                self.local += 1
            else:
                self.selector += 1
                [t.move_left() for t in self]
            self[self.selector + self.local].color = tk.palette.yellow

    def move_left(self):
        if self.selector + self.local > 0:
            self[self.selector + self.local].color = tk.palette.white
            if self.local > 0:
                self.local -= 1
            else:
                self.selector -= 1
                [t.move_right() for t in self]
            self[self.selector + self.local].color = tk.palette.yellow

    def delete(self):
        self.pop(self.selector + self.local)
        self._raw.pop(self.selector + self.local)
        json.dump(self._raw, open('data/boards.json', 'w'), indent=4)

    def draw(self):
        tk.draw_rect(x=360, y=160, width=700, height=300)
        super().draw()

    def click(self, x, y):
        [template.click(x, y) for template in self]

    def play(self):
        self[self.selector + self.local].on_click()


class Play(tk.Button):
    def on_click(self):
        self.window.view.templates.play()


class Delete(tk.Button):
    def on_click(self):
        self.window.view.templates.delete()


class Create(tk.Button):
    def on_click(self):
        from .editor import Editor
        self.window.view = Editor()


class Return(tk.Button):
    def on_click(self):
        if self.window.features:
            from .local import Local
            self.window.view = Local()
        else:
            from .menu import Menu
            self.window.view = Menu()


class Choice(tk.View):
    def __init__(self):
        super().__init__()
        self.templates = Templates()
        self.play = Play(x=540, y=440, width=340, height=50, text=lang.play[self.window.lang], color=tk.palette.yellow)
        if self.window.features:
            self.menu = Return(x=180, y=440, width=340, height=50,
                               text=lang.lan[self.window.lang], color=tk.palette.red)
        else:
            self.menu = Return(x=180, y=440, width=340, height=50,
                               text=lang.menu[self.window.lang], color=tk.palette.red)
        if self.window.features:
            self.delete = Delete(x=540, y=360, width=340, height=50,
                                 text=lang.delete[self.window.lang], color=tk.palette.light_peach)
            self.editor = Create(x=180, y=360, width=340, height=50,
                                 text=lang.editor[self.window.lang], color=tk.palette.light_peach)

    def on_draw(self):
        self.templates.draw()
        self.play.draw()
        self.menu.draw()
        if self.window.features:
            self.delete.draw()
            self.editor.draw()

    def on_key_press(self, key: str):
        if key == 'Escape':
            self.menu.on_click()
        elif key == 'Return':
            self.play.on_click()
        elif key == 'Delete' and self.window.features:
            self.delete.on_click()
        elif key == 'Right':
            self.templates.move_right()
        elif key == 'Left':
            self.templates.move_left()

    def on_mouse_press(self, x: int, y: int, key):
        self.templates.click(x, y)
        self.play.click(x, y)
        self.menu.click(x, y)
        if self.window.features:
            self.delete.click(x, y)
            self.editor.click(x, y)
