#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
import blocks
import pyganim
import monsters
import os
import random
import player
from pygame import *
import pygame

def testMapRandom(left, right, up, down, moveTime, hero, platforms, way: List[List[int]]):
    print('\nИнформация об алгоритме: ')
    print ("Я вижу:")
    for i in range(len(way)):
        for j in range(len(way[i])):
            #if way[i][j] == 3:
            #    hero.myPosX = j
            #    hero.myPosY = i
            #if way[i][j] == 2:
            #    hero.exitX = j
            #    hero.exitY = i
                #hero.exit[1][1] = way[i][j]
                #print(hero.exit, end=' ')
            print(way[i][j], end=' ')
        print()
    print('')
    print("Позиция  ГЕРОЯ  в массиве  X: " + str(hero.myPosX) + "  Y: " + str(hero.myPosY))
    print("Позиция ПОРТАЛА в массиве  X: " + str(blocks.Exit.myPosX)  + "  Y: " + str(blocks.Exit.myPosY))
    left = False
    right = False
    up = False
    down = False
    number = random.randint(1, 8)
    print('Число: ' + str(number))

    if number == 5: # Условие для прохода влево-вверх
        if (way[hero.myPosY][hero.myPosX-1] != 'B') and (way[hero.myPosY-1][hero.myPosX] != 'B') and (way[hero.myPosY-1][hero.myPosX-1] != 'B'):
            left = True
            up = True
            print("Left-Up")
        else: print("Stop: Left-Up") #number = 10

    elif number == 6: # Условие для прохода вправо-вверх
        if (way[hero.myPosY][hero.myPosX+1] != 'B') and (way[hero.myPosY-1][hero.myPosX] != 'B') and (way[hero.myPosY-1][hero.myPosX+1] != 'B'):
            right = True
            up = True
            print("Right-Up")
        else: print("Stop: Right-Up") #number = 10

    elif number == 7: # Условие для прохода влево-вниз
        if (way[hero.myPosY][hero.myPosX-1] != 'B') and (way[hero.myPosY+1][hero.myPosX] != 'B') and (way[hero.myPosY+1][hero.myPosX-1] != 'B'):
            left = True
            down = True
            print("Left-Down")
        else: print("Stop: Left-Down") #number = 10

    elif number == 8: # Условие для прохода влево-вниз
        if (way[hero.myPosY][hero.myPosX+1] != 'B') and (way[hero.myPosY+1][hero.myPosX] != 'B') and (way[hero.myPosY+1][hero.myPosX+1] != 'B'):
            right = True
            down = True
            print("Right-Down")
        else: print("Stop: Right-Down") #number = 10

    elif number == 1: # Условие для прохода влево
        if (way[hero.myPosY][hero.myPosX-1] != 'B'):
            left = True
            print("Left")
        else: print("Stop: Left") #number = 10

    elif number == 2: # Условие для прохода вправо
        if (way[hero.myPosY][hero.myPosX+1] != 'B'):
            right = True
            print("Right")
        else: print("Stop: Right")#number = 10

    elif number == 3: # Условие для прохода вверх
        if (way[hero.myPosY-1][hero.myPosX] != 'B'):
            up = True
            print("Up")
        else: print("Stop: Up")#number = 10

    elif number == 4: # Условие для прохода вниз
        if (way[hero.myPosY+1][hero.myPosX] != 'B'):
            down = True
            print("Down")
        else: print("Stop: Down")#number = 10

    #pause = True
    #while pause:
    #    for e in pygame.event.get():  # Обрабатываем события
    #        if e.type == KEYUP and e.key == K_SPACE:
    #            pause = False
    #            print('Продолжаем!')
    #        if e.type == QUIT:
    #            raise SystemExit("QUIT")

    if left==True: #Движение влево в матрице
        way[hero.myPosY][hero.myPosX] = 'o'
        hero.myPosX -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    if right==True: #Движение вправо в матрице
        way[hero.myPosY][hero.myPosX] = 'o'
        hero.myPosX += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    if up == True: #Движение вверх в матрице
        way[hero.myPosY][hero.myPosX] = 'o'
        hero.myPosY -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    if down == True: #Движение вниз в матрице
        way[hero.myPosY][hero.myPosX] = 'o'
        hero.myPosY += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    moveTime = 3 #*random.randint(1, 4)
    return left, right, up, down, moveTime




