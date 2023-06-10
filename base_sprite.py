from config import itera_id


class BaseSprite:
    @staticmethod
    def set_id():
        return itera_id.__next__()

    @staticmethod
    def get_sprite_by_id(sp, par_id) -> object:
        for i in sp:
            if i.id == par_id:
                return i

    @staticmethod
    def check_move(sp, x, y, cm_direct) ->int:
        cm = [0, 0, 0,
              0, 0, 0,
              0, 0, 0]
        tmp = [[-1, -1], [0, -1], [+1, -1],
               [-1, 0], [0, 0], [+1, 0],
               [-1, +1], [0, +1], [+1, +1]]
        # direct=[41, up 1, 12, left 2, 23, down 3, 34, right 4, stop 0]
        convert_direct = [4, 1, 5, 7, 3]
        for i in sp:
            for j in range(0, 9):
                if x + tmp[j][0] == i.cX1 and y + tmp[j][1] == i.cY1:
                    cm[j] = i.id

        return cm[convert_direct[cm_direct]]

    def fallen_and_slippery(self):
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
