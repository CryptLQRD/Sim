#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os
import random
import blocks

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#FF6262" #Синий-"#2110FF" , Розовый-"#FF6262"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_BAT_DELAY = 0.15
ANIMATION_BATFLYLEFT  = [('%s/monsters/bat/bat_fly_l1.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_l2.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_l3.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_l2.png' % ICON_DIR)]

ANIMATION_BATFLYRIGHT = [('%s/monsters/bat/bat_fly_r1.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_r2.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_r3.png' % ICON_DIR),
                         ('%s/monsters/bat/bat_fly_r2.png' % ICON_DIR)]

ANIMATION_WRAITHLEFT  = [('%s/monsters/wraith_l.png' % ICON_DIR)]
ANIMATION_WRAITHRIGHT = [('%s/monsters/wraith_r.png' % ICON_DIR)]

class Monster(sprite.Sprite): # Класс монстров
    def __init__(self, x, y, left, up, maxLengthLeft,maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up # скорость движения по вертикали, 0 - не двигается

    def update(self, platforms):  # по принципу героя

        if (self.xvel < 0):
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))
        else:
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms): # Метод проверки на столкновение с другими объектами
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                if isinstance(p, blocks.BigEnergy):  # Если коснулись энергии то телепортируем её в другое место
                    blocks.BigEnergy.teleporting(p, 1, 1, platforms, True)
                elif isinstance(p, Monster): # Если коснулись другого монстра, то игнорируем
                    1
                else:
                    self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                    self.yvel = - self.yvel

class Bat(Monster):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        Monster.__init__(self, x, y, left, up, maxLengthLeft, maxLengthUp)
        #self.rect = Rect(x, y, 29, 29)
        # Анимация полета направо
        boltAnim = []
        for anim in ANIMATION_BATFLYLEFT:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        # Анимация полета налево
        boltAnim = []
        for anim in ANIMATION_BATFLYRIGHT:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

class Wraith(Monster):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        Monster.__init__(self, x, y, left, up, maxLengthLeft, maxLengthUp)
        # Анимация полета направо
        boltAnim = []
        for anim in ANIMATION_WRAITHLEFT:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        # Анимация полета налево
        boltAnim = []
        for anim in ANIMATION_WRAITHRIGHT:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()