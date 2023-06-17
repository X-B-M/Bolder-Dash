import random

import pygame

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
    def explosiv_sprite(sprites_list, par_id):
        not_append = []
        cur_spr = BaseSprite.get_sprite_by_id(sprites_list, par_id)
        area_of_explosive = [[cur_spr.cX1 - 1, cur_spr.cY1 - 1], [cur_spr.cX1 + 0, cur_spr.cY1 - 1], [cur_spr.cX1 + 1, cur_spr.cY1 - 1],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 0], [cur_spr.cX1 + 0, cur_spr.cY1 + 0], [cur_spr.cX1 + 1, cur_spr.cY1 + 0],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 1], [cur_spr.cX1 + 0, cur_spr.cY1 + 1], [cur_spr.cX1 + 1, cur_spr.cY1 + 1]]
        for i in sprites_list:  # уничтожаем все вокруг центра взрыва
            if i.cX1 >= cur_spr.cX1 - 1 and i.cX1 <= cur_spr.cX1 + 1:
                if i.cY1 >= cur_spr.cY1 - 1 and i.cY1 <= cur_spr.cY1 + 1:
                    #if i.unitCod != FC.WALL_STEEL and i.unitCod != FC.BLANKFIELD and i.unitCod != FC.DOOR:
                    if i.unitCod != FC.WALL_STEEL and i.unitCod != FC.DOOR:
                        i.kill()
                    else:
                        if cur_spr.cX1 == i.cX1 and cur_spr.cY1 == i.cY1:
                            pass  # центр ызрыва всегда уничтожается
                        else:
                            not_append.append([i.cX1, i.cY1])

        for i in area_of_explosive:
            if i not in not_append:
                if cur_spr.unitCod in [FC.MONSTERDIAMOND, FC.HERO]:  # получаем алмазы
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
                if x + tmp[j][0] == i.cX1 and y + tmp[j][1] == i.cY1 and (i.unitCod == FC.HERO or i.unitCod == FC.MAGMA):
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
            if x + tmp[convert_direct[cm_direct]][0] == i.cX1 and y + tmp[convert_direct[cm_direct]][1] == i.cY1:
                return i.id
        return 0

    @staticmethod
    def check_move_old(sp, x, y, cm_direct) ->int:
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
                if i.unitCod in [FC.MONSTERBLANK, FC.MONSTERDIAMOND, FC.HERO]:
                    #if current_sprite.cX1 == i.cX1 and current_sprite.cY > i.cY - FC.SIZE_CELL and current_sprite.cY1 < i.cY1:
                    if current_sprite.cX1 == i.cX1 and current_sprite.cY1 in [i.cY1, i.cY1-1]:
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
            if current_sprite.unitCod == FC.MONSTERDIAMOND:
                tmp = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # для поиска опоры MonstrDiamond
            else: # .unitCod == FC.MONSTERBLANK
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

            if  current_sprite.finished_X1 == current_sprite.cX1 and current_sprite.finished_Y1 == current_sprite.cY1 :
                # зашли в открытую дверь, покидаем уровень
                my_event = pygame.event.Event(pygame.USEREVENT, message="Exit to next level")
                pygame.event.post(my_event)
                return

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
                if forward_sprite.unitCod == FC.PLANE: # съедаем квант поля
                    tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    forward_sprite.kill()

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))
                elif forward_sprite.unitCod == FC.DIAMOND: # съедаем алмаз
                    tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    current_sprite.collected_diamonds +=1

                    forward_sprite.kill()
                    if current_sprite.collected_diamonds >= 10:
                        # открываем дверь
                        current_sprite.door_opened(sprites_list)

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct - 1][0], current_sprite.cY1 + tmp[current_sprite.direct - 1][1]))

                elif forward_sprite.unitCod == FC.STONE: # толкаем камень
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
                elif forward_sprite.unitCod == FC.DOOR:  # уходим в открытую дверь
                    if forward_sprite.is_opened:
                        tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                        current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct - 1][0]
                        current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct - 1][1]
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                        current_sprite.finished_X1 = forward_sprite.cX1
                        current_sprite.finished_Y1 = forward_sprite.cY1


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

    @staticmethod
    def dig_plane(current_sprite, sprites_list, direct_dig):
        can_dig = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, direct_dig)
        if can_dig > 0:
            forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_dig)
            if forward_sprite.unitCod == FC.PLANE:  # съедаем квант поля
                from BlankField import BlankField
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                forward_sprite.kill()
                sprites_list.add(BlankField(current_sprite.cX1 + tmp[direct_dig - 1][0],
                                            current_sprite.cY1 + tmp[direct_dig - 1][1],FC.LENGTH_OF_LIFE*2))


    @staticmethod
    def door_opened(sp):
        for i in sp:
            if i.unitCod == FC.DOOR:
                i.set_imindex(1)
                i.is_opened = True

    @staticmethod
    def spreading_magma(current_sprite, sprites_list):
        from BlankField import BlankField
        tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
        can_spreading = []
        may_be_killed = []
        current_sprite.pressureNonCritical -= 1
        if current_sprite.pressureNonCritical <= 0:  # пора, превращаемся в камень
            from Stone import Stone
            for i in sprites_list:
                if i.unitCod == FC.MAGMA:
                    sprites_list.add(Stone(i.cX1, i.cY1))
                    i.kill()

        if random.randint(0, 1000) > 998:
            from Magma import Magma
            for d in range(1,5):
                can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, d)
                if can_move > 0:
                    tmp_sprite = current_sprite.get_sprite_by_id(sprites_list, can_move)

                    if tmp_sprite.unitCod in [FC.PLANE]:
                        can_spreading.append((current_sprite.cX1 + tmp[d - 1][0],
                                              current_sprite.cY1 + tmp[d - 1][1]))
                        may_be_killed.append(tmp_sprite)
                else:
                    can_spreading.append((current_sprite.cX1 + tmp[d - 1][0], current_sprite.cY1 + tmp[d - 1][1]))

            if len(can_spreading) == 0: # вся магма заперта
                current_sprite.pressureCritical = 1
                if random.randint(0, 1000) > 0: # а не пора ли превратиться
                    time_ch = 1
                    for i in sprites_list:
                        if i.unitCod == FC.MAGMA:
                            time_ch = time_ch & i.pressureCritical
                    if time_ch == 1: # пора, превращаемся
                        from Diamond import Diamond
                        for i in sprites_list:
                            if i.unitCod == FC.MAGMA:
                                sprites_list.add(Diamond(i.cX1,i.cY1))
                                i.kill()

            else: # магма распространяется

                current_sprite.pressureCritical = 0
                tmp_index = random.randint(0, len(can_spreading)-1)
                sprites_list.add(Magma(can_spreading[tmp_index][0],
                                       can_spreading[tmp_index][1]))
                try:
                    may_be_killed[tmp_index].kill()
                except:
                    pass
