import pygame
from pygame.locals import *

from BlankField import *
from base_sprite import BaseSprite
from config import FieldConstants as FC


class Hero(pygame.sprite.Sprite, BaseSprite):

    unitName = "rolobok"
    unitCod = 8
    speed = 5
    direct = 0  # 0-no move,1-up,2-right,3-down,4-left
    arrmove = [[0, 0],
               [5, 6],
               [3, 4],
               [5, 6],
               [1, 2]]
    speedX = 5
    speedY = 5
    slippery = False
    pushed_stone = 0
    force_pushed_stone = 5
    collected_diamonds =0
    collected_diamonds_prev = 0

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

        self.cX2 = self.cX1
        self.cY2 = self.cY1

    def update(self, sp):

        if self.cX % FC.SIZE_CELL == 0 and self.cY % FC.SIZE_CELL == 0:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and keys[K_SPACE]:
                # копаем справа
                self.dig_plane(self, sp, 2)
            elif keys[pygame.K_LEFT] and keys[K_SPACE]:
                # копаем слева
                self.dig_plane(self, sp, 4)
            elif keys[pygame.K_UP] and keys[K_SPACE]:
                # копаем вверх
                self.dig_plane(self, sp, 1)
            elif keys[pygame.K_DOWN] and keys[K_SPACE]:
                # копаем вниз
                self.dig_plane(self, sp, 3)
            elif keys[K_LEFT]:
                self.direct = 4
            elif keys[K_RIGHT]:
                self.direct = 2
            elif keys[K_UP]:
                self.direct = 1
            elif keys[K_DOWN]:
                self.direct = 3

            else:
                self.direct = 0

        self.hero_move(self, sp)

        if self.collected_diamonds != self.collected_diamonds_prev:
            self.collected_diamonds_prev = self.collected_diamonds
            pygame.display.set_caption('Алмазов собрано: ' + str(self.collected_diamonds))

        self.__imindex = 1 & (self.__imindex + 1)
        self.image = self.images[self.arrmove[self.direct][self.__imindex]]

    def draw(self, window):

        window.blit(self.image, (self.cX, self.cY))
