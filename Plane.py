import pygame
from pygame.locals import *

SIZECELL=40

class Plane(pygame.sprite.Sprite):
    global SIZECELL
    slippery = False  # не скользкий, с него камни не скатываются
    def get_imindex(self): return self.__imindex

    def set_imindex(self, value): self.__imindex = value

    def __init__(self, parX, parY):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        image = pygame.image.load('img/plane.png').convert()
        self.images.append(image)

        self.__imindex = 0
        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * SIZECELL  # random.randint(0,general.sizeFieldX-60)//60*60
        self.cY = parY * SIZECELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // SIZECELL
        self.cY1 = self.cY // SIZECELL

        self.cX2 = (self.cX + 39) // SIZECELL
        self.cY2 = (self.cY + 39) // SIZECELL
        self.unitName = "plane"
        self.unitCod = 3

    def update(self, sp):
        self.rect.x = self.cX
        self.rect.y = self.cY

        # self.image = self.images[self.__imindex]

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))
