from BlankField import *
from Explosiv import *
from Diamond import *
from config import FieldConstants as FC
from base_sprite import BaseSprite

class Stone(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    cY2 = 0
    cX2 = 0
    status = 0  # 0-no move,1-up,2-right,3-down,4-left
    kinect_energy = 0  # 'энергия удара. Двинулись - накопили 8. Стоим - убывает на 1 до 0
    slippery = True  # скользкий, с него камни скатываются
    direct = 3
    time_to_live = FC.LENGTH_OF_LIFE
    speed_live = 0 #живет вечно до особого события


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
        self.rect = image.get_rect()
        self.cX = parX * FC.SIZE_CELL  # random.randint(0,general.sizeFieldX-60)//60*60

        self.cY = parY * FC.SIZE_CELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.cX2 = self.cX // FC.SIZE_CELL
        self.cY2 = self.cY // FC.SIZE_CELL

        self.unitName = "stone"
        self.unitCod = 4

    def update(self, sp):

        self.fall_and_slippery(sp, self)

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

#    def init(self):
#        pass
