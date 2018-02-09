#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import pyganim
import random

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#003300"  #"#FF6262"
BLACK_COLOR = "#000000"  #"#FF6262"
WHITE_COLOR = "#ffffff"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal1.png' % ICON_DIR),
            ('%s/blocks/portal2.png' % ICON_DIR)]

ANIMATION_EXIT = [
            ('%s/blocks/exit_abyss_1.png' % ICON_DIR),
            ('%s/blocks/exit_abyss_2.png' % ICON_DIR)]

ANIMATION_BIGENERGY = [
            ('%s/blocks/big_energy1.png' % ICON_DIR),
            ('%s/blocks/big_energy2.png' % ICON_DIR),
            ('%s/blocks/big_energy3.png' % ICON_DIR),
            ('%s/blocks/big_energy4.png' % ICON_DIR)]

def levelSize(total_level_width, total_level_height):
    global LevelHeight
    global LevelWidth
    LevelWidth = int(total_level_width / 32)
    LevelHeight = int(total_level_height / 32)
    print("Размер уровня:   Ширина: " + str(LevelWidth) + "   Высота: " + str(LevelHeight))

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        #self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT) # Для каждого объекта могу установить свой размер, для этого необходимо добавить эту строчку.

    #def __del__(self):
    #    print ('Удален: ' + str(self))

class Block(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/platform1.png" % ICON_DIR)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.25))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class BigEnergy(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        #self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        boltAnim = []
        for anim in ANIMATION_BIGENERGY:
            boltAnim.append((anim, 0.15))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

    def teleporting(self, goX, goY, platforms, Random):
        if Random == True:
            #BigEnergy.teleporting(self, 32 * random.randint(1, LevelWidth), 32 * random.randint(1, LevelHeight), platforms, False)
            #levelSize()
            self.rect.x = 32 * random.randint(1, LevelWidth)
            self.rect.y = 32 * random.randint(1, LevelHeight)
            self.collide(platforms)
            print("Телепортировано: Ширина: " + str(LevelWidth) + "   Высота: " + str(LevelHeight))
        else:
            self.rect.x = goX
            self.rect.y = goY
            self.collide(platforms)

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                #BigEnergy.teleporting(self, 32 * random.randint(1, LevelWidth), 32 * random.randint(1, LevelHeight), platforms, True)
                BigEnergy.teleporting(self, 32 * random.randint(1, 34), 32 * random.randint(1, 22), platforms, True)




class Exit(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        #self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        boltAnim = []
        for anim in ANIMATION_EXIT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
