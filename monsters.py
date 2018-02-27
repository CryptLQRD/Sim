#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from pygame import *
import pyganim
import os
import random
import blocks
import player

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
    def __init__(self, x, y, moveOnLeft, moveOnUp, MOVE_SPEED):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # начальные координаты
        self.startY = y
        self.myPosX = -1
        self.myPosY = -1
        self.moveTime = 0
        self.moveOnLeft = moveOnLeft
        self.moveOnUp = moveOnUp
        self.MOVE_SPEED = MOVE_SPEED
        #self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        #self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = 0 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 0 # скорость движения по вертикали, 0 - не двигается

    def moveOn(self, left, right, up, down, way: List[List[int]]):
        if left == True:  # Движение влево в матрице
            way[self.myPosY][self.myPosX] = '0'
            self.myPosX -= 1
            #if blocks.Exit.myPosY == player.Player.myPosY and blocks.Exit.myPosX == player.Player.myPosX:
            #    self.myPosX = int(self.startX / 32)
            #    self.myPosY = int(self.startY / 32)
            way[self.myPosY][self.myPosX] = 'M'

        if right == True:  # Движение вправо в матрице
            way[self.myPosY][self.myPosX] = '0'
            self.myPosX += 1
            #if blocks.Exit.myPosY == player.Player.myPosY and blocks.Exit.myPosX == player.Player.myPosX:
            #    self.myPosX = int(self.startX / 32)
            #    self.myPosY = int(self.startY / 32)
            way[self.myPosY][self.myPosX] = 'M'

        if up == True:  # Движение вверх в матрице
            way[self.myPosY][self.myPosX] = '0'
            self.myPosY -= 1
            #if blocks.Exit.myPosY == player.Player.myPosY and blocks.Exit.myPosX == player.Player.myPosX:
            #    self.myPosX = int(self.startX / 32)
            #    self.myPosY = int(self.startY / 32)
            way[self.myPosY][self.myPosX] = 'M'

        if down == True:  # Движение вниз в матрице
            way[self.myPosY][self.myPosX] = '0'
            self.myPosY += 1
            #if blocks.Exit.myPosY == player.Player.myPosY and blocks.Exit.myPosX == player.Player.myPosX:
            #    self.myPosX = int(self.startX / 32)
            #    self.myPosY = int(self.startY / 32)
            way[self.myPosY][self.myPosX] = 'M'

    def algMove(self, way: List[List[int]]):

        left = False
        right = False
        up = False
        down = False
        #moveTimeFlag = False

        if way[self.myPosY][self.myPosX - 1] != 'B':# or way[self.myPosY][self.myPosX - 1] != 'W' or way[self.myPosY][self.myPosX - 1] != 'E':
            #if way[hero.myPosY][hero.myPosX - 1] == 'W': moveTimeFlag = True
            left = True
            print("Monster: Left" + str(self.myPosY) + str(self.myPosX - 1))

        elif way[self.myPosY][self.myPosX + 1] != 'B':# or way[self.myPosY][self.myPosX + 1] != 'W' or way[self.myPosY][self.myPosX + 1] != 'E':
            #if way[hero.myPosY][hero.myPosX + 1] == 'W': moveTimeFlag = True
            right = True
            print("Monster: Right")

        elif way[self.myPosY - 1][self.myPosX] != 'B':# or way[self.myPosY - 1][self.myPosX] != 'W' or way[self.myPosY - 1][self.myPosX] != 'E':
            #if way[hero.myPosY - 1][hero.myPosX] == 'W': moveTimeFlag = True
            up = True
            print("Monster: Up")

        elif way[self.myPosY + 1][self.myPosX] != 'B':# or way[self.myPosY + 1][self.myPosX] != 'W' or way[self.myPosY + 1][self.myPosX] != 'E':
            #if way[hero.myPosY + 1][hero.myPosX] == 'W': moveTimeFlag = True
            down = True
            print("Monster: Down")

        Monster.moveOn(self, left, right, up, down, way)
        #if moveTimeFlag == True:
        #    moveTime = 0
        #else:
        self.moveTime = 32/self.MOVE_SPEED
        return left, right, up, down

    def update(self, platforms, left, right, up, down, way: List[List[int]]):  # по принципу героя

        if (self.xvel < 0):
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))
        else:
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))

        if left:
            self.xvel = -self.MOVE_SPEED  # Лево = x- n
        if right:
            self.xvel = self.MOVE_SPEED  # Право = x + n
        if up:
            self.yvel = -self.MOVE_SPEED  # Лево = x- n
        if down:
            self.yvel = self.MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        if not (up or down):  # стоим, когда нет указаний идти
            self.yvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.rect.y += self.yvel  # переносим свои положение на yvel
        self.collide(platforms)

        #if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
        #    self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        #if (abs(self.startY - self.rect.y) > self.maxLengthUp):
        #    self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль



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

    def myCoord(self):
        self.myPosX = int(self.rect.x/32)
        self.myPosY = int(self.rect.y/32)

    def updateOld(self, platforms):  # по принципу героя

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

        #def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        #    Monster.__init__(self, x, y, left, up, maxLengthLeft, maxLengthUp)

class Bat(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, MOVE_SPEED):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, MOVE_SPEED)
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
    def __init__(self, x, y, moveOnLeft, moveOnUp, MOVE_SPEED):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, MOVE_SPEED)
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
