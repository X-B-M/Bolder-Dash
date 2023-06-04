import pygame
from pygame.locals import *
from config import FieldConstants as fc, itera_id
from BlankField import *


class MonstrBlank(pygame.sprite.Sprite, BaseSprite):
    speedX = 5
    speedY = 5
    cY1 = 0
    cX1 = 0
    cY2 = 0
    cX2 = 0
    status = 0
    direct = 3
    direct_list = [1, 2, 3, 4]  # двигаемся по правилу левой руки.
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
        image = pygame.image.load('img/monstr_blank1.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monstr_blank2.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monstr_blank3.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        image = pygame.image.load('img/monstr_blank4.png').convert()
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        self.images.append(image)

        self.__imindex = 0

        self.image = self.images[self.__imindex]
        self.rect = image.get_rect()

        self.cX = parX * fc.SIZE_CELL
        self.cY = parY * fc.SIZE_CELL

        self.cX1 = self.cX // fc.SIZE_CELL
        self.cY1 = self.cY // fc.SIZE_CELL

        self.cX2 = (self.cX + 39) // fc.SIZE_CELL
        self.cY2 = (self.cY + 39) // fc.SIZE_CELL

        self.unitName = "monstrblank"
        self.unitCod = 6

    def move(self):
        pass

    def update(self, sp):

        if self.statusTimeLife <= 0:
            self.statusTimeLife = 13

        else:
            self.statusTimeLife -= 1

        self.__imindex = 7 & (self.statusTimeLife // 4)
        self.image = self.images[self.__imindex]

        # если удачно пршли вперед, то направление следующей попытки движения меняеи на следующее
        if self.cX % fc.SIZE_CELL == 0 and self.cY % fc.SIZE_CELL == 0:  # можно ли начать двигаться в текущем
            # направлении

            self.direct = self.direct_list[0]
            exist_support = False  # если справа по направлению движения есть спрайт(опора), то двигаться можно
            # иначе - меняем напраление на следующее в массиве
            tmp = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # для поиска опоры
            for i in sp:
                if self.cX1 + tmp[self.direct - 1][0] == i.cX1 and self.cY1 + tmp[self.direct - 1][1] == i.cY1:
                    exist_support = True
                    break
            if exist_support:  # если опора есть, то проверим, есть ли место для шага вперед
                can_move = True
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                for i in sp:
                    if self.cX1 + tmp[self.direct - 1][0] == i.cX1 and self.cY1 + tmp[self.direct - 1][1] == i.cY1:
                        can_move = False
                        break
                if can_move:  # начинаем двигаться в текущем напрвалении
                    self.cX += self.speedX * tmp[self.direct - 1][0]
                    self.cY += self.speedY * tmp[self.direct - 1][1]
                    self.cX1 = self.cX // fc.SIZE_CELL
                    self.cY1 = self.cY // fc.SIZE_CELL

                    sp.add(BlankField(self.cX1 + tmp[self.direct - 1][0], self.cY1 + tmp[self.direct - 1][1]))

                else:  # места для шага вперед нет, меняем направление
                    self.direct_list = [self.direct_list[-1], *self.direct_list[0:3]]

            else:  # опоры нет, поворачиваем в ту сторону и идем вперед
                self.direct_list = [*self.direct_list[1:], self.direct_list[0]]
                self.direct = self.direct_list[0]
                tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
                self.cX += self.speedX * tmp[self.direct - 1][0]
                self.cY += self.speedY * tmp[self.direct - 1][1]
                self.cX1 = self.cX // fc.SIZE_CELL
                self.cY1 = self.cY // fc.SIZE_CELL

                sp.add(BlankField(self.cX1+tmp[self.direct - 1][0], self.cY1+tmp[self.direct - 1][1]))

        else:  # завершаем движение в клетке
            tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для шага вперед
            self.cX += self.speedX * tmp[self.direct - 1][0]
            self.cY += self.speedY * tmp[self.direct - 1][1]
            self.cX1 = self.cX // fc.SIZE_CELL
            self.cY1 = self.cY // fc.SIZE_CELL

        self.rect.x = self.cX
        self.rect.y = self.cY

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

    def init(self):
        pass
