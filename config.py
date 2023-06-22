class FieldConstants:
    SIZE_CELL = 40
    SIZEFIELD_X = 35
    SIZEFIELD_Y = 19
    CNT_MAX_SPRITE = 2000000000
    LENGTH_OF_LIFE = 40

    D_UP_L   = 0  #схема кодирования направлений движения
    D_UP     = 1  #   [D_UP_L]    [D_UP]    [D_UP_R]
    D_UP_R   = 2  #   [D_LEFT]   [D_STOP]  [D_RIGHT]
    D_LEFT   = 3  #   [D_DOWN_L] [D_DOWN] [D_DOWN_R]
    D_STOP   = 4  #
    D_RIGHT  = 5  #
    D_DOWN_L = 6  #
    D_DOWN   = 7  #
    D_DOWN_R = 8  #
    DIRECTION=[D_UP_L,D_UP,D_UP_R,D_LEFT,D_STOP,D_RIGHT,D_DOWN_L,D_DOWN,D_DOWN_R]

    EMPTYPLACE = -1

    EMPTYSPRITE = -1
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

    CNT_WIN_DIAMOND = 10 # количество собранных алмазов для выхода из уровня
    PRESSURE_NON_CRITICAL = 1500 # интервал до превращения магмы  в камень

def set_sprite_id() -> int:
    for i in range(1, FieldConstants.CNT_MAX_SPRITE):
        yield i
    raise RuntimeError('Слишком много выадно Id')


itera_id = set_sprite_id()
