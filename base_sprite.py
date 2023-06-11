from config import FieldConstants as FC
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

    @staticmethod
    def fall_and_slippery(sprites_list, current_sprite):
        from BlankField import BlankField

        if current_sprite.kinect_energy > 0 and current_sprite.direct == 3:
            # можем взорвать что-то внизу, если падаем
            flag_kill = []
            for i in sprites_list:
                if i.unitCod in [6, 7, 8]:
                    #if current_sprite.cX1 == i.cX1 and current_sprite.cY > i.cY - FC.SIZE_CELL and current_sprite.cY1 < i.cY1:
                    if current_sprite.cX1 == i.cX1 and current_sprite.cY1 +1 == i.cY1:
                        # цель найдена, взрываем
                        flag_kill.append(i.cX1)
                        flag_kill.append(i.cY1)
                        flag_kill.append(i.unitCod)
                        break
                        # i.kill()
                        # self.kill()

            if len(flag_kill) > 0:
                not_append = []
                area_of_explosive = [[i.cX1 - 1, i.cY1 - 1], [i.cX1, i.cY1 - 1], [i.cX1 + 1, i.cY1 - 1],
                               [i.cX1 - 1, i.cY1], [i.cX1, i.cY1], [i.cX1 + 1, i.cY1],
                               [i.cX1 - 1, i.cY1 + 1], [i.cX1, i.cY1 + 1], [i.cX1 + 1, i.cY1 + 1]]
                for i in sprites_list:  # уничтожаем все вокруг центра взрыва
                    if i.cX1 >= flag_kill[0] - 1 and i.cX1 <= flag_kill[0] + 1:
                        if i.cY1 >= flag_kill[1] - 1 and i.cY1 <= flag_kill[1] + 1:
                            if i.unitCod != 1 and i.unitCod != 0:
                                i.kill()
                            else:
                                if current_sprite.cX1 == i.cX1 and current_sprite.cY1 == i.cY1:
                                    pass # центр ызрыва всегда уничтожается
                                else:
                                    not_append.append([i.cX1, i.cY1])

                for i in area_of_explosive:
                    if i not in not_append:
                        a = 0
                        if flag_kill[2] in [7, 8]:  # получаем алмазы
                            from Diamond import Diamond
                            sprites_list.add(Diamond(i[0], i[1]))
                        else:
                            from Explosiv import Explosiv
                            sprites_list.add(Explosiv(i[0], i[1]))

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении

            can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, current_sprite.direct)

            if can_move == 0 :  # падаем вниз

                sprites_list.add(BlankField(current_sprite.cX1, current_sprite.cY1 + 1))
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.direct = 3
                current_sprite.kinect_energy = 8

            else:  # соскальзываем вправо или влево
                forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_move)
                if forward_sprite.slippery:
                    can_move2 = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, 2)
                    can_move23 = current_sprite.check_move(sprites_list, current_sprite.cX1 + 1, current_sprite.cY1, 3)
                    if can_move2 == 0 and can_move23 == 0:
                        sprites_list.add(BlankField(current_sprite.cX1 + 1, current_sprite.cY1))
                        sprites_list.add(BlankField(current_sprite.cX1 + 1, current_sprite.cY1 + 1))
                        current_sprite.cX += current_sprite.speedX
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.direct = 2
                        current_sprite.kinect_energy = 8
                    else:
                        can_move4 = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, 4)
                        can_move43 = current_sprite.check_move(sprites_list, current_sprite.cX1 - 1, current_sprite.cY1, 3)
                        if can_move4 == 0 and can_move43 == 0:
                            sprites_list.add(BlankField(current_sprite.cX1 - 1, current_sprite.cY1))
                            sprites_list.add(BlankField(current_sprite.cX1 - 1, current_sprite.cY1 + 1))
                            current_sprite.cX -= current_sprite.speedX
                            current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                            current_sprite.direct = 4
                            current_sprite.kinect_energy = 8

            current_sprite.kinect_energy -= 1
        else:
            if current_sprite.direct == 3:  # вниз
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.direct = 3

            elif current_sprite.direct == 2:  # Либо его толкают направо, либо соскальзывает направо.
                current_sprite.cX += current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                if current_sprite.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    current_sprite.direct = 3
                else:
                    current_sprite.direct = 2

            elif current_sprite.direct == 4:  # Либо его толкают налнво, либо соскальзывает налево.
                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                if current_sprite.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    current_sprite.direct = 3
                else:
                    current_sprite.direct = 4

            elif current_sprite.direct == 1:  # уникальный случай - толкают вверх (не бывает такого).
                pass

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY

    @staticmethod
    def monster_move(sprites_list, current_sprite):
        from BlankField import BlankField

        # если удачно пршли вперед, то направление следующей попытки движения меняеи на следующее
        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении
            current_sprite.direct = current_sprite.direct_list[0]
            exist_support = False  # если справа по направлению движения есть спрайт(опора), то двигаться можно
            # иначе - меняем напраление на следующее в массиве
            if current_sprite.unitCod == 7:
                tmp = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # для поиска опоры MonstrDiamond
            else: # .unitCod == 6
                tmp = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # для поиска опоры MonstrBlank
            for i in sprites_list:
                if current_sprite.cX1 + tmp[current_sprite.direct - 1][0] == i.cX1 and current_sprite.cY1 + tmp[current_sprite.direct - 1][1] == i.cY1:
                    exist_support = True
                    break
            if exist_support:  # если опора есть, то проверим, есть ли место для шага вперед
                can_move = True
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                for i in sprites_list:
                    if current_sprite.cX1 + tmp[current_sprite.direct - 1][0] == i.cX1 and current_sprite.cY1 + tmp[current_sprite.direct - 1][1] == i.cY1:
                        can_move = False
                        break
                if can_move:  # начинаем двигаться в текущем напрвалении
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))

                else:  # места для шага вперед нет, меняем направление
                    current_sprite.direct_list = [current_sprite.direct_list[-1], *current_sprite.direct_list[0:3]]

            else:  # опоры нет, поворачиваем в ту сторону и идем вперед
                current_sprite.direct_list = [*current_sprite.direct_list[1:], current_sprite.direct_list[0]]
                current_sprite.direct = current_sprite.direct_list[0]
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))

        else:  # завершаем движение в клетке
            tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
            current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
            current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
            current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
            current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL



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
