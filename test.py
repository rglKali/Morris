from time import time


def main():
    hitbox = [range(10, 20), range(10, 20)]
    if 12 in hitbox[0] and 15 in hitbox[1]:
        print('y')


if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print(f'Total: {round(end - start, 2)} seconds')
