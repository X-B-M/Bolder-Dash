#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

from cod.Wall import *
from cod.Plane import *
from cod.Stone import *
from cod.MonsterBlank import *
from cod.MonsterDiamond import *
from cod.Hero import *
from cod.Door import *
from cod.Magma import *


class Location(object):
    def __init__(self):
        self.window = pygame.display.get_surface()

    def event(self, event):
        pass

    def draw(self):
        pass


class General:
    level = 0
    music = 0
    sizeFieldX = FC.SIZEFIELD_X * FC.SIZE_CELL
    sizeFieldY = FC.SIZEFIELD_Y * FC.SIZE_CELL
    map_game = []

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((self.sizeFieldX, self.sizeFieldY))
        pygame.display.set_caption('Бу-го-га')
        #        pygame.mixer.music.load('s.mp3')
        pygame.mixer.music.load('sound/05.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        for i in range(FC.SIZEFIELD_X):
            self.map_game.append([])
            for j in range(FC.SIZEFIELD_Y):
                self.map_game[i].append([])

    def event(self, event):
        if event.type == QUIT:
            sys.exit()
        if event.type == USEREVENT:
            if len(levels) > 0:
                general.location = Game_location(levels[0])
                levels.pop(0)
            else:
                general.location = exit_location
        if event.type == KEYUP:
            if event.key == K_m:
                if self.music:
                    pygame.mixer.music.pause()
                    self.music = 0
                else:
                    pygame.mixer.music.unpause()
                    self.music = 1
            elif event.key == K_ESCAPE:
                general.location = exit_location


class Start_Location(Location):
    def __init__(self):
        Location.__init__(self)
        background = pygame.image.load('img/first.png')
        self.background = pygame.transform.scale(background, self.window.get_size())
        font = pygame.font.Font(None, 36)
        text = font.render("press Enter to start", True, (10, 10, 10))
        textpos = text.get_rect(center=(FC.SIZEFIELD_X * FC.SIZE_CELL / 2, FC.SIZEFIELD_Y * FC.SIZE_CELL / 2))
        self.background.blit(text, textpos)

    def draw(self):
        self.window.blit(self.background, (0, 0))

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == 13:
                # general.location = game_location[0]
                general.location = Game_location(levels[0])
                levels.pop(0)


class Exit_location(Location):
    def __init__(self):
        Location.__init__(self)

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    def draw(self):
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 200, 200))
        font = pygame.font.Font(None, 36)

        # score = font.render("your level: " + str(general.level), True, (20, 20, 20))
        # scorepos = score.get_rect(center=(320, 150))
        # self.background.blit(score, scorepos)

        text = font.render("press Esc key to exit", True, (10, 10, 10))
        textpos = text.get_rect(center=(FC.SIZEFIELD_X * FC.SIZE_CELL / 2, FC.SIZEFIELD_Y * FC.SIZE_CELL / 2))

        self.background.blit(text, textpos)
        self.window.blit(self.background, (0, 0))


class Game_location(Location):
    alreadyPlay = 0

    def __init__(self, par_map):
        Location.__init__(self)
        big_surf = pygame.image.load('img/fone.png').convert()
        big_surf = pygame.transform.scale(big_surf, self.window.get_size())
        #        pygame.image.save(big_surf, 'day1.png')
        self.background = big_surf
        self.game_units = pygame.sprite.Group()
        self.arr_sprites = ArrSprite()
        f = open(par_map, 'r')
        tY = 0
        for line in f:
            if line[0] == '~':  # параметры для уровня
                if "CNT_WIN_DIAMOND" in line:
                    FC.CNT_WIN_DIAMOND = int(line[line.find("=") + 1:])
                elif "PRESSURE_NON_CRITICAL" in line:
                    FC.PRESSURE_NON_CRITICAL = int(line[line.find("=") + 1:])
            else:
                tX = 0
                for l1 in line:
                    if l1 == "1":
                        tmp = Wall(tX, tY, 1)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                        # self.game_units.add(self.arr_sprites.store(Wall(tX, tY, 1))
                    elif l1 == "2":
                        tmp = Wall(tX, tY, 2)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "3":
                        tmp = Plane(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "4":
                        tmp = Stone(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "5":
                        tmp = Diamond(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "6":
                        tmp = MonsterBlank(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "7":
                        tmp = MonsterDiamond(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "8":
                        tmp = Hero(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "9":
                        tmp = Door(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)
                    elif l1 == "A":
                        tmp = Magma(tX, tY)
                        self.arr_sprites.store(tmp)
                        self.game_units.add(tmp)

                    #  else:
                    #     self.game_units.add(BlankField(tX,tY))
                    tX += 1
                tY += 1

        f.close()  # keys = pygame.key.get_pressed()

    def draw(self):

        self.window.blit(self.background, (0, 0))

        self.arr_sprites.clear()
        for i in self.game_units:
            self.arr_sprites.store(i)
            # if i.unitCod == 8:
            #     print(f'Hero Y={i.cY}')
        self.game_units.update(self.game_units, self.arr_sprites)
        self.game_units.draw(self.window)


class ArrSprite():
    map = []

    def __init__(self):
        self.map = [[None for _ in range(FC.SIZEFIELD_Y)] for __ in range(FC.SIZEFIELD_X)]

    def store(self, parSprite):
        self.map[parSprite.cX1][parSprite.cY1] = parSprite

    def clear(self):
        self.map = [[None for _ in range(FC.SIZEFIELD_Y)] for __ in range(FC.SIZEFIELD_X)]

general = General()


start_location = Start_Location()
levels = ['maps/' + i for i in os.listdir('maps')]
levels.sort()
exit_location = Exit_location()

general.location = start_location

clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        general.location.event(event)
        general.event(event)

    general.location.draw()
    pygame.display.flip()
    clock.tick(30)
