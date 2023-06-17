class FieldConstants:
    SIZE_CELL = 40
    SIZEFIELD_X = 35
    SIZEFIELD_Y = 19
    CNT_MAX_SPRITE = 2000000000
    LENGTH_OF_LIFE = 40

    EXPLOSIVE = 0
    BLANKFIELD = 0
    WALL_STEEL = 1
    WALL_BRICK = 2
    PLANE = 3
    STONE = 4
    DIAMOND = 5
    MONSTERBLANK = 6
    MONSTERDIAMOND = 7
    HERO = 8
    DOOR = 9
    MAGMA = 10


def set_sprite_id() -> int:
    for i in range(1, FieldConstants.CNT_MAX_SPRITE):
        yield i
    raise RuntimeError('Слишком много выадно Id')


itera_id = set_sprite_id()
