import time as tm


def coords_from_point(p: str):
    x = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
    y = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6}
    return x[p[0]], y[p[1]]


def main():
    point = 'e2'
    neighbors = ['e1', 'e3']
    for ind, n1 in enumerate(neighbors):
        for n2 in neighbors[:ind]:
            print(coords_from_point(n1), coords_from_point(n2))


if __name__ == '__main__':
    start = tm.time()
    main()
    end = tm.time()
    print(f'Total: {end - start} seconds')
