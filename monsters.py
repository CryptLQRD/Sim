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

ANIMATION_BATFLYUP = [('%s/monsters/bat/bat_back_1.png' % ICON_DIR),
                      ('%s/monsters/bat/bat_back_2.png' % ICON_DIR),
                      ('%s/monsters/bat/bat_back_3.png' % ICON_DIR),
                      ('%s/monsters/bat/bat_back_2.png' % ICON_DIR)]

ANIMATION_BATFLYDOWN = [('%s/monsters/bat/bat_stay_1.png' % ICON_DIR),
                        ('%s/monsters/bat/bat_stay_2.png' % ICON_DIR),
                        ('%s/monsters/bat/bat_stay_3.png' % ICON_DIR),
                        ('%s/monsters/bat/bat_stay_2.png' % ICON_DIR)]

ANIMATION_WRAITHLEFT  = [('%s/monsters/wraith_l.png' % ICON_DIR)]
ANIMATION_WRAITHRIGHT = [('%s/monsters/wraith_r.png' % ICON_DIR)]

class Monster(sprite.Sprite): # Класс монстров
    def __init__(self, x, y, moveOnLeft, moveOnUp, startMoveTime):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # начальные координаты
        self.startY = y
        self.myPosX = -1
        self.myPosY = -1
        self.myPrevPosX = int(self.startX / 32)
        self.myPrevPosY = int(self.startY / 32)
        self.startMoveTime = startMoveTime - 1
        self.moveTime = 0
        self.moveOnLeft = False
        self.moveOnRight = moveOnLeft
        self.moveOnUp = moveOnUp
        self.moveOnDown = False
        self.MOVE_SPEED = 32 #MOVE_SPEED
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        #self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        #self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = 0 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 0 # скорость движения по вертикали, 0 - не двигается

    def moveOn(self, left, right, up, down, hero, way: List[List[int]]):
        if left == True and up == True:  # Движение влево-вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            self.myPosY -= 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True and up == True:  # Движение вправо-вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            self.myPosY -= 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True and down == True:  # Движение вправо-вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            self.myPosY += 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

        elif left == True and down == True:  # Движение влево-вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            self.myPosY += 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

        elif left == True:  # Движение влево в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            if way[self.myPosY][self.myPosX] == 'H' and self.myPosY == hero.myPosY and self.myPosX == hero.myPosX:
                hero.die()
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True:  # Движение вправо в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            if way[self.myPosY][self.myPosX] == 'H' and self.myPosY == hero.myPosY and self.myPosX == hero.myPosX:
                hero.die()
            #way[self.myPosY][self.myPosX] = 'M'

        elif up == True:  # Движение вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosY -= 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

        elif down == True:  # Движение вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosY += 1
            #if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            #    hero.myPosX = int(hero.startX / 32)
            #    hero.myPosY = int(hero.startY / 32)
            #way[self.myPosY][self.myPosX] = 'M'

    def algMove(self, hero, way: List[List[int]]):
        #print ('Left: ' + str(self.moveOnLeft) + '   Right: '+ str(self.moveOnRight))
        if (self.moveOnLeft == True and self.moveOnRight == False) or (self.moveOnLeft == False and self.moveOnRight == True):
            if way[self.myPosY][self.myPosX - 1] == 'B':
                self.moveOnLeft = False
                self.moveOnRight = True
            elif way[self.myPosY][self.myPosX + 1] == 'B':
                self.moveOnLeft = True
                self.moveOnRight = False
        #print ('Up: ' + str(self.moveOnUp) + '   Down: '+ str(self.moveOnDown))
        if (self.moveOnUp == True and self.moveOnDown == False) or (self.moveOnUp == False and self.moveOnDown == True):
            if way[self.myPosY - 1][self.myPosX] == 'B':
                self.moveOnUp = False
                self.moveOnDown = True
            elif way[self.myPosY + 1][self.myPosX] == 'B':
                self.moveOnUp = True
                self.moveOnDown = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        if way[self.myPosY][self.myPosX - 1] != 'B' and self.moveOnLeft == True and self.moveOnRight == False:# or way[self.myPosY][self.myPosX - 1] != 'W' or way[self.myPosY][self.myPosX - 1] != 'E':
            #if way[hero.myPosY][hero.myPosX - 1] == 'W': moveTimeFlag = True
            self.left = True
            #print("Monster: Left   Y=" + str(self.myPosY) + '   X='+ str(self.myPosX - 1))

        elif way[self.myPosY][self.myPosX + 1] != 'B' and self.moveOnLeft == False and self.moveOnRight == True:# or way[self.myPosY][self.myPosX + 1] != 'W' or way[self.myPosY][self.myPosX + 1] != 'E':
            #if way[hero.myPosY][hero.myPosX + 1] == 'W': moveTimeFlag = True
            self.right = True
            #print("Monster: Right   Y=" + str(self.myPosY) + '   X='+ str(self.myPosX + 1))

        if way[self.myPosY - 1][self.myPosX] != 'B' and self.moveOnUp == True and self.moveOnDown == False:# or way[self.myPosY - 1][self.myPosX] != 'W' or way[self.myPosY - 1][self.myPosX] != 'E':
            #if way[hero.myPosY - 1][hero.myPosX] == 'W': moveTimeFlag = True
            self.up = True
            #print("Monster: Up   Y=" + str(self.myPosY - 1) + '   X='+ str(self.myPosX))

        elif way[self.myPosY + 1][self.myPosX] != 'B' and self.moveOnUp == False and self.moveOnDown == True:# or way[self.myPosY + 1][self.myPosX] != 'W' or way[self.myPosY + 1][self.myPosX] != 'E':
            #if way[hero.myPosY + 1][hero.myPosX] == 'W': moveTimeFlag = True
            self.down = True
            #print("Monster: Down   Y=" + str(self.myPosY + 1) + '   X='+ str(self.myPosX))

        Monster.moveOn(self, self.left, self.right, self.up, self.down, hero, way)
        self.moveTime = self.startMoveTime  #32/self.MOVE_SPEED - 1 Для плавного движения

    def update(self, platforms, way: List[List[int]], hero):  # по принципу героя

        #if (self.yvel != 0):
        #    if (self.yvel < 0):
        #        self.image.fill(Color(MONSTER_COLOR))
        #        self.boltAnimUp.blit(self.image, (0, 0))
        #    else:
        #        self.image.fill(Color(MONSTER_COLOR))
        #        self.boltAnimDown.blit(self.image, (0, 0))
        #if (self.xvel != 0):
        #    if (self.xvel < 0):
        #        self.image.fill(Color(MONSTER_COLOR))
        #        self.boltAnimLeft.blit(self.image, (0, 0))
        #    else:
        #        self.image.fill(Color(MONSTER_COLOR))
        #        self.boltAnimRight.blit(self.image, (0, 0))
        if (self.moveOnUp == True and self.moveOnDown == False) or (self.moveOnUp == False and self.moveOnDown == True):
            if self.moveOnUp == True:
                self.image.fill(Color(MONSTER_COLOR))
                self.boltAnimUp.blit(self.image, (0, 0))
            else:
                self.image.fill(Color(MONSTER_COLOR))
                self.boltAnimDown.blit(self.image, (0, 0))

        if (self.moveOnLeft == True and self.moveOnRight == False) or (self.moveOnLeft == False and self.moveOnRight == True):
            if self.moveOnLeft == True:
                self.image.fill(Color(MONSTER_COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))
            else:
                self.image.fill(Color(MONSTER_COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))

        if self.left:
            self.xvel = -self.MOVE_SPEED  # Лево = x- n
        if self.right:
            self.xvel = self.MOVE_SPEED  # Право = x + n
        if self.up:
            self.yvel = -self.MOVE_SPEED  # Лево = x- n
        if self.down:
            self.yvel = self.MOVE_SPEED  # Право = x + n

        if not (self.left or self.right):  # стоим, когда нет указаний идти
            self.xvel = 0
        if not (self.up or self.down):  # стоим, когда нет указаний идти
            self.yvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.rect.y += self.yvel  # переносим свои положение на yvel
        self.collide(platforms, hero , way)

        #if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
        #    self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        #if (abs(self.startY - self.rect.y) > self.maxLengthUp):
        #    self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль



    def collide(self, platforms, hero, way: List[List[int]]): # Метод проверки на столкновение с другими объектами
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                if isinstance(p, blocks.BigEnergy):  # Если коснулись энергии то телепортируем её в другое место
                    if (way[int(p.rect.y / 32)][int(p.rect.x / 32)] != 'H') or (blocks.Exit.myPosX != int(p.rect.x/32) and blocks.Exit.myPosY != int(p.rect.y/32)) or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] != 'M'): #or (self.myPosX == int(p.rect.x / 32) and self.myPosY == int(p.rect.y / 32)):
                        way[int(p.rect.y / 32)][int(p.rect.x / 32)] = '0'
                    blocks.BigEnergy.teleporting(p, 1, 1, platforms, True)
                    #Проверка и отрисовка, нужны Hero и Way
                    while (hero.rect.x == p.rect.x and hero.rect.y == p.rect.y) or (hero.startX == p.rect.x and hero.startY == p.rect.y) or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == 'H') or (blocks.Exit.myPosX == int(p.rect.x/32) and blocks.Exit.myPosY == int(p.rect.y/32)) or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == 'M'): #or (self.myPosX == int(p.rect.x / 32) and self.myPosY == int(p.rect.y / 32)):
                        blocks.BigEnergy.teleporting(p, 32, 32 * random.randint(4, 5), platforms, True)
                    blocks.BigEnergy.myCoord(p)
                    way[int(p.rect.y / 32)][int(p.rect.x / 32)] = 'E'
                elif isinstance(p, Monster): # Если коснулись другого монстра, то игнорируем
                    1
                else:
                    self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                    self.yvel = - self.yvel

    def myCoord(self):
        self.myPosX = int(self.rect.x/32)
        self.myPosY = int(self.rect.y/32)


    def OLD_update_OLD(self, platforms):  # по принципу героя

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

    def teleporting(self, goX, goY, platforms, hero, way):
        #if Random == True: #Если True телепортируем себя на случайне координаты в пределах уровня
        #    self.rect.x = 32 * random.randint(1, LevelWidth-2)
        #    self.rect.y = 32 * random.randint(1, LevelHeight-2)
        #else: #иначе телепортируем себя на выбранные координаты
        self.rect.x = goX
        self.rect.y = goY
        print("Монстр перенесен на начальные координаты... Ширина: " + str(self.rect.x) + "   Высота: " + str(self.rect.y))
        self.collide(platforms, hero, way)

class Bat(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, startMoveTime)
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
        # Анимация полета наверх
        boltAnim = []
        for anim in ANIMATION_BATFLYUP:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        # Анимация полета вниз
        boltAnim = []
        for anim in ANIMATION_BATFLYDOWN:
            boltAnim.append((anim, ANIMATION_BAT_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

class Wraith(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, startMoveTime)
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
