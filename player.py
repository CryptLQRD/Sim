#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import blocks
import pyganim
import monsters
import os
import random
import maps
from typing import List

MOVE_SPEED = 32 #Для плавного движения изменить на 8
WIDTH = 32 #24
HEIGHT = 32 #30
COLOR =  "#888888"

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
#ANIMATION_FLY_LEFT = [('%s/player/0.png' % ICON_DIR, 0.1)]
#ANIMATION_FLY_RIGHT = [('%s/player/1.png' % ICON_DIR, 0.1)]

class Player(sprite.Sprite): # Класс игрока
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.myPosX = -1 #Позиция X игрока в массиве
        self.myPosY = -1 #Позиция Y игрока в массиве
        self.MOVE_SPEED = MOVE_SPEED
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0 # скорость вертикального перемещения
        self.startX = x # текущая позиция x
        self.startY = y # текущая позиция y
        self.onGround = False # На земле ли я?
        self.score = 0
        self.live = 3
        self.imDie = False
        self.imSlow = False
        self.winner = False
        self.Fleft = True #Вспомогательная переменная для анимации
        self.image = Surface((WIDTH,HEIGHT))
        #self.image.fill(Color(COLOR))  #Покрасить героя в серый цвет
        self.image = image.load("%s/player/0_24-32.png" % ICON_DIR)
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        #self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным

    def updatePlayer(self,  left, right, up, down, platforms, way: List[List[int]]): # Метод "передвижения"
        if left:
            self.xvel = -self.MOVE_SPEED # Лево = x- n
            self.image = image.load("%s/player/0_24-32.png" % ICON_DIR)
            self.Fleft = True
        if right:
            self.xvel = self.MOVE_SPEED # Право = x + n
            self.image = image.load("%s/player/1_24-32.png" % ICON_DIR)
            self.Fleft = False
        if up:
            self.yvel = -self.MOVE_SPEED # Лево = x- n
            if self.Fleft==True:
                self.image = image.load("%s/player/0_24-32.png" % ICON_DIR)
            else:
                self.image = image.load("%s/player/1_24-32.png" % ICON_DIR)
        if down:
            self.yvel = self.MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            if self.Fleft==True:
                self.image = image.load("%s/player/0_24-32.png" % ICON_DIR)
            else:
                self.image = image.load("%s/player/1_24-32.png" % ICON_DIR)

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
        if not(up or down): # стоим, когда нет указаний идти
            self.yvel = 0


        #self.onGround = False; # Мы не знаем, когда мы на земле...
        
        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, way)
        #print("Позиция X: " + str(self.rect.x))

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, platforms, way)
        #print("Позиция Y: " + str(self.rect.y))


    def collide(self, xvel, yvel, platforms, way: List[List[int]]): # Метод проверки на столкновения с другими объектами
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster): # если пересакаемый блок - blocks.BlockDie или Monster
                    self.die()# умираем
                elif isinstance(p, blocks.BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.Exit): # если коснулись блока выхода
                    self.winner = True # победили!!!
                    self.teleporting(self.startX, self.startY)
                elif isinstance(p, blocks.BigEnergy): # если коснулись энергии
                    self.score += 1
                    blocks.BigEnergy.teleporting(p, -64 * self.score, 32 * random.randint(1, 5), platforms, False, way)
                    #self.energyTP = True
                    #if (self.rect.x == p.rect.x and self.rect.y == p.rect.y) or (blocks.Exit.myPosX == int(p.rect.x/32) and blocks.Exit.myPosY == int(p.rect.y/32)):
                    #    blocks.BigEnergy.teleporting(p, -160, 32 * random.randint(1, 15), platforms, True)
                    #blocks.BigEnergy.myCoord(p)
                    #maps.clearMap(way)
                    #way[int(p.rect.y / 32)][int(p.rect.x / 32)] = 'E'
                    #del(p)
                    #blocks.BigEnergy.kill(p) # убирает объект, но как бы остается на месте
                #self.imSlow = False
                #self.MOVE_SPEED = MOVE_SPEED
                elif isinstance(p, blocks.BlackHole):
                    #self.imSlow = True
                    #self.MOVE_SPEED = MOVE_SPEED/2
                    1
                else:
                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        #self.onGround = True          # и становится на что-то твердое
                        #self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        #self.yvel = 0                 # и энергия прыжка пропадает


    def teleporting(self, goX, goY): # переносим себя на полученные координаты
        self.rect.x = goX
        self.rect.y = goY

    def die(self): # В случае смерти, переносим себя на начальные координаты
        time.wait(300)
        self.live -= 1
        self.imDie = True
        self.myPosX = int(self.startX/32) #Позиция X игрока в массиве
        self.myPosY = int(self.startY/32) #Позиция Y игрока в массиве
        self.teleporting(self.startX, self.startY) # перемещаемся в начальные координаты


       
