import random
import time

import pygame

from config import FieldConstants as FC
from config import itera_id


class LocalGroupList(list):
    def get_id(self, direction):
        try:
            return self[direction].id
        except:
            return -1
    def get_unitCod(self, direction):
        try:
            return self[direction].unitCod
        except:
            return -1
    def get_kinect_energy(self, direction):
        try:
            return self[direction].kinect_energy
        except:
            return 0


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
        area_of_explosive = [[cur_spr.cX1 - 1, cur_spr.cY1 - 1], [cur_spr.cX1 + 0, cur_spr.cY1 - 1],
                             [cur_spr.cX1 + 1, cur_spr.cY1 - 1],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 0], [cur_spr.cX1 + 0, cur_spr.cY1 + 0],
                             [cur_spr.cX1 + 1, cur_spr.cY1 + 0],
                             [cur_spr.cX1 - 1, cur_spr.cY1 + 1], [cur_spr.cX1 + 0, cur_spr.cY1 + 1],
                             [cur_spr.cX1 + 1, cur_spr.cY1 + 1]]
        for i in sprites_list:  # уничтожаем все вокруг центра взрыва
            if i.cX1 >= cur_spr.cX1 - 1 and i.cX1 <= cur_spr.cX1 + 1:
                if i.cY1 >= cur_spr.cY1 - 1 and i.cY1 <= cur_spr.cY1 + 1:
                    # if i.unitCod != FC.WALL_STEEL and i.unitCod != FC.BLANKFIELD and i.unitCod != FC.DOOR:
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
    def danger_place(sp, x, y) -> int:
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
                if x + tmp[j][0] == i.cX1 and y + tmp[j][1] == i.cY1 and (
                        i.unitCod == FC.HERO or i.unitCod == FC.MAGMA):
                    return i.id
        return -1

    @staticmethod
    def check_move(sp, x, y, cm_direct) -> int:
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
    def create_local_group(current_sprite, sprites_list) -> LocalGroupList:
        sp_list_of_collide = pygame.sprite.spritecollide(current_sprite, sprites_list, False, collided=pygame.sprite.collide_rect_ratio(1.10))
        c_l_g = LocalGroupList([None for i in FC.DIRECTION])
        tmp = [[-1, -1], [0, -1], [+1, -1],
               [-1, 0], [0, 0], [+1, 0],
               [-1, +1], [0, +1], [+1, +1]]
        for i in sp_list_of_collide:
            for direction in FC.DIRECTION:
                if current_sprite.cX1 + tmp[direction][0] == i.cX1 and current_sprite.cY1 + tmp[direction][1] == i.cY1:
                    c_l_g[direction] = i
                    break
        # s = pygame.sprite.GroupSingle()
        # for direction in range(9):
        #      if isinstance(c_l_g[direction],None.__class__):
        #          from BlankField import BlankField
        #          s.add(BlankField(x + tmp[direction][0], x + tmp[direction][1], 1, 0))
        #          for j in s:
        #             c_l_g[direction] = j
                  # время жизни этого спрайта минимально, его id=0
        return c_l_g

    @staticmethod
    def fall_and_slippery(current_sprite, sprites_list):

        local_group = BaseSprite.create_local_group(current_sprite, sprites_list)
        if current_sprite.kinect_energy > 0 and current_sprite.direct == FC.D_DOWN:
            # можем взорвать что-то внизу, если падаем
            if local_group.get_unitCod(FC.D_DOWN) in [FC.MONSTERBLANK, FC.MONSTERDIAMOND, FC.HERO]:
                if current_sprite.cX1 == local_group[FC.D_DOWN].cX1 and current_sprite.cY1 in [local_group[FC.D_DOWN].cY1,
                                                                                              local_group[FC.D_DOWN].cY1 - 1]:
                        # цель найдена, взрываем
                    BaseSprite.explosiv_sprite(sprites_list, local_group.get_id(FC.D_DOWN))

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении
            # проверим, нет ли коллизии
            from BlankField import BlankField
            # can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1,
            #                                      current_sprite.direct)
            # can_move = local_group[current_sprite.direct].id
            # can_move = local_group.get_id(FC.D_DOWN)

            # if can_move == 0 and current_sprite.direct == FC.D_DOWN:  # падаем вниз
            if local_group.get_id(FC.D_DOWN) == FC.EMPTYSPRITE and current_sprite.direct == FC.D_DOWN:  # падаем вниз
                sprites_list.add(BlankField(current_sprite.cX1, current_sprite.cY1 + 1))
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.kinect_energy = 8

            elif local_group.get_id(FC.D_RIGHT) == FC.EMPTYSPRITE and current_sprite.direct == FC.D_RIGHT:  # толкают вправо
                sprites_list.add(BlankField(current_sprite.cX1 + 1, current_sprite.cY1))
                current_sprite.cX += current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.kinect_energy = 8

            elif local_group.get_id(FC.D_LEFT) == FC.EMPTYSPRITE and current_sprite.direct == FC.D_LEFT:  # толкают влево
                sprites_list.add(BlankField(current_sprite.cX1 - 1, current_sprite.cY1))
                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.kinect_energy = 8

            else:  # пробуем соскальзнуть вправо или влево
                #forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_move)
                if local_group[FC.D_DOWN].slippery:
                    can_moveRight = local_group.get_id(FC.D_RIGHT)
                    can_moveDownR = local_group.get_id(FC.D_DOWN_R)
                    if can_moveRight == FC.EMPTYSPRITE and can_moveDownR == FC.EMPTYSPRITE:
                        sprites_list.add(BlankField(current_sprite.cX1 + 1, current_sprite.cY1))
                        sprites_list.add(BlankField(current_sprite.cX1 + 1, current_sprite.cY1 + 1))
                        current_sprite.cX += current_sprite.speedX
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.direct = FC.D_RIGHT
                        current_sprite.kinect_energy = 8
                    else:
                        can_moveLeft = local_group.get_id(FC.D_LEFT)
                        can_moveDownL = local_group.get_id(FC.D_DOWN_L)
                        if can_moveLeft == FC.EMPTYSPRITE and can_moveDownL == FC.EMPTYSPRITE:
                            sprites_list.add(BlankField(current_sprite.cX1 - 1, current_sprite.cY1))
                            sprites_list.add(BlankField(current_sprite.cX1 - 1, current_sprite.cY1 + 1))
                            current_sprite.cX -= current_sprite.speedX
                            current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                            current_sprite.direct = FC.D_LEFT
                            current_sprite.kinect_energy = 8

            current_sprite.kinect_energy -= 1
        else:
            if current_sprite.direct == FC.D_DOWN:  # вниз
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

            elif current_sprite.direct == FC.D_RIGHT:  # Либо его толкают направо, либо соскальзывает направо.
                current_sprite.cX += current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                if current_sprite.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    current_sprite.direct = FC.D_DOWN

            elif current_sprite.direct == FC.D_LEFT:  # Либо его толкают налнво, либо соскальзывает налево.
                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                if current_sprite.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    current_sprite.direct = FC.D_DOWN

            elif current_sprite.direct == FC.D_UP:  # уникальный случай - толкают вверх (не бывает такого).
                pass

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY

    @staticmethod
    def monster_move(current_sprite, sprites_list):
        from BlankField import BlankField

        # если удачно пршли вперед, то направление следующей попытки движения меняеи на следующее
        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении

            tmp = BaseSprite.danger_place(sprites_list, current_sprite.cX1, current_sprite.cY1)
            if tmp > 0:
                BaseSprite.explosiv_sprite(sprites_list, tmp)

            current_sprite.direct = current_sprite.direct_list[0]
            exist_support = False  # если справа по направлению движения есть спрайт(опора), то двигаться можно
            # иначе - меняем напраление на следующее в массиве
            if current_sprite.unitCod == FC.MONSTERDIAMOND:
                tmp = [[0,0],[-1, 0], [0,0],
                       [0, 1],[0, 0], [0, -1],
                       [0, 0],[1, 0], [0,0]]  # для поиска опоры MonstrDiamond
            else:  # .unitCod == FC.MONSTERBLANK
                tmp = [[0, 0],[1, 0],[0, 0],
                       [0, -1],[0, 0],[0, 1],
                       [0, 0],[-1, 0], [0, 0]]  # для поиска опоры MonstrBlank
            for i in sprites_list:
                if current_sprite.cX1 + tmp[current_sprite.direct][0] == i.cX1 and current_sprite.cY1 + \
                        tmp[current_sprite.direct][1] == i.cY1:
                    exist_support = True
                    break
            if exist_support:  # если опора есть, то проверим, есть ли место для шага вперед
                can_move = True
                tmp = [[0, 0], [0,-1], [0,0],
                       [-1,0], [0, 0], [1,0],
                       [0, 0], [0, 1]        ]  # для шага вперед
                for i in sprites_list:
                    if current_sprite.cX1 + tmp[current_sprite.direct][0] == i.cX1 and current_sprite.cY1 + \
                            tmp[current_sprite.direct][1] == i.cY1:
                        can_move = False
                        break
                if can_move:  # начинаем двигаться в текущем напрвалении
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct][0],
                                                current_sprite.cY1 + tmp[current_sprite.direct][1]))

                else:  # места для шага вперед нет, меняем направление
                    current_sprite.direct_list = [current_sprite.direct_list[-1], *current_sprite.direct_list[0:3]]

            else:  # опоры нет, поворачиваем в ту сторону и идем вперед
                current_sprite.direct_list = [*current_sprite.direct_list[1:], current_sprite.direct_list[0]]
                current_sprite.direct = current_sprite.direct_list[0]
                tmp = [[0,0],[0, -1],[0,0],
                       [-1, 0],[0,0],[1, 0],
                       [0,0], [0, 1]        ]  # для шага вперед
                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct][0],
                                            current_sprite.cY1 + tmp[current_sprite.direct][1]))

        else:  # завершаем движение в клетке
            tmp = [[0, 0], [0, -1], [0, 0],
                   [-1, 0], [0, 0], [1, 0],
                   [0, 0], [0, 1]]  # для шага вперед
            current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
            current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
            current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
            current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

    @staticmethod
    def hero_move(current_sprite, sprites_list):

        from BlankField import BlankField

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0 and current_sprite.direct != 0:  # можно ли начать
            # двигаться в текущем  направлении

            if current_sprite.finished_X1 == current_sprite.cX1 and current_sprite.finished_Y1 == current_sprite.cY1:
                # зашли в открытую дверь, покидаем уровень
                my_event = pygame.event.Event(pygame.USEREVENT, message="Exit to next level")
                pygame.event.post(my_event)
                return
            local_group = BaseSprite.create_local_group(current_sprite, sprites_list, current_sprite.cX1, current_sprite.cY1)
            can_move = local_group[current_sprite.direct].id

            # can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1,
            #                                     current_sprite.direct)

            if can_move == 0:  # если пусто, то просто шагаем вперед
                tmp = [[0,0],  [0, -1], [0,0],
                       [-1, 0], [0,0],   [1, 0],
                       [0,0],  [0, 1],   [0,0]]  # для шага вперед

                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct][0],
                                            current_sprite.cY1 + tmp[current_sprite.direct][1]))
            else:
                forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_move)
                forward_sprite = local_group[current_sprite.direct]
                if forward_sprite.unitCod == FC.PLANE:  # съедаем квант поля
                    tmp = [[0, 0], [0, -1], [0, 0],
                           [-1, 0], [0, 0], [1, 0],
                           [0, 0], [0, 1], [0, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    forward_sprite.kill()

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct][0],
                                                current_sprite.cY1 + tmp[current_sprite.direct][1]))
                elif forward_sprite.unitCod == FC.DIAMOND:  # съедаем алмаз
                    tmp = [[0, 0], [0, -1], [0, 0],
                           [-1, 0], [0, 0], [1, 0],
                           [0, 0], [0, 1], [0, 0]]  # для шага вперед
                    current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    current_sprite.collected_diamonds += 1

                    forward_sprite.kill()
                    if current_sprite.collected_diamonds >= FC.CNT_WIN_DIAMOND:
                        # открываем дверь
                        current_sprite.door_opened(sprites_list)

                    sprites_list.add(BlankField(current_sprite.cX1 + tmp[current_sprite.direct][0],
                                                current_sprite.cY1 + tmp[current_sprite.direct][1]))

                elif forward_sprite.unitCod == FC.STONE:  # толкаем камень
                    if current_sprite.direct in [FC.D_RIGHT, FC.D_LEFT]:
                        current_sprite.pushed_stone += current_sprite.force_pushed_stone
                    else:
                        current_sprite.pushed_stone = 0  # обнуляем усилия по толканию камня

                    if current_sprite.pushed_stone >= FC.SIZE_CELL and current_sprite.direct == FC.D_RIGHT:
                        # придаем камню справа имульс движения вправо
                        forward_sprite.direct = FC.D_RIGHT

                        pass
                    elif current_sprite.pushed_stone >= FC.SIZE_CELL and current_sprite.direct == FC.D_LEFT:
                        # придаем камню слева имульс движения влево
                        forward_sprite.direct = FC.D_LEFT
                elif forward_sprite.unitCod == FC.DOOR:  # уходим в открытую дверь
                    if forward_sprite.is_opened:
                        tmp = [[0, 0], [0, -1], [0, 0],
                               [-1, 0], [0, 0], [1, 0],
                               [0, 0], [0, 1], [0, 0]]  # для шага вперед

                        current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                        current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                        current_sprite.finished_X1 = forward_sprite.cX1
                        current_sprite.finished_Y1 = forward_sprite.cY1


        else:
            current_sprite.pushed_stone = 0  # обнуляем усилия по толканию камня

            if current_sprite.direct == 0:
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.cX = current_sprite.cX1 * FC.SIZE_CELL
                current_sprite.cY = current_sprite.cY1 * FC.SIZE_CELL
            else:
                tmp = [[0, 0], [0, -1], [0, 0],
                       [-1, 0], [0, 0], [1, 0],
                       [0, 0], [0, 1], [0, 0]]  # для шага вперед

                current_sprite.cX += current_sprite.speedX * tmp[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * tmp[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY

    @staticmethod
    def dig_plane(current_sprite, sprites_list, direct_dig):
        #can_dig = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, direct_dig)
        local_group = BaseSprite.create_local_group(current_sprite, sprites_list, current_sprite.cX1, current_sprite.cY1)
        can_dig = local_group[direct_dig].id
        if can_dig > 0:
            forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_dig)
            if forward_sprite.unitCod == FC.PLANE:  # съедаем квант поля
                from BlankField import BlankField
                tmp = [[0, 0], [0, -1], [0, 0],
                       [-1, 0], [0, 0], [1, 0],
                       [0, 0], [0, 1], [0, 0]]  # для шага вперед
                forward_sprite.kill()
                sprites_list.add(BlankField(current_sprite.cX1 + tmp[direct_dig][0],
                                            current_sprite.cY1 + tmp[direct_dig][1], FC.LENGTH_OF_LIFE * 2))
            if forward_sprite.unitCod == FC.DIAMOND:  # съедаем квант поля
                from BlankField import BlankField
                tmp = [[0, 0], [0, -1], [0, 0],
                       [-1, 0], [0, 0], [1, 0],
                       [0, 0], [0, 1], [0, 0]]  # для шага вперед

                forward_sprite.kill()
                sprites_list.add(BlankField(current_sprite.cX1 + tmp[direct_dig][0],
                                            current_sprite.cY1 + tmp[direct_dig][1]))
                current_sprite.collected_diamonds += 1

    @staticmethod
    def door_opened(sp):
        for i in sp:
            if i.unitCod == FC.DOOR:
                i.set_imindex(1)
                i.is_opened = True

    @staticmethod
    def spreading_magma(current_sprite, sprites_list):
        from BlankField import BlankField
        tmp = [[0, 0], [0, -1], [0, 0],
               [-1, 0], [0, 0], [1, 0],
               [0, 0], [0, 1], [0, 0]]  # для шага вперед
        can_spreading = []
        may_be_killed = []
        current_sprite.pressureNonCritical += 1
        if current_sprite.pressureNonCritical >= FC.PRESSURE_NON_CRITICAL:  # пора, превращаемся в камень
            from Stone import Stone
            for i in sprites_list:
                if i.unitCod == FC.MAGMA:
                    sprites_list.add(Stone(i.cX1, i.cY1))
                    i.kill()

        if random.randint(0, 1000) > current_sprite.spreading_chance:
            from Magma import Magma
            local_group = BaseSprite.create_local_group(current_sprite, sprites_list, current_sprite.cX1, current_sprite.cY1)
            for d in (FC.D_UP, FC.D_RIGHT, FC.D_DOWN, FC.D_LEFT):
                #can_move = current_sprite.check_move(sprites_list, current_sprite.cX1, current_sprite.cY1, d)
                can_move = local_group[d].id
                tmp_sprite = local_group[d]
                if tmp_sprite.unitCod in [FC.PLANE]:
                    can_spreading.append((current_sprite.cX1 + tmp[d][0],
                                          current_sprite.cY1 + tmp[d][1]))
                    may_be_killed.append(tmp_sprite)
                elif tmp_sprite.unitCod in [FC.BLANKFIELD]:
                    can_spreading.append((current_sprite.cX1 + tmp[d][0], current_sprite.cY1 + tmp[d][1]))

            if len(can_spreading) == 0:  # вся магма заперта
                current_sprite.pressureCritical = 1
                time_ch = 1
                for i in sprites_list:
                    if i.unitCod == FC.MAGMA:
                        time_ch = time_ch & i.pressureCritical
                if time_ch == 1:  # пора, превращаемся
                    from Diamond import Diamond
                    for i in sprites_list:
                        if i.unitCod == FC.MAGMA:
                            sprites_list.add(Diamond(i.cX1, i.cY1))
                            i.kill()

            else:  # магма распространяется

                current_sprite.pressureCritical = 0
                tmp_index = random.randint(0, len(can_spreading) - 1)
                sprites_list.add(Magma(can_spreading[tmp_index][0],
                                       can_spreading[tmp_index][1]))
                try:
                    may_be_killed[tmp_index].kill()
                except:
                    pass
