from config import FieldConstants as FC
from config import itera_id

GAME_CAPTION ='======'

class BaseSprite:
    global GAME_CAPTION
    @staticmethod
    def set_id():
        return itera_id.__next__()

    @staticmethod
    def get_sprite_by_id(sp, par_id) -> object:
        for i in sp:
            if i.id == par_id:
                return i

    @staticmethod
    def explosiv_sprite(sprites_list, par_id):
        not_append = []
        cur_spr = BaseSprite.get_sprite_by_id(sprites_list, par_id)
        area_of_explosive = [[cur_spr.cX1 - 1, cur_spr.cY1 - 1], [cur_spr.cX1, cur_spr.cY1 - 1], [cur_spr.cX1 + 1, cur_spr.cY1 - 1],
                             [cur_spr.cX1 - 1, cur_spr.cY1], [cur_spr.cX1, cur_spr.cY1], [cur_spr.cX1 + 1, cur_spr.cY1],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 1], [cur_spr.cX1, cur_spr.cY1 + 1], [cur_spr.cX1 + 1, cur_spr.cY1 + 1]]
        for i in sprites_list:  # уничтожаем все вокруг центра взрыва
            if i.cX1 >= cur_spr.cX1 - 1 and i.cX1 <= cur_spr.cX1 + 1:
                if i.cY1 >= cur_spr.cY1 - 1 and i.cY1 <= cur_spr.cY1 + 1:
                    if i.unitCod != 1 and i.unitCod != 0:
                        i.kill()
                    else:
                        if cur_spr.cX1 == i.cX1 and cur_spr.cY1 == i.cY1:
                            pass  # центр ызрыва всегда уничтожается
                        else:
                            not_append.append([i.cX1, i.cY1])

        for i in area_of_explosive:
            if i not in not_append:
                if cur_spr.unitCod in [7, 8]:  # получаем алмазы
                    from Diamond import Diamond
                    sprites_list.add(Diamond(i[0], i[1]))
                else:
                    from Explosiv import Explosiv
                    sprites_list.add(Explosiv(i[0], i[1]))

    @staticmethod
    def danger_place(sp, x, y ) -> int:
        cm = [0, 0, 0,
              0, 0, 0,
              0, 0, 0]
#        tmp = [[-1, -1], [0, -1], [+1, -1],
#               [-1, 0], [0, 0], [+1, 0],
#               [-1, +1], [0, +1], [+1, +1]]
        tmp = [[0, 0], [0, -1], [0, 0],
               [-1, 0], [0, 0], [+1, 0],
               [0, 0], [0, +1], [0, 0]]

        # direct=[41, up 1, 12, left 2, 23, down 3, 34, right 4, stop 0]
        convert_direct = [4, 1, 5, 7, 3]
        for i in sp:
            for j in range(0, 9):
                if x + tmp[j][0] == i.cX1 and y + tmp[j][1] == i.cY1 and i.unitCod == 8:
                    return i.id
        return -1

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
    def fall_and_slippery(current_sprite, sprites_list):
        from BlankField import BlankField

        if current_sprite.kinect_energy > 0 and current_sprite.direct == 3:
            # можем взорвать что-то внизу, если падаем
            flag_kill = []
            for i in sprites_list:
                if i.unitCod in [6, 7, 8]:
                    #if current_sprite.cX1 == i.cX1 and current_sprite.cY > i.cY - FC.SIZE_CELL and current_sprite.cY1 < i.cY1:
                    if current_sprite.cX1 == i.cX1 and current_sprite.cY1 +1 == i.cY1:
                        # цель найдена, взрываем
                        BaseSprite.explosiv_sprite(sprites_list, i.id)
                        break

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении

            can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, current_sprite.direct)

            if can_move == 0 and current_sprite.direct == 3 :  # падаем вниз
                sprites_list.add(BlankField(current_sprite.cX1, current_sprite.cY1 + 1))
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.direct = 3
                current_sprite.kinect_energy = 8

            elif can_move == 0 and current_sprite.direct == 2 :  # толкают вправо
                sprites_list.add(BlankField(current_sprite.cX1+1, current_sprite.cY1))
                current_sprite.cX += current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.direct = 2
                current_sprite.kinect_energy = 8

            elif can_move == 0 and current_sprite.direct == 4 :  # толкают влево
                sprites_list.add(BlankField(current_sprite.cX1-1, current_sprite.cY1))
                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.direct = 4
                current_sprite.kinect_energy = 8

            else:  # пробуем соскальзнуть вправо или влево
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
    def monster_move(current_sprite, sprites_list):
        from BlankField import BlankField

        # если удачно пршли вперед, то направление следующей попытки движения меняеи на следующее
        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении

            tmp = BaseSprite.danger_place(sprites_list, current_sprite.cX1, current_sprite.cY1)
            if tmp>0:
                BaseSprite.explosiv_sprite(sprites_list, tmp)

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


    @staticmethod
    def hero_move(current_sprite, sprites_list):

        from BlankField import BlankField

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0 and current_sprite.direct != 0:  # можно ли начать
            # двигаться в текущем  направлении

            can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, current_sprite.direct)

            if can_move == 0: # если пусто, то просто шагаем вперед
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))
            else:
                forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_move)
                if forward_sprite.unitCod == 3: # съедаем квант поля
                    tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    forward_sprite.kill()

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))
                elif forward_sprite.unitCod == 5: # съедаем алмаз
                    tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    current_sprite.collected_diamonds +=1

                    forward_sprite.kill()

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))

                elif forward_sprite.unitCod == 4: # толкаем камень
                    if current_sprite.direct in [2, 4]:
                        current_sprite.pushed_stone+= current_sprite.force_pushed_stone
                    else:
                        current_sprite.pushed_stone = 0  # обнуляем усилия по толканию камня

                    if current_sprite.pushed_stone>= FC.SIZE_CELL and  current_sprite.direct == 2:
                        # придаем камню справа имульс движения вправо
                        forward_sprite.direct = 2

                        pass
                    elif current_sprite.pushed_stone>= FC.SIZE_CELL and current_sprite.direct == 4:
                        # придаем камню слева имульс движения влево
                        forward_sprite.direct = 4
                        pass
        else:
            current_sprite.pushed_stone = 0 # обнуляем усилия по толканию камня

            if current_sprite.direct == 0:
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.cX = current_sprite.cX1 * FC.SIZE_CELL
                current_sprite.cY = current_sprite.cY1 * FC.SIZE_CELL
            else:
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY
