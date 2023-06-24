import pygame
from pygame.locals import *

from cod.base_sprite import BaseSprite
from config import FieldConstants as FC


class Explosiv(pygame.sprite.Sprite, BaseSprite):
    time_to_live = FC.SIZE_CELL
    speed_live = 2
    slippery = False  # не скользкий, с него камни не скатываются
    statusTimeLife = 13  # для отсчета номера картинки

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []

        def get_imindex(self): return self.__imindex

        def set_imindex(self, value): self.__imindex = value

        image = pygame.image.load('img/explosiv1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/explosiv2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/explosiv3.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/explosiv4.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.unitName = "blank"
        self.unitCod = FC.EXPLOSIVE

    def update(self, sp, arr_sp):
        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13
        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        self.time_to_live -= self.speed_live
        if self.time_to_live <= 0:
            self.kill()
        self.rect.x = self.cX
        self.rect.y = self.cY

    def draw(self, window):
        pass
    # window.blit(self.image,(self.cX,self.cY))
