from config import itera_id

class BaseSprite:
    @staticmethod
    def get_id():
        return itera_id.__next__()

    pass
'''    def get_sprite_env(sprite_lists, current_x, current_y) -> list[list]:
        for i in sprite_lists:
            if self.cX1 == i.cX1 and self.cY1 + 1 == i.cY1 and self.direct == 3 and i.unitCod != 3:
                can_move = False
            if self.cX1 + 1 == i.cX1 and self.cY1 == i.cY1 and self.direct == 2 and i.unitCod != 3:
                can_move = False
            if self.cX1 - 1 == i.cX1 and self.cY1 == i.cY1 and self.direct == 4 and i.unitCod != 3:
                can_move = False
            if self.cX1 == i.cX1 and self.cY1 - 1 == i.cY1 and self.direct == 1 and i.unitCod != 3:
                can_move = False
        a = [[]]
        pass
        return a
'''


