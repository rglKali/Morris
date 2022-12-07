import argparse as ap
from .gui import Window, Menu


class Parser(ap.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.description = 'Welcome to the Morris games!'
        self.add_argument(
            '--ui',
            action='store_true',
            help='Set this parameter, if you want to run the ui version. Else would run the gui version'
        )
        self.data = self.parse_args()

    @property
    def gui(self):
        return self.data


def main():
    parser = Parser()
    gui = not parser.data.ui
    if gui:
        window = Window()
        window.view = Menu(window)
        window.run()
