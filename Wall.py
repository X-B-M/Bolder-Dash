import pygame
from pygame.locals import *

SIZECELL=40
class Wall(pygame.sprite.Sprite):
    global SIZECELL
    speedX = 0
    speedY = 0
    speed = 0
    status = 0
    statusTimeLife = 0  # Время движения в заданном направлении
    slippery = False  # не скользкий, с него камни не скатываются

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY, typeOfWall=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/wall_steel.png').convert()
        self.images.append(image)
        image = pygame.image.load('img/wall_steel.png').convert()
        self.images.append(image)
        image = pygame.image.load('img/wall_brick.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = typeOfWall
        self.unitCod = typeOfWall
        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()
        self.cX = parX * SIZECELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * SIZECELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // SIZECELL
        self.cY1 = self.cY // SIZECELL

        self.cX2 = (self.cX + 39) // SIZECELL
        self.cY2 = (self.cY + 39) // SIZECELL
        if typeOfWall == 1:
            self.unitName = "wall_steel"
        else:
            self.unitName = "wall_brick"

    def update(self, sp):
        self.rect.x = self.cX
        self.rect.y = self.cY

        # self.image = self.images[self.__imindex]

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))