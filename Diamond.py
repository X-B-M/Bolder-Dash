import pygame
from pygame.locals import *

from BlankField import *
from Explosiv import *
from base_sprite import BaseSprite
from config import itera_id


class Diamond(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    cY2 = 0
    cX2 = 0
    status = 0
    direct = 3
    slippery = True  # скользкий, с него камни скатываются
    kinect_energy = 8
    statusTimeLife = 0  # для отсчета номера картинки

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/diamond_01.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/diamond_02.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/diamond_03.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/diamond_04.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * FC.SIZE_CELL
        self.cY = parY * FC.SIZE_CELL

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.cX2 = (self.cX + 39) // FC.SIZE_CELL
        self.cY2 = (self.cY + 39) // FC.SIZE_CELL

        self.unitName = "diamond"
        self.unitCod = 5

    def move(self):
        pass

    def update(self, sp):

        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13

        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        if self.kinect_energy > 0:
            tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для поиска цели
            flag_kill = []
            for i in sp:
                if i.unitCod in [6, 7, 8]:
                    if self.cX1 + tmp[self.direct - 1][0] == i.cX1 and self.cY + FC.SIZE_CELL * tmp[self.direct - 1][
                        1] >= i.cY:
                        # цель найдена, взрываем
                        flag_kill.append(i.cX1)
                        flag_kill.append(i.cY1)
                        flag_kill.append(i.unitCod)
                        break
                        # i.kill()
                        # self.kill()

            if len(flag_kill) > 0:
                not_append = []
                kill_append = [[i.cX1 - 1, i.cY1 - 1], [i.cX1, i.cY1 - 1], [i.cX1 + 1, i.cY1 - 1],
                               [i.cX1 - 1, i.cY1], [i.cX1, i.cY1], [i.cX1 + 1, i.cY1],
                               [i.cX1 - 1, i.cY1 + 1], [i.cX1, i.cY1 + 1], [i.cX1 + 1, i.cY1 + 1]]
                for i in sp:  # уничтожаем все вокруг монстра
                    if i.cX1 >= flag_kill[0] - 1 and i.cX1 <= flag_kill[0] + 1:
                        if i.cY1 >= flag_kill[1] - 1 and i.cY1 <= flag_kill[1] + 1:
                            if i.unitCod != 1 and i.unitCod != 0:
                                i.kill()
                            else:
                                not_append.append([i.cX1, i.cY1])

                for i in kill_append:
                    if i not in not_append:
                        if flag_kill[2] in [7, 8]:  # получаем алмазы
                            sp.add(Diamond(i[0], i[1]))
                        else:
                            sp.add(Explosiv(i[0], i[1]))

        if self.cX % FC.SIZE_CELL == 0 and self.cY % FC.SIZE_CELL == 0:  # можно ли начать падать в текущем  направлении
            self.direct = 3

            can_move = self.check_move(sp, self.cX1, self.cY1, self.direct)

            if can_move == 0 :  # падаем вниз
                sp.add(BlankField(self.cX1, self.cY1 + 1))
                self.cY += self.speedY
                self.cY1 = self.cY // FC.SIZE_CELL
                self.direct = 3
                self.kinect_energy = 8

            else:  # соскальзываем вправо или влево
                forward_sprite = self.get_sprite_by_id(sp, can_move)
                if forward_sprite.slippery:
                    can_move2 = self.check_move(sp, self.cX1, self.cY1, 2)
                    can_move23 = self.check_move(sp, self.cX1 + 1, self.cY1, 3)
                    if can_move2 == 0 and can_move23 == 0:
                        sp.add(BlankField(self.cX1 + 1, self.cY1))
                        sp.add(BlankField(self.cX1 + 1, self.cY1 + 1))
                        self.cX += self.speedX
                        self.cX1 = self.cX // FC.SIZE_CELL
                        self.direct = 2
                        self.kinect_energy = 8
                    else:
                        can_move4 = self.check_move(sp, self.cX1, self.cY1, 4)
                        can_move43 = self.check_move(sp, self.cX1 - 1, self.cY1, 3)
                        if can_move4 == 0 and can_move43 == 0:
                            sp.add(BlankField(self.cX1 - 1, self.cY1))
                            sp.add(BlankField(self.cX1 - 1, self.cY1+1))
                            self.cX -= self.speedX
                            self.cX1 = self.cX // FC.SIZE_CELL
                            self.direct = 4
                            self.kinect_energy = 8

            self.kinect_energy -= 1

        else:
            if self.direct == 3:  # вниз
                self.cY += self.speedY
                self.cY1 = self.cY // FC.SIZE_CELL
                self.direct = 3

            elif self.direct == 2:  # Либо его толкают направо, либо соскальзывает направо.
                self.cX += self.speedX
                self.cX1 = self.cX // FC.SIZE_CELL
                if self.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 2

            elif self.direct == 4:  # Либо его толкают налнво, либо соскальзывает налево.
                self.cX -= self.speedX
                self.cX1 = self.cX // FC.SIZE_CELL
                if self.cX % FC.SIZE_CELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 4

            elif self.direct == 1:  # уникальный случай - толкают вверх (не бывает такого).
                pass

        self.rect.x = self.cX
        self.rect.y = self.cY

    def draw(self, window):
        window.blit(self.image(self.cX, self.cY))

    def init(self):
        pass
