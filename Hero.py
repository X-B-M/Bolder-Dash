import pygame
from pygame.locals import *

from BlankField import *
from config import FieldConstants as FC

class Hero(pygame.sprite.Sprite):
    
    #FC.SIZE_CELL=FieldConstants.SIZE_CELL
    
    
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
        self.cX = parX * FC.SIZE_CELL
        self.cY = parY * FC.SIZE_CELL

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.cX2 = self.cX1
        self.cY2 = self.cY1

    def update(self, sp):

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.direct = 4
        elif keys[K_RIGHT]:
            self.direct = 2
        elif keys[K_UP]:
            self.direct = 1
        elif keys[K_DOWN]:
            self.direct = 3

        if self.cX % FC.SIZE_CELL == 0 and self.cY % FC.SIZE_CELL == 0 and self.direct != 0:  # можно ли начать двигаться в текущем  направлении

            canMove = True
            for i in sp:
                if self.cX1 == i.cX1 and self.cY1 + 1 == i.cY1 and self.direct == 3 and i.unitCod != 3:
                    canMove = False
                if self.cX1 + 1 == i.cX1 and self.cY1 == i.cY1 and self.direct == 2 and i.unitCod != 3:
                    canMove = False
                if self.cX1 - 1 == i.cX1 and self.cY1 == i.cY1 and self.direct == 4 and i.unitCod != 3:
                    canMove = False
                if self.cX1 == i.cX1 and self.cY1 - 1 == i.cY1 and self.direct == 1 and i.unitCod != 3:
                    canMove = False

            if canMove:
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                self.cX += self.speedX * tmp[self.direct - 1][0]
                self.cY += self.speedY * tmp[self.direct - 1][1]
                self.cX1 = self.cX // FC.SIZE_CELL
                self.cY1 = self.cY // FC.SIZE_CELL

                sp.add(BlankField(self.cX1 + tmp[self.direct - 1][0], self.cY1 + tmp[self.direct - 1][1]))

        else:
            if self.direct == 0:
                self.cX1 = self.cX // FC.SIZE_CELL
                self.cY1 = self.cY // FC.SIZE_CELL
                self.cX = self.cX1 * FC.SIZE_CELL
                self.cY = self.cY1 * FC.SIZE_CELL
            else:
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                self.cX += self.speedX * tmp[self.direct - 1][0]
                self.cY += self.speedY * tmp[self.direct - 1][1]
                self.cX1 = self.cX // FC.SIZE_CELL
                self.cY1 = self.cY // FC.SIZE_CELL

        self.rect.x = self.cX
        self.rect.y = self.cY
        if self.cY % FC.SIZE_CELL == 0 and self.cX % FC.SIZE_CELL == 0:
            self.direct = 0

    def draw(self, window):
        self.__imindex = 1 & (self.__imindex + 1)
        self.image = self.images[self.arrmove[max(self.direct, self.direct)][self.__imindex]]

        window.blit(self.image, (self.cX, self.cY))
