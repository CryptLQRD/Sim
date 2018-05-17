#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from pygame import *
import pyganim
import os
import random
import blocks
import player
import maps

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#000000"#"#FF6262" #Синий-"#2110FF" , Розовый-"#FF6262"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

# Анимации для мыши
ANIMATION_BAT_DELAY = 0.30
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

# Анимации для птицы
ANIMATION_BIRD_DELAY = 0.30
ANIMATION_BIRDFLYLEFT  = [('%s/monsters/bird/bird_left1.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_left2.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_left3.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_left2.png' % ICON_DIR)]

ANIMATION_BIRDFLYRIGHT = [('%s/monsters/bird/bird_right1.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_right2.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_right3.png' % ICON_DIR),
                         ('%s/monsters/bird/bird_right2.png' % ICON_DIR)]

ANIMATION_BIRDFLYUP = [('%s/monsters/bird/bird_up1.png' % ICON_DIR),
                      ('%s/monsters/bird/bird_up2.png' % ICON_DIR),
                      ('%s/monsters/bird/bird_up3.png' % ICON_DIR),
                      ('%s/monsters/bird/bird_up2.png' % ICON_DIR)]

ANIMATION_BIRDFLYDOWN = [('%s/monsters/bird/bird_down1.png' % ICON_DIR),
                        ('%s/monsters/bird/bird_down2.png' % ICON_DIR),
                        ('%s/monsters/bird/bird_down3.png' % ICON_DIR),
                        ('%s/monsters/bird/bird_down2.png' % ICON_DIR)]

