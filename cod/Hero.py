from pygame.locals import *

from BlankField import *
from cod.base_sprite import BaseSprite
from config import FieldConstants as FC


class Hero(pygame.sprite.Sprite, BaseSprite):

    unitName = "rolobok"
    unitCod = FC.HERO
    speed = 5
    direct = FC.D_STOP
    arrmove = [[0, 0], [5, 6], [0, 0],
               [1, 2], [0, 0], [3, 4],
               [0, 0], [5, 6], [0, 0]]
    speedX = 5
    speedY = 5
    slippery = False
    pushed_stone = 0
    force_pushed_stone = 5
    collected_diamonds =0
    collected_diamonds_prev = 0
    finished_X1 = -1 # когда эта координата станет положительной, значит дверь открыта и можно покинуть уровень,
    finished_Y1 = -1 # встав на эту координату
    def __init__(self, parX, parY):

        self.id = self.set_id()

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

        pygame.display.set_caption(
            'Алмазов собрано: ' + str(self.collected_diamonds) + ' из ' + str(FC.CNT_WIN_DIAMOND))
    def update(self, sp, arr_sp):

        if self.cX % FC.SIZE_CELL == 0 and self.cY % FC.SIZE_CELL == 0:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and (keys[K_SPACE] or keys[K_LSHIFT]):
                # копаем справа
                self.dig_plane(self, sp, arr_sp, FC.D_RIGHT)
            elif keys[pygame.K_LEFT] and (keys[K_SPACE] or keys[K_LSHIFT]):
                # копаем слева
                self.dig_plane(self, sp, arr_sp, FC.D_LEFT)
            elif keys[pygame.K_UP] and (keys[K_SPACE] or keys[K_LSHIFT]):
                # копаем вверх
                self.dig_plane(self, sp, arr_sp, FC.D_UP)
            elif keys[pygame.K_DOWN] and (keys[K_SPACE] or keys[K_LSHIFT]):
                # копаем вниз
                self.dig_plane(self, sp, arr_sp, FC.D_DOWN)
            elif keys[K_LEFT]:
                self.direct = FC.D_LEFT
            elif keys[K_RIGHT]:
                self.direct = FC.D_RIGHT
            elif keys[K_UP]:
                self.direct = FC.D_UP
            elif keys[K_DOWN]:
                self.direct = FC.D_DOWN

            else:
                self.direct = 0

        self.hero_move(self, sp, arr_sp)

        if self.collected_diamonds != self.collected_diamonds_prev:
            self.collected_diamonds_prev = self.collected_diamonds
            pygame.display.set_caption('Алмазов собрано: ' + str(self.collected_diamonds)+' из '+str(FC.CNT_WIN_DIAMOND))

        self.__imindex = 1 & (self.__imindex + 1)
        self.image = self.images[self.arrmove[self.direct][self.__imindex]]

    def draw(self, window):

        window.blit(self.image, (self.cX, self.cY))
