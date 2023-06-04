class FieldConstants:
    SIZE_CELL = 40
    SIZEFIELD_X = 35
    SIZEFIELD_Y = 19
    CNT_MAX_SPRITE = 2000


def set_sprite_id() -> int:
    for i in range(1, FieldConstants.CNT_MAX_SPRITE):
        yield i
    raise RuntimeError('Слишком много выадно Id')


itera_id = set_sprite_id()
