from pygame.locals import *
from config import FieldConstants as FC
from cod.BlankField import *
from cod.base_sprite import BaseSprite
from monster_move import MonsterSprite



class MonsterDiamond(pygame.sprite.Sprite, BaseSprite, MonsterSprite):

    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    cY2 = 0
    cX2 = 0
    status = 0
    direct = 3
    direct_list = [FC.D_LEFT, FC.D_DOWN, FC.D_RIGHT, FC.D_UP]  # двигаемся по правилу левой руки.
    move_list = [[0, 0], [0, -1], [0, 0],  #
                 [-1, 0], [0, 0], [1, 0],
                 [0, 0], [0, 1], [0, 0]]  # для движения в заданном направлении

    support_list = [[0, 0, 0], [1, 0, 5], [0, 0, 0],   # x,y,supp_direct
                    [0, -1, 1], [0, 0, 4], [0, 1, 7],
                    [0, 0, 0], [-1, 0, 3], [0, 0, 0]]  # для поиска опоры MonsterDiamond

    slippery = False  # скользкий, с него камни скатываются
    prev_status = 0  # информация о том, в прошлой итерции обект двигался (1,2,3,4)
    statusTimeLife = 0  # Время движения в заданном направлении

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):

        self.id = self.set_id()

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/monster_diamond1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monster_diamond2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monster_diamond3.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monster_diamond4.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * FC.SIZE_CELL
        self.cY = parY * FC.SIZE_CELL

        self.cX1 = self.cX // FC.SIZE_CELL
        self.cY1 = self.cY // FC.SIZE_CELL

        self.unitName = "monstrdiamond"
        self.unitCod = FC.MONSTERDIAMOND

    def move(self):
        pass

    def update(self, sp, arr_sp):

        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13

        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        # self.monster_move(current_sprite=self, arr_sp=arr_sp)
        self.monster_move(self, sp, arr_sp=arr_sp)

        self.rect.x = self.cX
        self.rect.y = self.cY

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

    def init(self):
        pass
