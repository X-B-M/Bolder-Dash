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
    def get_slippery(self, direction):
        try:
            return self[direction].slippery
        except:
            return False

    def get_kinect_energy(self, direction):
        try:
            return self[direction].kinect_energy
        except:
            return 0
    def kill_sprite(self, direction):
        try:
            self[direction].kill()
        except:
            pass
    def get_cX1(self, direction):
        try:
            return self[direction].cX1
        except:
            return -1

    def get_cY1(self, direction):
        try:
            return self[direction].cY1
        except:
            return -1


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
        for i in sp:
            for j in (FC.D_UP, FC.D_RIGHT, FC.D_LEFT, FC.D_DOWN):
                if x + FC.MOVE_LIST[0] == i.cX1 and y + FC.MOVE_LIST[j][1] == i.cY1 and (
                        i.unitCod == FC.HERO or i.unitCod == FC.MAGMA):
                    return i.id
        return FC.EMPTYSPRITE

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

    def create_local_group_arr(current_sprite, arr_sp) -> LocalGroupList:
        tmp_c_l_g = [None for _ in FC.DIRECTION]
        tmp = [[-1, -1], [0, -1], [+1, -1],
               [-1, 0], [0, 0], [+1, 0],
               [-1, +1], [0, +1], [+1, +1]]
        for direction in FC.DIRECTION:
            tmp_c_l_g[direction] = arr_sp.map[current_sprite.cX1 + tmp[direction][0]][current_sprite.cY1 + tmp[direction][1]]
        c_l_g = LocalGroupList(tmp_c_l_g)
        return c_l_g

    def debug_create_local_group_arr(current_sprite, arr_sp) -> LocalGroupList:
        tmp_c_l_g = [None for _ in FC.DIRECTION]
        tmp = [[-1, -1], [0, -1], [+1, -1],
               [-1, 0], [0, 0], [+1, 0],
               [-1, +1], [0, +1], [+1, +1]]
        for direction in FC.DIRECTION:
            print(tmp_c_l_g)
            tmp_c_l_g[direction] = arr_sp.map[current_sprite.cX1 + tmp[direction][0]][current_sprite.cY1 + tmp[direction][1]]
        c_l_g = LocalGroupList(tmp_c_l_g)
        print('===================')
        print(c_l_g)
        # a=input('смотрим')
        return c_l_g

    @staticmethod
    def fall_and_slippery(current_sprite, sprites_list, arr_sp):
        local_group = BaseSprite.create_local_group_arr(current_sprite, arr_sp)
        if current_sprite.kinect_energy > 0 and current_sprite.direct == FC.D_DOWN:
            # можем взорвать что-то внизу, если падаем
            if local_group.get_unitCod(FC.D_DOWN) in [FC.MONSTERBLANK, FC.MONSTERDIAMOND, FC.HERO]:
                if current_sprite.cX1 == local_group[FC.D_DOWN].cX1 and current_sprite.cY1 in [local_group[FC.D_DOWN].cY1,
                                                                                              local_group[FC.D_DOWN].cY1 - 1]:
                        # цель найдена, взрываем
                    # BaseSprite.explosiv_sprite(sprites_list, local_group.get_id(FC.D_DOWN))
                    current_sprite.kill()
                    from monster_move import MonsterSprite
                    explosive_sprite_direct_id = local_group.get_id(FC.D_DOWN)
                    explosive_sprite_direct = BaseSprite.get_sprite_by_id(sprites_list, explosive_sprite_direct_id)
                    local_group = BaseSprite.create_local_group_arr(explosive_sprite_direct, arr_sp)
                    MonsterSprite.explosive_sprite(local_group, sprites_list) #local_group.get_id(FC.D_DOWN))
                    return

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0:  # можно ли начать двигаться в текущем  направлении
            from BlankField import BlankField

            if local_group.get_id(FC.D_DOWN) == FC.EMPTYSPRITE: # and current_sprite.direct == FC.D_DOWN:  # падаем вниз
                tmp_add_blank_field = BlankField(current_sprite.cX1, current_sprite.cY1 + 1)
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.kinect_energy = 8
                current_sprite.direct = FC.D_DOWN

            elif local_group.get_id(FC.D_RIGHT) == FC.EMPTYSPRITE and current_sprite.direct == FC.D_RIGHT:  # толкают вправо

                tmp_add_blank_field = BlankField(current_sprite.cX1 + 1, current_sprite.cY1)
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)

                current_sprite.cX += current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.kinect_energy = 8

            elif local_group.get_id(FC.D_LEFT) == FC.EMPTYSPRITE and current_sprite.direct == FC.D_LEFT:  # толкают влево
                tmp_add_blank_field = BlankField(current_sprite.cX1 - 1, current_sprite.cY1)
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)

                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.kinect_energy = 8

            elif local_group.get_id(FC.D_DOWN) == FC.EMPTYSPRITE: #снова падаем вниз (некорректно толкаем)
                tmp_add_blank_field = BlankField(current_sprite.cX1, current_sprite.cY1 + 1)
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)
                current_sprite.cY += current_sprite.speedY
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL
                current_sprite.kinect_energy = 8
                current_sprite.direct = FC.D_DOWN

            else:  # пробуем соскальзнуть вправо или влево
                if local_group.get_slippery(FC.D_DOWN):
                    can_moveRight = local_group.get_id(FC.D_RIGHT)
                    can_moveDownR = local_group.get_id(FC.D_DOWN_R)
                    if can_moveRight == FC.EMPTYSPRITE and can_moveDownR == FC.EMPTYSPRITE:
                        tmp_add_blank_field = BlankField(current_sprite.cX1 + 1, current_sprite.cY1)
                        arr_sp.store(tmp_add_blank_field)
                        sprites_list.add(tmp_add_blank_field)

                        tmp_add_blank_field = BlankField(current_sprite.cX1 + 1, current_sprite.cY1 + 1)
                        arr_sp.store(tmp_add_blank_field)
                        sprites_list.add(tmp_add_blank_field)

                        current_sprite.cX += current_sprite.speedX
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.direct = FC.D_RIGHT
                        current_sprite.kinect_energy = 8
                    else:
                        can_moveLeft = local_group.get_id(FC.D_LEFT)
                        can_moveDownL = local_group.get_id(FC.D_DOWN_L)
                        if can_moveLeft == FC.EMPTYSPRITE and can_moveDownL == FC.EMPTYSPRITE:
                            tmp_add_blank_field = BlankField(current_sprite.cX1 - 1, current_sprite.cY1)
                            arr_sp.store(tmp_add_blank_field)
                            sprites_list.add(tmp_add_blank_field)

                            tmp_add_blank_field = BlankField(current_sprite.cX1 - 1, current_sprite.cY1 + 1)
                            arr_sp.store(tmp_add_blank_field)
                            sprites_list.add(tmp_add_blank_field)

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

            elif current_sprite.direct == FC.D_LEFT:  # Либо его толкают налево, либо соскальзывает налево.
                current_sprite.cX -= current_sprite.speedX
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                if current_sprite.cX % FC.SIZE_CELL == 0:  # дошли налево до конца ячейки, надо падать вниз
                    current_sprite.direct = FC.D_DOWN

            elif current_sprite.direct == FC.D_UP:  # уникальный случай - толкают вверх (не бывает такого).
                pass

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY


    @staticmethod
    def hero_move(current_sprite, sprites_list, arr_sp):

        from BlankField import BlankField

        if current_sprite.cX % FC.SIZE_CELL == 0 and current_sprite.cY % FC.SIZE_CELL == 0 and current_sprite.direct != 0:  # можно ли начать
            # двигаться в текущем  направлении

            if current_sprite.finished_X1 == current_sprite.cX1 and current_sprite.finished_Y1 == current_sprite.cY1:
                # зашли в открытую дверь, покидаем уровень
                my_event = pygame.event.Event(pygame.USEREVENT, message="Exit to next level")
                pygame.event.post(my_event)
                return

            local_group = BaseSprite.create_local_group_arr(current_sprite, arr_sp)
            can_move = local_group.get_id(current_sprite.direct)

            if can_move == FC.EMPTYSPRITE:  # если пусто, то просто шагаем вперед
                current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                tmp_add_blank_field = BlankField(current_sprite.cX1 + FC.MOVE_LIST[current_sprite.direct][0],
                                                 current_sprite.cY1 + FC.MOVE_LIST[current_sprite.direct][1])
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)

            else:
                forward_sprite = local_group[current_sprite.direct]
                if local_group.get_unitCod(current_sprite.direct) == FC.PLANE:  # съедаем квант поля
                    current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    # forward_sprite.kill()
                    local_group[current_sprite.direct].kill()

                    tmp_add_blank_field = BlankField(current_sprite.cX1 + FC.MOVE_LIST[current_sprite.direct][0],
                                                     current_sprite.cY1 + FC.MOVE_LIST[current_sprite.direct][1])
                    arr_sp.store(tmp_add_blank_field)
                    sprites_list.add(tmp_add_blank_field)

                elif local_group.get_unitCod(current_sprite.direct) == FC.DIAMOND:  # съедаем алмаз
                    current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                    current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                    current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                    current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                    current_sprite.collected_diamonds += 1

                    # forward_sprite.kill()
                    local_group[current_sprite.direct].kill()

                    if current_sprite.collected_diamonds >= FC.CNT_WIN_DIAMOND:
                        # открываем дверь
                        current_sprite.door_opened(sprites_list)

                    tmp_add_blank_field = BlankField(current_sprite.cX1 + FC.MOVE_LIST[current_sprite.direct][0],
                                                     current_sprite.cY1 + FC.MOVE_LIST[current_sprite.direct][1])
                    arr_sp.store(tmp_add_blank_field)
                    sprites_list.add(tmp_add_blank_field)

                elif local_group.get_unitCod(current_sprite.direct) == FC.STONE:  # толкаем камень
                    if current_sprite.direct in [FC.D_RIGHT, FC.D_LEFT]:
                        current_sprite.pushed_stone += current_sprite.force_pushed_stone
                    else:
                        current_sprite.pushed_stone = 0  # обнуляем усилия по толканию камня

                    if current_sprite.pushed_stone >= FC.SIZE_CELL and current_sprite.direct == FC.D_RIGHT:
                        # придаем камню справа имульс движения вправо
                        local_group[current_sprite.direct].direct = FC.D_RIGHT

                    elif current_sprite.pushed_stone >= FC.SIZE_CELL and current_sprite.direct == FC.D_LEFT:
                        # придаем камню слева имульс движения влево
                        local_group[current_sprite.direct].direct = FC.D_LEFT

                elif local_group.get_unitCod(current_sprite.direct) == FC.DOOR:  # уходим в открытую дверь
                    if local_group[current_sprite.direct].is_opened:
                        current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                        current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                        current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                        current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

                        current_sprite.finished_X1 = forward_sprite.cX1
                        current_sprite.finished_Y1 = forward_sprite.cY1

        else:

            current_sprite.pushed_stone = 0  # обнуляем усилия по толканию камня

            if current_sprite.direct == 0:
                pass
            else:
                current_sprite.cX += current_sprite.speedX * FC.MOVE_LIST[current_sprite.direct][0]
                current_sprite.cY += current_sprite.speedY * FC.MOVE_LIST[current_sprite.direct][1]
                current_sprite.cX1 = current_sprite.cX // FC.SIZE_CELL
                current_sprite.cY1 = current_sprite.cY // FC.SIZE_CELL

        current_sprite.rect.x = current_sprite.cX
        current_sprite.rect.y = current_sprite.cY

    @staticmethod
    def dig_plane(current_sprite, sprites_list, arr_sp, direct_dig):

        local_group = BaseSprite.create_local_group_arr(current_sprite, arr_sp)
        can_dig = local_group.get_id(direct_dig)
        if can_dig > 0:
            forward_sprite = current_sprite.get_sprite_by_id(sprites_list, can_dig)
            if local_group.get_unitCod(direct_dig) == FC.PLANE:  # съедаем квант поля
                from BlankField import BlankField

                forward_sprite.kill()
                # local_group(current_sprite.direct).kill()
                tmp_add_blank_field = BlankField(current_sprite.cX1 + FC.MOVE_LIST[direct_dig][0],
                                                 current_sprite.cY1 + FC.MOVE_LIST[direct_dig][1], FC.LENGTH_OF_LIFE * 2)
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)

            if local_group.get_unitCod(direct_dig) == FC.DIAMOND:  # съедаем квант поля
                from BlankField import BlankField

                forward_sprite.kill()
                tmp_add_blank_field = BlankField(current_sprite.cX1 + FC.MOVE_LIST[direct_dig][0],
                                                 current_sprite.cY1 + FC.MOVE_LIST[direct_dig][1])
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)

                current_sprite.collected_diamonds += 1

    @staticmethod
    def door_opened(sp):
        for i in sp:
            if i.unitCod == FC.DOOR:
                i.set_imindex(1)
                i.is_opened = True

    @staticmethod
    def spreading_magma(current_sprite, sprites_list, arr_sp):
        from BlankField import BlankField
        tmp = [[-1, -1], [0, -1], [1, -1],
               [-1, 0], [0, 0], [1, 0],
               [-1, 1], [0, 1], [1, 1]]  # для шага вперед
        can_spreading = []
        may_be_killed = []
        current_sprite.pressureNonCritical += 1
        if current_sprite.pressureNonCritical >= FC.PRESSURE_NON_CRITICAL:  # пора, превращаемся в камень
            from Stone import Stone
            for i in sprites_list:
                if i.unitCod == FC.MAGMA:
                    tmp_add_blank_field = Stone(i.cX1, i.cY1)
                    i.kill()
                    arr_sp.store(tmp_add_blank_field)
                    sprites_list.add(tmp_add_blank_field)



        if random.randint(0, 1000) > current_sprite.spreading_chance:
            from Magma import Magma
            local_group = BaseSprite.create_local_group_arr(current_sprite, arr_sp)

            for d in (FC.D_UP, FC.D_RIGHT, FC.D_DOWN, FC.D_LEFT):
                if local_group.get_unitCod(d) in [FC.PLANE, FC.BLANKFIELD]:
                    can_spreading.append((current_sprite.cX1 + tmp[d][0],
                                          current_sprite.cY1 + tmp[d][1]))
                    may_be_killed.append(d)
                elif local_group.get_unitCod(d) in [FC.EMPTYSPRITE]:
                    can_spreading.append((current_sprite.cX1 + tmp[d][0], current_sprite.cY1 + tmp[d][1]))
                    may_be_killed.append(FC.EMPTYSPRITE)

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

                            tmp_add_blank_field = Diamond(i.cX1, i.cY1)
                            i.kill()
                            arr_sp.store(tmp_add_blank_field)
                            sprites_list.add(tmp_add_blank_field)



            else:  # магма распространяется

                current_sprite.pressureCritical = 0
                tmp_index = random.randint(0, len(can_spreading) - 1)

                if may_be_killed[tmp_index] != FC.EMPTYSPRITE:
                    local_group.kill_sprite(may_be_killed[tmp_index])

                tmp_add_blank_field = Magma(can_spreading[tmp_index][0],
                                                can_spreading[tmp_index][1])
                arr_sp.store(tmp_add_blank_field)
                sprites_list.add(tmp_add_blank_field)


