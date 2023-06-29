import pygame.sprite

from cod.Diamond import *
from config import FieldConstants as FC
from cod.base_sprite import BaseSprite

class Stone(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    kinect_energy = 0  # 'энергия удара. Двинулись - накопили 8. Стоим - убывает на 1 до 0
    slippery = True  # скользкий, с него камни скатываются
    direct = FC.D_DOWN

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/stone01.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/stone02.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/stone03.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/stone04.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60

        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.rect = image.get_rect()
        self.rect.x = self.cX
        self.rect.y = self.cY
        # self.rect.width = 1 + FC.SIZE_CELL + 1
        # self.rect.height = 1 + FC.SIZE_CELL + 1

        self.unitName = "stone"
        self.unitCod = FC.STONE

    def update(self, sp, arr_sp):

        self.fall_and_slippery(self, sp, arr_sp)

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

#    def init(self):
#        pass