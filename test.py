from time import time


class Class:
    def __init__(self):
        self.state = True

    def action(self):
        if not self.state:
            return
        else:
            pass


class SubClass(Class):
    def __init__(self):
        super().__init__()
        self.state = False

    def action(self):
        super().action()
        print(self.state)


class List:
    def __init__(self, *args):
        self.widgets = list(args)
        print(self.widgets)


def main():
    pass


if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print(f'Total: {round(end - start, 2)} seconds')
