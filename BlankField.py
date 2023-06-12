import pygame

from base_sprite import BaseSprite

from config import FieldConstants as FC


class BlankField(pygame.sprite.Sprite, BaseSprite):

    speed_live = 5
    slippery = False  # не скользкий, с него камни не скатываются

    def get_imindex(self): return self.__imindex

    def set_imindex(self, value): self.__imindex = value

    def __init__(self, parX, parY, parTTL=FC.LENGTH_OF_LIFE):
        self.time_to_live = parTTL
        self.id = -1  # здесь id возможно не нужен

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/blank.png').convert()
        self.images.append(image)

        self.__imindex = 0
        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.cX2 = (self.cX + 39) // FC.SIZE_CELL
        self.cY2 = (self.cY + 39) // FC.SIZE_CELL
        self.unitName = "blank"
        self.unitCod = 0

    def update(self, sp):
        self.time_to_live -= self.speed_live
        if self.time_to_live <= 0:
            self.kill()
        self.rect.x = self.cX
        self.rect.y = self.cY

        # self.image = self.images[self.__imindex]

    def draw(self, window):
        pass
    # window.blit(self.image,(self.cX,self.cY))
