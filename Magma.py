from BlankField import *
from Explosiv import *
from Diamond import *
from config import FieldConstants as FC
from base_sprite import BaseSprite

class Magma(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    slippery = False  # скользкий, с него камни скатываются
    statusTimeLife = 0  # для отсчета номера картинки
    pressureCritical = 0 # если вся магма заперта, то превращается в алмазы
    pressureNonCritical = 10000 # если дойдет до нуля, то превратится в камень
    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/magma1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/magma2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/magma3.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/magma4.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()
        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60

        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.unitName = "stone"
        self.unitCod = FC.MAGMA

        self.rect.x = self.cX
        self.rect.y = self.cY

    def update(self, sp):

        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13
        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        self.spreading_magma(self, sp)

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

#    def init(self):
#        pass