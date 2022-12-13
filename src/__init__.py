import dataclasses as dc
import argparse as ap
import json

from .engine import Engine


@dc.dataclass
class ConfigItem:
    def __init__(self, raw: dict):
        for key, value in raw.items():
            if isinstance(value, dict):
                value = ConfigItem(value)
            setattr(self, key, value)

    def save(self):
        js = vars(self)
        for attr, value in js.items():
            if isinstance(value, ConfigItem):
                js[attr] = value.save()
        return js


# Setting up the Config
cfg = ConfigItem(json.load(open('data/config.json')))

# Setting up the Engine
engine = Engine()


def main():
    # Arguments GUI/UI version
    args = ap.ArgumentParser()
    args.add_argument('--ui', action='store_true', help='Set this parameter, if you want to run the ui version')
    args.add_argument('--gui', action='store_true', help='Set this parameter, if you want to run the gui version')
    args = args.parse_args()

    if args.gui and not args.ui:
        from .gui import gui
        gui()
    elif args.ui and not args.gui:
        from .ui import ui
        ui()

    # Running default
    else:
        if cfg.globals.gui:
            from .gui import gui
            gui()
        else:
            from .ui import ui
            ui()

    # Save config
    json.dump(cfg.save(), open('data/config.json', 'w'), indent=4)
