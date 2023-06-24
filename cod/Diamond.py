from Explosiv import *
from cod.base_sprite import BaseSprite


class Diamond(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    direct = FC.D_DOWN
    slippery = True  # скользкий, с него камни скатываются
    kinect_energy = 0
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

        self.unitName = "diamond"
        self.unitCod = FC.DIAMOND

    def move(self):
        pass

    def update(self, sp, arr_sp):

        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13
        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        self.fall_and_slippery(self, sp, arr_sp)

    def draw(self, window):
        window.blit(self.image(self.cX, self.cY))

    def init(self):
        pass
