
from BlankField import *
from Explosiv import *
from Diamond import *
SIZECELL = 40
class Stone(pygame.sprite.Sprite):
    global SIZECELL
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

    def get_imindex(self):
        return self.__imindex

    def set_imindex(self, value):
        self.__imindex = value

    def __init__(self, parX, parY):
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
        self.cX = parX * SIZECELL  # random.randint(0,general.sizeFieldX-60)//60*60

        self.cY = parY * SIZECELL  # random.randint(0,general.sizeFieldY-60)//60*60

        self.cX1 = self.cX // SIZECELL
        self.cY1 = self.cY // SIZECELL

        self.cX2 = self.cX // SIZECELL
        self.cY2 = self.cY // SIZECELL

        self.unitName = "stone"
        self.unitCod = 4

    def update(self, sp):

        if self.kinect_energy >0:
            tmp = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # для поиска цели
            flag_kill = []
            for i in sp:
                if i.unitCod in [6, 7, 8]:
                 #   print("Энерг=",self.kinect_energy,"камень=", self.cY, self.cY1, "Монстр=",i.cY, i.cY1)
                    if self.cX1 + tmp[self.direct - 1][0] == i.cX1 and self.cY + SIZECELL*tmp[self.direct - 1][1] >= i.cY:
                        # цель найдена, взрываем
                        flag_kill.append(i.cX1)
                        flag_kill.append(i.cY1)
                        flag_kill.append(i.unitCod)
                        break
                        #i.kill()
                        #self.kill()

            if len(flag_kill)>0:
                not_append = []
                kill_append = [[i.cX1-1, i.cY1-1], [i.cX1, i.cY1-1], [i.cX1+1, i.cY1-1],
                               [i.cX1-1, i.cY1],   [i.cX1, i.cY1],   [i.cX1+1, i.cY1],
                               [i.cX1-1, i.cY1+1], [i.cX1, i.cY1+1], [i.cX1+1, i.cY1+1]]
                for i in sp: # уничтожаем все вокруг монстра
                    if i.cX1>=flag_kill[0]-1 and i.cX1<=flag_kill[0]+1:
                        if i.cY1 >= flag_kill[1] - 1 and i.cY1 <= flag_kill[1] + 1:
                            if i.unitCod != 1 and i.unitCod != 0:
                                i.kill()
                            else:
                                not_append.append([i.cX1,i.cY1])

                for i in kill_append:
                    if i not in not_append:
                        if flag_kill[2] in [7, 8]: # получаем алмазы
                            sp.add(Diamond(i[0], i[1]))
                        else:
                            sp.add(Explosiv(i[0], i[1]))


        if self.cX % SIZECELL == 0 and self.cY % SIZECELL == 0:  # можно ли начать двигаться в текущем  направлении
            canMove = True
            canMove23 = True
            canMove43 = True
            for i in sp:
                if self.cX1 == i.cX1 and self.cY1 + 1 == i.cY1:
                    canMove = False
                    if not i.slippery:
                        canMove23 = False
                        canMove43 = False
                if self.cX1 + 1 == i.cX1 and self.cY1 == i.cY1:  # не скользко или справа что=то есть
                    canMove23 = False
                if self.cX1 - 1 == i.cX1 and self.cY1 == i.cY1:  # не скользко или слева что=то есть
                    canMove43 = False
                if self.cX1 + 1 == i.cX1 and self.cY1 + 1 == i.cY1:  # справа-внизу что=то есть
                    canMove23 = False
                if self.cX1 - 1 == i.cX1 and self.cY1 + 1 == i.cY1:  # слева-внизу что=то есть
                    canMove43 = False

            if canMove:  # падаем вниз
                sp.add(BlankField(self.cX1, self.cY1 + 1))
                self.cY += self.speedY
                self.cY1 = self.cY // SIZECELL
                self.direct = 3
                self.kinect_energy = 8

            elif canMove23:  # соскальзываем вправо
                sp.add(BlankField(self.cX1 + 1, self.cY1))
                self.cX += self.speedX
                self.cX1 = self.cX // SIZECELL

                if self.cX % SIZECELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 2

                self.kinect_energy = 8

            elif canMove43:  # соскальзываем влево
                sp.add(BlankField(self.cX1 - 1, self.cY1))
                self.cX -= self.speedX
                self.cX1 = self.cX // SIZECELL

                if self.cX % SIZECELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 4

                self.kinect_energy = 8

            else:

                self.kinect_energy -= 1
        else:
            if self.direct == 3:  # вниз
                self.cY += self.speedY
                self.cY1 = self.cY // SIZECELL
                self.direct = 3

            elif self.direct == 2:  # Либо его толкают направо, либо соскальзывает направо.
                self.cX += self.speedX
                self.cX1 = self.cX // SIZECELL
                if self.cX % SIZECELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 2

            elif self.direct == 4:  # Либо его толкают налнво, либо соскальзывает налево.
                self.cX -= self.speedX
                self.cX1 = self.cX // SIZECELL
                if self.cX % SIZECELL == 0:  # дошли вправо до конца ячейки, надо падать вниз
                    self.direct = 3
                else:
                    self.direct = 4

            elif self.direct == 1:  # уникальный случай - толкают вверх (не бывает такого).
                pass

        self.rect.x = self.cX
        self.rect.y = self.cY

        pass

    def draw(self, window):
        window.blit(self.image, (self.cX, self.cY))

    def init(self):
        pass