# Анимации для птицы
ANIMATION_PURSUER_DELAY = 0.25
ANIMATION_PURSUERFLYLEFT  = [('%s/monsters/pursuer/pursuer_left1.gif' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_left2.gif' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_left3.gif' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_left2.gif' % ICON_DIR)]

ANIMATION_PURSUERFLYRIGHT = [('%s/monsters/pursuer/pursuer_right1.png' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_right2.png' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_right3.png' % ICON_DIR),
                         ('%s/monsters/pursuer/pursuer_right2.png' % ICON_DIR)]

ANIMATION_PURSUERFLYUP = [('%s/monsters/pursuer/pursuer_up1.gif' % ICON_DIR),
                      ('%s/monsters/pursuer/pursuer_up2.gif' % ICON_DIR),
                      ('%s/monsters/pursuer/pursuer_up3.gif' % ICON_DIR),
                      ('%s/monsters/pursuer/pursuer_up2.gif' % ICON_DIR)]

ANIMATION_PURSUERFLYDOWN = [('%s/monsters/pursuer/pursuer_down1.gif' % ICON_DIR),
                        ('%s/monsters/pursuer/pursuer_down2.gif' % ICON_DIR),
                        ('%s/monsters/pursuer/pursuer_down3.gif' % ICON_DIR),
                        ('%s/monsters/pursuer/pursuer_down2.gif' % ICON_DIR)]

ANIMATION_WRAITHLEFT  = [('%s/monsters/wraith_l.png' % ICON_DIR)]
ANIMATION_WRAITHRIGHT = [('%s/monsters/wraith_r.png' % ICON_DIR)]

class Monster(sprite.Sprite): # Класс монстров
    def __init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.algorithm = algorithm
        self.startX = x # начальные координаты
        self.startY = y
        self.myPosX = -1
        self.myPosY = -1
        self.myPrevPosX = int(self.startX / 32)
        self.myPrevPosY = int(self.startY / 32)
        self.myTargetPosX = -1
        self.myTargetPosY = -1
        self.startMoveTime = startMoveTime #- 1
        self.moveTime = 0
        self.moveOnLeft = moveOnLeft
        self.moveOnRight = False
        self.moveOnUp = moveOnUp
        self.moveOnDown = False
        self.MOVE_SPEED = 32 #MOVE_SPEED
        self.index = -1
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        #self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        #self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = 0 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 0 # скорость движения по вертикали, 0 - не двигается

    def moveOn(self, left, right, up, down):
        if left == True and up == True:  # Движение влево-вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            self.myPosY -= 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True and up == True:  # Движение вправо-вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            self.myPosY -= 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True and down == True:  # Движение вправо-вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            self.myPosY += 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif left == True and down == True:  # Движение влево-вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            self.myPosY += 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif left == True:  # Движение влево в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX -= 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif right == True:  # Движение вправо в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosX += 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif up == True:  # Движение вверх в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosY -= 1
            #way[self.myPosY][self.myPosX] = 'M'

        elif down == True:  # Движение вниз в матрице
            #way[self.myPosY][self.myPosX] = '0'
            self.myPrevPosX = self.myPosX
            self.myPrevPosY = self.myPosY
            self.myPosY += 1
            #way[self.myPosY][self.myPosX] = 'M'


    def monsterPatrolWay (self, monWay: List[List[int]]):
        if self.moveOnUp == True or self.moveOnDown == True:
            number = 0
            for i in range(len(monWay)):
                if i == 0:
                    1
                else:
                    if self.moveOnUp == True and self.moveOnDown == False:
                        if monWay[self.myPosY - i][self.myPosX] != 'B' and monWay[self.myPosY - i][self.myPosX] != 'W':
                            monWay[self.myPosY - i][self.myPosX] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                        else:
                            number = i
                            break
                    if self.moveOnUp == False and self.moveOnDown == True:
                        if monWay[self.myPosY + i][self.myPosX] != 'B' and monWay[self.myPosY + i][self.myPosX] != 'W':
                            monWay[self.myPosY + i][self.myPosX] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                        else:
                            number = i
                            break
                #print (i)
            for i in range(len(monWay)):
                if i == 0:
                    1
                else:
                    if self.moveOnUp == True and self.moveOnDown == False:
                        if monWay[self.myPosY + i][self.myPosX] != 'B' and monWay[self.myPosY + i][self.myPosX] != 'W':
                            #monWay[self.myPosY - i][self.myPosX] = 'M' + str(i)
                            monWay[self.myPosY + i][self.myPosX] = (number-1)*(self.startMoveTime + 1)*2 + i*(self.startMoveTime + 1)  + self.moveTime - self.startMoveTime
                        else:
                            break
                    if self.moveOnUp == False and self.moveOnDown == True:
                        if monWay[self.myPosY - i][self.myPosX] != 'B' and monWay[self.myPosY - i][self.myPosX] != 'W':
                            #monWay[self.myPosY + i][self.myPosX] = 'M' + str(i)
                            monWay[self.myPosY - i][self.myPosX] = (number-1)*(self.startMoveTime + 1)*2 + i*(self.startMoveTime + 1)  + self.moveTime - self.startMoveTime
                        else:
                            break
        if self.moveOnLeft == True or self.moveOnRight == True:
            number = 0
            for i in range(len(monWay[0])):
                if i == 0:
                    1
                else:
                    if self.moveOnLeft == True and self.moveOnRight == False:
                        if monWay[self.myPosY][self.myPosX - i] != 'B' and monWay[self.myPosY][self.myPosX - i] != 'W':
                            monWay[self.myPosY][self.myPosX - i] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                        else:
                            number = i
                            break
                    if self.moveOnLeft == False and self.moveOnRight == True:
                        if monWay[self.myPosY][self.myPosX + i] != 'B' and monWay[self.myPosY][self.myPosX + i] != 'W':
                            monWay[self.myPosY][self.myPosX + i] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                        else:
                            number = i
                            break
                #print (i)
            for i in range(len(monWay[0])):
                if i == 0:
                    1
                else:
                    if self.moveOnLeft == True and self.moveOnRight == False:
                        if monWay[self.myPosY][self.myPosX + i] != 'B' and monWay[self.myPosY][self.myPosX + i] != 'W':
                            monWay[self.myPosY][self.myPosX + i] = (number-1)*(self.startMoveTime + 1)*2 + i*(self.startMoveTime + 1)  + self.moveTime - self.startMoveTime
                        else:
                            break
                    if self.moveOnLeft == False and self.moveOnRight == True:
                        if monWay[self.myPosY][self.myPosX - i] != 'B' and monWay[self.myPosY][self.myPosX - i] != 'W':
                            monWay[self.myPosY][self.myPosX - i] = (number-1)*(self.startMoveTime + 1)*2 + i*(self.startMoveTime + 1)  + self.moveTime - self.startMoveTime
                        else:
                            break

    def patrolMove(self, hero, way: List[List[int]]):
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

        Monster.moveOn(self, self.left, self.right, self.up, self.down)
        self.moveTime = self.startMoveTime  #32/self.MOVE_SPEED - 1 Для плавного движения



    def monsterRandWay(self, monWay: List[List[int]]):
        if monWay[self.myPosY - 1][self.myPosX] != 'B' and monWay[self.myPosY - 1][self.myPosX] != 'W':
            monWay[self.myPosY - 1][self.myPosX] = self.moveTime + 1
        if monWay[self.myPosY + 1][self.myPosX] != 'B' and monWay[self.myPosY + 1][self.myPosX] != 'W':
            monWay[self.myPosY + 1][self.myPosX] = self.moveTime + 1
        if monWay[self.myPosY][self.myPosX + 1] != 'B' and monWay[self.myPosY][self.myPosX + 1] != 'W':
            monWay[self.myPosY][self.myPosX + 1] = self.moveTime + 1
        if monWay[self.myPosY][self.myPosX - 1] != 'B' and monWay[self.myPosY][self.myPosX - 1] != 'W':
            monWay[self.myPosY][self.myPosX - 1] = self.moveTime + 1

    def randMove(self, hero, way: List[List[int]]):
        number = random.randint(1, 4)
        # print('Число: ' + str(number))

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.moveOnLeft = False
        self.moveOnRight = False
        self.moveOnUp = False
        self.moveOnDown = False

        while self.left != True and self.right != True and self.up != True and self.down != True:
            if number == 1:  # Условие для прохода влево
                if way[self.myPosY][self.myPosX - 1] != 'B' and way[self.myPosY][self.myPosX - 1] != 'W':
                    self.left = True
                    self.moveOnLeft = True
                    # print("Left")
                else:
                    number = random.randint(1, 4)
                    # print("Stop: Left")  # number = 10

            elif number == 2:  # Условие для прохода вправо
                if way[self.myPosY][self.myPosX + 1] != 'B' and way[self.myPosY][self.myPosX + 1] != 'W':
                    self.right = True
                    self.moveOnRight = True
                    # print("Right")
                else:
                    number = random.randint(1, 4)
                    # print("Stop: Right")  # number = 10

            elif number == 3:  # Условие для прохода вверх
                if way[self.myPosY - 1][self.myPosX] != 'B' and way[self.myPosY - 1][self.myPosX] != 'W':
                    self.up = True
                    self.moveOnUp = True
                    # print("Up")
                else:
                    number = random.randint(1, 4)
                    # print("Stop: Up")  # number = 10

            elif number == 4:  # Условие для прохода вниз
                if way[self.myPosY + 1][self.myPosX] != 'B' and way[self.myPosY + 1][self.myPosX] != 'W':
                    self.down = True
                    self.moveOnDown = True
                    # print("Down")
                else:
                    number = random.randint(1, 4)
                    # print("Stop: Down")  # number = 10

        Monster.moveOn(self, self.left, self.right, self.up, self.down)
        self.moveTime = self.startMoveTime  # 32/self.MOVE_SPEED - 1 Для плавного движения



    def monsterPendingWay(self, monWay: List[List[int]]):
        if self.myTargetPosX != self.myPosX or self.myTargetPosY != self.myPosY:
            #if self.moveOnUp == True or self.moveOnDown == True: #Так же если убираю случайное блуждание скорее всего потребуется вернуть и закомменченое внутри
                for i in range(len(monWay)):
                    if i == 0: 1
                    else:
                        if self.myPosY >= self.myTargetPosY: # and self.moveOnUp == True and self.moveOnDown == False:
                            if self.myPosY - i >= self.myTargetPosY:
                                monWay[self.myPosY - i][self.myPosX] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                            else: break
                        if self.myPosY <= self.myTargetPosY: # and self.moveOnUp == False and self.moveOnDown == True:
                            if self.myPosY + i <= self.myTargetPosY:
                                monWay[self.myPosY + i][self.myPosX] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                            else: break
            #if self.moveOnLeft == True or self.moveOnRight == True: #Так же если убираю случайное блуждание скорее всего потребуется вернуть и закомменченое внутри
                for i in range(len(monWay[0])):
                    if i == 0: 1
                    else:
                        if self.myPosX >= self.myTargetPosX: # and self.moveOnLeft == True and self.moveOnRight == False:
                            if self.myPosX - i >= self.myTargetPosX:
                                monWay[self.myPosY][self.myPosX - i] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                            else: break
                        if self.myPosX + i <= self.myTargetPosX: # and self.moveOnLeft == False and self.moveOnRight == True:
                            if self.myPosX + i <= self.myTargetPosX:
                                monWay[self.myPosY][self.myPosX + i] = i*(self.startMoveTime + 1) + self.moveTime - self.startMoveTime
                            else: break

        elif self.myTargetPosX == self.myPosX and self.myTargetPosY == self.myPosY: #self.moveTime <= 0 and
            if monWay[self.myPosY - 1][self.myPosX] != 'B' and monWay[self.myPosY - 1][self.myPosX] != 'W':
                monWay[self.myPosY - 1][self.myPosX] = self.moveTime + 1 #Если убираю случайное блуждание, то ставлю здесь #1
            if monWay[self.myPosY + 1][self.myPosX] != 'B' and monWay[self.myPosY + 1][self.myPosX] != 'W':
                monWay[self.myPosY + 1][self.myPosX] = self.moveTime + 1 #Если убираю случайное блуждание, то ставлю здесь #1
            if monWay[self.myPosY][self.myPosX - 1] != 'B' and monWay[self.myPosY][self.myPosX - 1] != 'W':
                monWay[self.myPosY][self.myPosX - 1] = self.moveTime + 1 #Если убираю случайное блуждание, то ставлю здесь #1
            if monWay[self.myPosY][self.myPosX + 1] != 'B' and monWay[self.myPosY][self.myPosX + 1] != 'W':
                monWay[self.myPosY][self.myPosX + 1] = self.moveTime + 1 #Если убираю случайное блуждание, то ставлю здесь #1

    def pendingMove(self, monWay: List[List[int]], way: List[List[int]]):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        #self.moveOnLeft = False
        #self.moveOnRight = False
        #self.moveOnUp = False
        #self.moveOnDown = False
        #print("TargetPosX: " + str(self.myTargetPosX) + "    myPosX: " + str(self.myPosX))
        #print("TargetPosY: " + str(self.myTargetPosY) + "    myPosY: " + str(self.myPosY))
        if (self.myTargetPosX != self.myPosX) or (self.myTargetPosY != self.myPosY):
            #Сюда можно целиком переместить checkForPendingMove, но там работает быстрее за счет постоянного пробегания moveTime
            if self.myPosX > self.myTargetPosX:
                self.left = True
                self.moveOnLeft = True
                self.moveOnRight = False
                self.moveOnUp = False
                self.moveOnDown = False
            elif self.myPosX < self.myTargetPosX:
                self.right = True
                self.moveOnRight = True
                self.moveOnLeft = False
                self.moveOnUp = False
                self.moveOnDown = False
            elif self.myPosY < self.myTargetPosY:
                self.down = True
                self.moveOnDown = True
                self.moveOnLeft = False
                self.moveOnRight = False
                self.moveOnUp = False
            elif self.myPosY > self.myTargetPosY:
                self.up = True
                self.moveOnUp = True
                self.moveOnLeft = False
                self.moveOnRight = False
                self.moveOnDown = False
        else:
            stopUp = False
            stopDown = False
            stopLeft = False
            stopRight = False
            for i in range(len(monWay)):
                if i == 0:
                    1
                else:
                    if  stopUp == False:
                        if monWay[self.myPosY - i][self.myPosX] != 'B' and monWay[self.myPosY - i][self.myPosX] != 'W':
                            if way[self.myPosY - i][self.myPosX] == 'H':
                                self.myTargetPosX = self.myPosX
                                self.myTargetPosY = self.myPosY - i
                                self.up = True
                                self.moveOnUp = True
                                self.moveOnLeft = False
                                self.moveOnRight = False
                                self.moveOnDown = False
                        else: stopUp = True
                    if stopDown == False:
                        if monWay[self.myPosY + i][self.myPosX] != 'B' and monWay[self.myPosY + i][self.myPosX] != 'W':
                            if way[self.myPosY + i][self.myPosX] == 'H':
                                self.myTargetPosX = self.myPosX
                                self.myTargetPosY = self.myPosY + i
                                self.down = True
                                self.moveOnDown = True
                                self.moveOnLeft = False
                                self.moveOnRight = False
                                self.moveOnUp = False
                        else: stopDown = True
            for i in range(len(monWay[0])):
                if i == 0:
                    1
                else:
                    if  stopLeft == False:
                        if monWay[self.myPosY][self.myPosX - i] != 'B' and monWay[self.myPosY][self.myPosX - i] != 'W':
                            if way[self.myPosY][self.myPosX - i] == 'H':
                                self.myTargetPosX = self.myPosX - i
                                self.myTargetPosY = self.myPosY
                                self.left = True
                                self.moveOnLeft = True
                                self.moveOnRight = False
                                self.moveOnUp = False
                                self.moveOnDown = False
                        else: stopLeft = True
                    if stopRight == False:
                        if monWay[self.myPosY][self.myPosX + i] != 'B' and monWay[self.myPosY][self.myPosX + i] != 'W':
                            if way[self.myPosY][self.myPosX + i] == 'H':
                                self.myTargetPosX = self.myPosX + i
                                self.myTargetPosY = self.myPosY
                                self.right = True
                                self.moveOnRight = True
                                self.moveOnLeft = False
                                self.moveOnUp = False
                                self.moveOnDown = False
                        else: stopRight = True

        #Если не видим героя, то делаем шаг в случайную сторону
        if self.myTargetPosX == self.myPosX and self.myTargetPosY == self.myPosY:
            number = random.randint(1, 4)
            # print('Число: ' + str(number))

            while self.left != True and self.right != True and self.up != True and self.down != True:
                if number == 1:  # Условие для прохода влево
                    if way[self.myPosY][self.myPosX - 1] != 'B' and way[self.myPosY][self.myPosX - 1] != 'W':
                        self.left = True
                        self.myTargetPosX = self.myPosX - 1
                        self.myTargetPosY = self.myPosY
                        self.moveOnLeft = True
                        self.moveOnRight = False
                        self.moveOnUp = False
                        self.moveOnDown = False
                        # print("Left")
                    else:
                        number = random.randint(1, 4)
                        # print("Stop: Left")  # number = 10

                elif number == 2:  # Условие для прохода вправо
                    if way[self.myPosY][self.myPosX + 1] != 'B' and way[self.myPosY][self.myPosX + 1] != 'W':
                        self.right = True
                        self.myTargetPosX = self.myPosX + 1
                        self.myTargetPosY = self.myPosY
                        self.moveOnRight = True
                        self.moveOnLeft = False
                        self.moveOnUp = False
                        self.moveOnDown = False
                        # print("Right")
                    else:
                        number = random.randint(1, 4)
                        # print("Stop: Right")  # number = 10

                elif number == 3:  # Условие для прохода вверх
                    if way[self.myPosY - 1][self.myPosX] != 'B' and way[self.myPosY - 1][self.myPosX] != 'W':
                        self.up = True
                        self.myTargetPosX = self.myPosX
                        self.myTargetPosY = self.myPosY - 1
                        self.moveOnUp = True
                        self.moveOnLeft = False
                        self.moveOnRight = False
                        self.moveOnDown = False
                        # print("Up")
                    else:
                        number = random.randint(1, 4)
                        # print("Stop: Up")  # number = 10

                elif number == 4:  # Условие для прохода вниз
                    if way[self.myPosY + 1][self.myPosX] != 'B' and way[self.myPosY + 1][self.myPosX] != 'W':
                        self.down = True
                        self.myTargetPosX = self.myPosX
                        self.myTargetPosY = self.myPosY + 1
                        self.moveOnDown = True
                        self.moveOnLeft = False
                        self.moveOnRight = False
                        self.moveOnUp = False
                        # print("Down")
                    else:
                        number = random.randint(1, 4)

        Monster.moveOn(self, self.left, self.right, self.up, self.down)
        self.moveTime = self.startMoveTime #(self.startMoveTime + 1)*number - 1

    def checkForPendingMove(self, monWay, way):
        stopUp = False
        stopDown = False
        stopLeft = False
        stopRight = False
        for i in range(len(monWay)):
            if i == 0:
                1
            else:
                #print('Q: X=' + str(self.myPosX) + ' Y=' + str(self.myPosY - i) + ' way: ' + str(way[self.myPosY - i][self.myPosX]))
                if stopUp == False:
                    if monWay[self.myPosY - i][self.myPosX] != 'B' and monWay[self.myPosY - i][self.myPosX] != 'W':
                        if way[self.myPosY - i][self.myPosX] == 'H':
                            self.myTargetPosX = self.myPosX
                            self.myTargetPosY = self.myPosY - i
                    else:
                        stopUp = True
                if stopDown == False:
                    if monWay[self.myPosY + i][self.myPosX] != 'B' and monWay[self.myPosY + i][self.myPosX] != 'W':
                        if way[self.myPosY + i][self.myPosX] == 'H':
                            self.myTargetPosX = self.myPosX
                            self.myTargetPosY = self.myPosY + i
                    else:
                        stopDown = True
        for i in range(len(monWay[0])):
            if i == 0:
                1
            else:
                #print('Q: X=' + str(self.myPosX - i) + ' Y=' + str(self.myPosY) + ' way: ' + str(way[self.myPosY][self.myPosX - i]))
                if stopLeft == False:
                    if monWay[self.myPosY][self.myPosX - i] != 'B' and monWay[self.myPosY][self.myPosX - i] != 'W':
                        if way[self.myPosY][self.myPosX - i] == 'H':
                            self.myTargetPosX = self.myPosX - i
                            self.myTargetPosY = self.myPosY
                    else:
                        stopLeft = True
                if stopRight == False:
                    if monWay[self.myPosY][self.myPosX + i] != 'B' and monWay[self.myPosY][self.myPosX + i] != 'W':
                        if way[self.myPosY][self.myPosX + i] == 'H':
                            self.myTargetPosX = self.myPosX + i
                            self.myTargetPosY = self.myPosY
                    else:
                        stopRight = True



    def pursueMove(self, hero, way: List[List[int]]):
        1



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
                    check = blocks.BigEnergy.moveEnergy(p, platforms, way)
                    #Проверка и отрисовка, нужны Hero и Way
                    #while (hero.rect.x == p.rect.x and hero.rect.y == p.rect.y) or (hero.startX == p.rect.x and hero.startY == p.rect.y) or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == 'H') or (blocks.Exit.myPosX == int(p.rect.x/32) and blocks.Exit.myPosY == int(p.rect.y/32)) or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == 'M') or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == 'B' or (way[int(p.rect.y / 32)][int(p.rect.x / 32)] == '*')): #or (self.myPosX == int(p.rect.x / 32) and self.myPosY == int(p.rect.y / 32)):
                    while check == False:
                        check = blocks.BigEnergy.moveEnergy(p, platforms, way)
                        #blocks.BigEnergy.teleporting(p, 32, 32 * random.randint(4, 5), platforms, True)
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
    def __init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime)
        self.name = 'Bat'
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

class Bird(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime)
        self.name = 'Bird'
        #self.rect = Rect(x, y, 29, 29)
        # Анимация полета направо
        boltAnim = []
        for anim in ANIMATION_BIRDFLYLEFT:
            boltAnim.append((anim, ANIMATION_BIRD_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        # Анимация полета налево
        boltAnim = []
        for anim in ANIMATION_BIRDFLYRIGHT:
            boltAnim.append((anim, ANIMATION_BIRD_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация полета наверх
        boltAnim = []
        for anim in ANIMATION_BIRDFLYUP:
            boltAnim.append((anim, ANIMATION_BIRD_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        # Анимация полета вниз
        boltAnim = []
        for anim in ANIMATION_BIRDFLYDOWN:
            boltAnim.append((anim, ANIMATION_BIRD_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

class Pursuer(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime)
        self.name = 'Pursuer'
        #self.rect = Rect(x, y, 29, 29)
        # Анимация полета направо
        boltAnim = []
        for anim in ANIMATION_PURSUERFLYLEFT:
            boltAnim.append((anim, ANIMATION_PURSUER_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        # Анимация полета налево
        boltAnim = []
        for anim in ANIMATION_PURSUERFLYRIGHT:
            boltAnim.append((anim, ANIMATION_PURSUER_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация полета наверх
        boltAnim = []
        for anim in ANIMATION_PURSUERFLYUP:
            boltAnim.append((anim, ANIMATION_PURSUER_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        # Анимация полета вниз
        boltAnim = []
        for anim in ANIMATION_PURSUERFLYDOWN:
            boltAnim.append((anim, ANIMATION_PURSUER_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

class Wraith(Monster):
    def __init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime):
        Monster.__init__(self, x, y, moveOnLeft, moveOnUp, algorithm, startMoveTime)
        self.name = 'Wraith'
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
