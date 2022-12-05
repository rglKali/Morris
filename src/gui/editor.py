from .objects import View
from . import fltk as tk
from time import time
import json


class Editor(View):
    def __init__(self, window):
        super().__init__(window)
        self.data = {
            'name': None,
            'size': None,
            'points': None,
            'connects': None,
            'pieces': None,
            'unite': None,
            'skip': None,
        }
        self.selector = 'name'

    def draw(self):
        if int(time()) % 2 and self.selector == 'size':
            tk.texte(100, 100, f'Board size: {self.data["size"] if self.data["size"] else ""}|')
        else:
            tk.texte(100, 100, f'Board size: {self.data["size"] if self.data["size"] else ""}')

        if int(time()) % 2 and self.selector == 'name':
            tk.texte(100, 50, f'Board name: {self.data["name"] if self.data["name"] else ""}|')
        else:
            tk.texte(100, 50, f'Board name: {self.data["name"] if self.data["name"] else ""}')

    def update(self, ev):
        if ev[0] == 'Touche':
            key = ev[1].keysym
            if key in ['Down', 'Return'] and self.selector == 'name':
                self.selector = 'size'
            elif key == 'Up' and self.selector == 'size':
                self.selector = 'name'

            elif key in '13579' and self.selector == 'size':
                self.data['size'] = int(key)

            elif key in 'azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN'and self.selector == 'name':
                self.data['name'] = self.data['name'] + key if self.data['name'] else key

            elif key == 'BackSpace' and self.selector == 'name':
                self.data['name'] = self.data['name'][:-1] if self.data['name'] else None

            elif key == 'Return' and self.data['name'] and self.data['size']:
                self.window.view = None

    def save(self):
        data = json.load(open('res/boards.json'))
        data.append(self.data)
        json.dump(data, open('res/boards.json', 'w'), indent=4)
