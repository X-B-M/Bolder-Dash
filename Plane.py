import pygame
from pygame.locals import *
from config import FieldConstants as fc, itera_id
from base_sprite import BaseSprite

class Plane(pygame.sprite.Sprite, BaseSprite):
    slippery = False  # не скользкий, с него камни не скатываются
    #time_to_live = FC.LENGTH_OF_LIFE
    #speed_live = 0 #живет вечно до особого события


    def get_imindex(self): return self.__imindex

    def set_imindex(self, value): self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/plane.png').convert()
        self.images.append(image)

        self.__imindex = 0
        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * fc.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * fc.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // fc.SIZE_CELL
        self.cY1 = self.cY // fc.SIZE_CELL

        self.cX2 = (self.cX + 39) // fc.SIZE_CELL
        self.cY2 = (self.cY + 39) // fc.SIZE_CELL
        self.unitName = "plane"
        self.unitCod = 3

    def update(self, sp):
        self.rect.x = self.cX
        self.rect.y = self.cY

        # self.image = self.images[self.__imindex]

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))
