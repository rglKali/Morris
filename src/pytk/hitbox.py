__all__ = [
    'hitbox_rect',
    'hitbox_circle',
]


def hitbox_rect(width: int, height: int) -> set:
    hitbox = set()
    for w in range(-(width // 2), (width // 2) + 1):
        for h in range(-(height // 2), (height // 2) + 1):
            hitbox.add((w, h))
    return hitbox


def hitbox_circle(radius: int) -> set:
    hitbox = set()
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x ** 2 + y ** 2 <= radius ** 2:
                hitbox.add((x, y))
    return hitbox
