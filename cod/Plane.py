import pygame
from config import FieldConstants as FC
from cod.base_sprite import BaseSprite

class Plane(pygame.sprite.Sprite, BaseSprite):
    slippery = False  # не скользкий, с него камни не скатываются

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

        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.unitName = "plane"
        self.unitCod = FC.PLANE
        self.rect.x = self.cX-1
        self.rect.y = self.cY-1

    def update(self, sp):
        # self.image = self.images[self.__imindex]
        pass

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))