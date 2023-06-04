import pygame
from pygame.locals import *

from BlankField import *
from base_sprite import BaseSprite
from config import FieldConstants as fc


class Hero(pygame.sprite.Sprite, BaseSprite):

    unitName = "rolobok"
    unitCod = 8
    speed = 5
    direct = 0  # 0-no move,1-up,2-right,3-down,4-left
    arrmove = [[0, 0],
               [5, 6],
               [3, 4],
               [5, 6],
               [1, 2]]
    speedX = 5
    speedY = 5
    slippery = False

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)

        self.images = []
        image = pygame.image.load('img/hero_0.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_l1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_l2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_r1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_r2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_up1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/hero_up2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 1

        self.image = self.images[self.arrmove[self.direct][self.__imindex]]
        self.rect = image.get_rect()
        self.cX = parX * fc.SIZE_CELL
        self.cY = parY * fc.SIZE_CELL

        self.cX1 = self.cX // fc.SIZE_CELL
        self.cY1 = self.cY // fc.SIZE_CELL

        self.cX2 = self.cX1
        self.cY2 = self.cY1

    def update(self, sp):

        if self.cX % fc.SIZE_CELL == 0 and self.cY % fc.SIZE_CELL == 0:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.direct = 4
            elif keys[K_RIGHT]:
                self.direct = 2
            elif keys[K_UP]:
                self.direct = 1
            elif keys[K_DOWN]:
                self.direct = 3
            else:
                self.direct = 0

        if self.cX % fc.SIZE_CELL == 0 and self.cY % fc.SIZE_CELL == 0 and self.direct != 0:  # можно ли начать
            # двигаться в текущем  направлении

            can_move = self.check_move(sp, self.cX1, self.cY1, self.direct)

            if can_move == 0: # если пусто, то просто шагаем вперед
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                self.cX += self.speedX * tmp[self.direct - 1][0]
                self.cY += self.speedY * tmp[self.direct - 1][1]
                self.cX1 = self.cX // fc.SIZE_CELL
                self.cY1 = self.cY // fc.SIZE_CELL

                sp.add(BlankField(self.cX1 + tmp[self.direct - 1][0], self.cY1 + tmp[self.direct - 1][1]))
            else:
                forward_sprite=self.get_sprite_by_id(sp, can_move)
                if forward_sprite.unitCod == 3:
                    tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                    self.cX += self.speedX * tmp[self.direct - 1][0]
                    self.cY += self.speedY * tmp[self.direct - 1][1]
                    self.cX1 = self.cX // fc.SIZE_CELL
                    self.cY1 = self.cY // fc.SIZE_CELL

                    forward_sprite.kill()

                    sp.add(BlankField(self.cX1 + tmp[self.direct - 1][0], self.cY1 + tmp[self.direct - 1][1]))


        else:
            if self.direct == 0:
                self.cX1 = self.cX // fc.SIZE_CELL
                self.cY1 = self.cY // fc.SIZE_CELL
                self.cX = self.cX1 * fc.SIZE_CELL
                self.cY = self.cY1 * fc.SIZE_CELL
            else:
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                self.cX += self.speedX * tmp[self.direct - 1][0]
                self.cY += self.speedY * tmp[self.direct - 1][1]
                self.cX1 = self.cX // fc.SIZE_CELL
                self.cY1 = self.cY // fc.SIZE_CELL

        self.rect.x = self.cX
        self.rect.y = self.cY
        if self.cY % fc.SIZE_CELL == 0 and self.cX % fc.SIZE_CELL == 0:
            #self.direct = 0
            pass

        self.__imindex = 1 & (self.__imindex + 1)
        self.image = self.images[self.arrmove[self.direct][self.__imindex]]

    def draw(self, window):

        window.blit(self.image, (self.cX, self.cY))
