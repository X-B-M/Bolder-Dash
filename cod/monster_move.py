from cod.base_sprite import BaseSprite
from config import FieldConstants as FC


class MonsterSprite:

    @staticmethod
    def monster_move(current_sprite, sp, arr_sp):
        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении

            local_group = BaseSprite.create_local_group_arr(current_sprite, arr_sp)

            # tmp = BaseSprite.danger_place(sprites_list, current_sprite.cX1, current_sprite.cY1)
            tmp = MonsterSprite.danger_place(local_group, current_sprite.cX1, current_sprite.cY1)
            if tmp >= 0:
                MonsterSprite.explosive_sprite(local_group, sp)
                return

            current_sprite.direct = current_sprite.direct_list[0]

            if local_group.get_id(current_sprite.support_list[current_sprite.direct][
                                      2]) != FC.EMPTYSPRITE:  # если опора есть, то проверим, есть ли место для шага вперед
                if local_group.get_unitCod(
                        current_sprite.direct) == FC.EMPTYSPRITE:  # начинаем двигаться в текущем напрвалении
                    current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                else:
                    current_sprite.direct_list = [*current_sprite.direct_list[1:], current_sprite.direct_list[0]]

            else:
                current_sprite.direct_list = [current_sprite.direct_list[-1], *current_sprite.direct_list[0:3]]
                current_sprite.direct = current_sprite.direct_list[0]
                current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

        else:

            current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
            current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
            current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
            current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

    @staticmethod
    def explosive_sprite(local_group, sp):
        not_append = []
        cur_spr = BaseSprite.get_sprite_by_id(sp, local_group.get_id(4))
        area_of_explosive = [[cur_spr.cX1 - 1, cur_spr.cY1 - 1], [cur_spr.cX1 + 0, cur_spr.cY1 - 1],
                             [cur_spr.cX1 + 1, cur_spr.cY1 - 1],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 0], [cur_spr.cX1 + 0, cur_spr.cY1 + 0],
                             [cur_spr.cX1 + 1, cur_spr.cY1 + 0],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 1], [cur_spr.cX1 + 0, cur_spr.cY1 + 1],
                             [cur_spr.cX1 + 1, cur_spr.cY1 + 1]]
        for i in FC.DIRECTION:  # уничтожаем все вокруг центра взрыва
            if local_group.get_unitCod(i) != FC.WALL_STEEL and local_group.get_unitCod(i) != FC.DOOR:
                local_group.kill_sprite(i)
            else:
                not_append.append([local_group.get_cX1(i), local_group.get_cY1(i)])

        for i in area_of_explosive:
            if i not in not_append:
                if cur_spr.unitCod in [FC.MONSTERDIAMOND, FC.HERO]:  # получаем алмазы
                    from cod.Diamond import Diamond
                    sp.add(Diamond(i[0], i[1]))
                else:
                    from cod.Explosiv import Explosiv
                    sp.add(Explosiv(i[0], i[1]))

    @staticmethod
    def danger_place(sp, x, y) -> int:
        """ Из списка локального окружения возвращает направление опасного соседства или
         FC.EMPTYSPRITE если причин для взрыва нет."""
        for j in (FC.D_UP, FC.D_RIGHT, FC.D_LEFT, FC.D_DOWN):
            if x + FC.MOVE_LIST[j][0] == sp.get_cX1(j) and y + FC.MOVE_LIST[j][1] == sp.get_cY1(j):
                if sp.get_unitCod(j) == FC.HERO or sp.get_unitCod(j) == FC.MAGMA:
                    return j
        return FC.EMPTYSPRITE
