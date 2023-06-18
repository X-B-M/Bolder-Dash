#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys

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

    def __init__(self) -> object:
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
            if len(levels)>0:
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


class Start_location(Location):
    def __init__(self):
        Location.__init__(self)
        background = pygame.image.load('img/first.png')
        self.background = pygame.transform.scale(background, self.window.get_size())
        font = pygame.font.Font(None, 36)
        text = font.render("press Enter to start", True, (10, 10, 10))
        textpos = text.get_rect(center=(FC.SIZEFIELD_X*FC.SIZE_CELL/2, FC.SIZEFIELD_Y*FC.SIZE_CELL/2))
        self.background.blit(text, textpos)


    def draw(self):
        self.window.blit(self.background, (0, 0))

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == 13:
                #general.location = game_location[0]
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

        #score = font.render("your level: " + str(general.level), True, (20, 20, 20))
        #scorepos = score.get_rect(center=(320, 150))
        #self.background.blit(score, scorepos)

        text = font.render("press Esc key to exit", True, (10, 10, 10))
        textpos = text.get_rect(center=(FC.SIZEFIELD_X*FC.SIZE_CELL/2, FC.SIZEFIELD_Y*FC.SIZE_CELL/2))

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
        f = open(par_map, 'r')
        tY = 0
        for line in f:
            if line[0] == '~': #параметры для уровня
                if "CNT_WIN_DIAMOND" in line:
                    FC.CNT_WIN_DIAMOND = int(line[line.find("=")+1:])
                elif "PRESSURE_NON_CRITICAL" in line:
                    FC.PRESSURE_NON_CRITICAL = int(line[line.find("=")+1:])
            else:
                tX = 0
                for l1 in line:
                    if l1 == "1":
                        self.game_units.add(Wall(tX, tY, 1))
                    elif l1 == "2":
                        self.game_units.add(Wall(tX, tY, 2))
                    elif l1 == "3":
                        self.game_units.add(Plane(tX, tY))
                    elif l1 == "4":
                        self.game_units.add(Stone(tX, tY))
                    elif l1 == "5":
                        self.game_units.add(Diamond(tX, tY))
                    elif l1 == "6":
                        self.game_units.add(MonsterBlank(tX, tY))
                    elif l1 == "7":
                        self.game_units.add(MonsterDiamond(tX, tY))
                    elif l1 == "8":
                        self.game_units.add(Hero(tX, tY))
                    elif l1 == "9":
                        self.game_units.add(Door(tX, tY))
                    elif l1 == "A":
                        self.game_units.add(Magma(tX, tY))

                    #  else:
                    #     self.game_units.add(BlankField(tX,tY))
                    tX += 1
                tY += 1

        f.close()#        keys = pygame.key.get_pressed()

    def draw(self):

        self.window.blit(self.background, (0, 0))
        self.game_units.update(self.game_units)
        self.game_units.draw(self.window)


general = General()

start_location = Start_location()
levels = ['maps/map01.txt',
          'maps/map02.txt',
          'maps/map03.txt']
#game_location =['maps/map01.txt']
#game_location.append(Game_location('maps/map01.txt'))
#game_location.append(Game_location('maps/map02.txt'))
#game_location.append(Game_location('maps/map03.txt'))
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
