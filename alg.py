#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
import blocks
import pyganim
import monsters
import os
import random
import maps
import player
from pygame import *
import pygame

def algRandom(hero, way: List[List[int]]):
    maps.printInfo (hero, way)
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
    moveOn (left, right, up, down, hero, way)
    moveTime = 3 #*random.randint(1, 4)
    return left, right, up, down, moveTime

def moveOn (left, right, up, down, hero, way: List[List[int]]):
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



def algWave (hero, way: List[List[int]]):
    maps.printInfo (hero, way)
    left = False
    right = False
    up = False
    down = False
    moveTimeFlag = False

    if way[hero.myPosY][hero.myPosX - 1] == '+' or way[hero.myPosY][hero.myPosX - 1] == 'W' or way[hero.myPosY][hero.myPosX - 1] == 'E':
        if way[hero.myPosY][hero.myPosX - 1] == 'W': moveTimeFlag = True
        left = True
        print("Left")

    elif way[hero.myPosY][hero.myPosX + 1] == '+' or way[hero.myPosY][hero.myPosX + 1] == 'W' or way[hero.myPosY][hero.myPosX + 1] == 'E':
        if way[hero.myPosY][hero.myPosX + 1] == 'W': moveTimeFlag = True
        right = True
        print("Right")

    elif way[hero.myPosY - 1][hero.myPosX] == '+' or way[hero.myPosY - 1][hero.myPosX] == 'W' or way[hero.myPosY - 1][hero.myPosX] == 'E':
        if way[hero.myPosY - 1][hero.myPosX] == 'W': moveTimeFlag = True
        up = True
        print("Up")

    elif way[hero.myPosY + 1][hero.myPosX] == '+' or way[hero.myPosY + 1][hero.myPosX] == 'W' or way[hero.myPosY + 1][hero.myPosX] == 'E':
        if way[hero.myPosY + 1][hero.myPosX] == 'W': moveTimeFlag = True
        down = True
        print("Down")

    #Скорее всего тоже верно
    elif way[hero.myPosY + 1][hero.myPosX + 1] == '+' or way[hero.myPosY + 1][hero.myPosX + 1] == 'W' or way[hero.myPosY + 1][hero.myPosX + 1] == 'E':
        if way[hero.myPosY + 1][hero.myPosX + 1] == 'W': moveTimeFlag = True
        right = True
        down = True
        print("Right-Down")

    elif way[hero.myPosY - 1][hero.myPosX + 1] == '+' or way[hero.myPosY - 1][hero.myPosX + 1] == 'W' or way[hero.myPosY - 1][hero.myPosX + 1] == 'E':
        if way[hero.myPosY - 1][hero.myPosX + 1] == 'W': moveTimeFlag = True
        right = True
        up = True
        print("Right-Up")

    elif way[hero.myPosY - 1][hero.myPosX - 1] == '+' or way[hero.myPosY - 1][hero.myPosX - 1] == 'W' or way[hero.myPosY - 1][hero.myPosX - 1] == 'E':
        if way[hero.myPosY - 1][hero.myPosX - 1] == 'W': moveTimeFlag = True
        left = True
        up = True
        print("Left-Up")

    elif way[hero.myPosY + 1][hero.myPosX - 1] == '+' or way[hero.myPosY + 1][hero.myPosX - 1] == 'W' or way[hero.myPosY + 1][hero.myPosX - 1] == 'E':
        if way[hero.myPosY + 1][hero.myPosX - 1] == 'W': moveTimeFlag = True
        left = True
        down = True
        print("Left-Down")

    moveOn(left, right, up, down, hero, way)
    if moveTimeFlag == True:
        moveTime = 0
    else: moveTime = 3
    return left, right, up, down, moveTime

def algWaveFindExit (symbol, hero, way: List[List[int]]):
    #Сперва ищем все пути до портала
    n = 1
    #number = 0
    exitFlag = False
    nextStep = False
    #print("Позиция  ГЕРОЯ  в массиве  X: " + str(hero.myPosX) + "  Y: " + str(hero.myPosY))
    x = hero.myPosX#blocks.Exit.myPosX#hero.myPosX
    y = hero.myPosY#blocks.Exit.myPosY#hero.myPosY
    exitFlag = findWays(y, x, n, exitFlag, 0, symbol, way)
    while exitFlag != True:
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == n:
                    exitFlag = findWays(i, j, n+1, exitFlag, 0, symbol, way) # посылаю координаты y и x; следующее число; проверку на конец алг; знак который буду менять; что ищу; массив
        if exitFlag != True:
            n += 1

    #maps.printInfo(hero, way) # Выводим информацию о посланной волне
    #Теперь записываем путь для последующего движения
    #print ("Steps of alghoritm: N="+ str(n))
    exitFlag = False
    nextStep = False
    if symbol == 'E':
        x = blocks.BigEnergy.myPosX#hero.myPosX
        y = blocks.BigEnergy.myPosY#hero.myPosY
        print('BigEnergy.myPosX: ' + str(blocks.BigEnergy.myPosX) + '   BigEnergy.myPosY: ' + str(blocks.BigEnergy.myPosY))
    elif symbol == 'W':
        x = blocks.Exit.myPosX#hero.myPosX
        y = blocks.Exit.myPosY#hero.myPosY
    #exitFlag = findWays(y, x, '+', exitFlag, n, 'H', way)
    exitFlag, nextStep = findBackWay(y, x, '+', exitFlag, n, 'H', nextStep, way)
    n -= 1
    nextStep = False
    while exitFlag != True:
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == '+':
                    #exitFlag = findWays(i, j, '+', exitFlag, n, 'H', way)
                    if nextStep == True:
                        break
                    else: exitFlag, nextStep = findBackWay(i, j, '+',exitFlag, n, 'H', nextStep, way)
            if nextStep == True:
                break
        nextStep = False
        if exitFlag != True:
            n -= 1
    #maps.printInfo(hero, way) #Выводим информацию о карте после построения маршрута


def findWays (y, x, n, exitFlag, checkSym, symbol, way: List[List[int]]):
    #Вверх
    if (y - 1 >= 0 and way[y - 1][x] != 'B' and way[y - 1][x] == checkSym) or way[y - 1][x] == symbol:
        if way[y - 1][x] == symbol:
            exitFlag = True
        else:
            way[y - 1][x] = n

    #Вниз
    if (y + 1 < len(way) and way[y + 1][x] != 'B' and way[y + 1][x] == checkSym) or way[y + 1][x] == symbol:
        if way[y + 1][x] == symbol:
            exitFlag = True
        else:
            way[y + 1][x] = n

    #Влево
    if (x - 1 >= 0 and way[y][x - 1] != 'B' and way[y][x - 1] == checkSym) or way[y][x - 1] == symbol:
        if way[y][x - 1] == symbol:
            exitFlag = True
        else:
            way[y][x - 1] = n

    #Вправо
    if (x + 1 < len(way[y]) and way[y][x + 1] != 'B' and way[y][x + 1] == checkSym) or way[y][x + 1] == symbol:
        if way[y][x + 1] == symbol:
            exitFlag = True
        else:
            way[y][x + 1] = n

    #Вправо-Вниз
    if (x + 1 < len(way[y]) and y + 1 < len(way) and way[y][x + 1] != 'B' and way[y + 1][x] != 'B' and way[y + 1][x + 1] == checkSym) or (way[y + 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y + 1][x] != 'B'):
        if way[y + 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y + 1][x] != 'B':
            exitFlag = True
        else:
            way[y + 1][x + 1] = n

    #Вправо-Вверх
    if (x + 1 < len(way[y]) and y - 1 >= 0 and way[y][x + 1] != 'B' and way[y - 1][x] != 'B' and way[y - 1][x + 1] == checkSym) or (way[y - 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y - 1][x] != 'B'):
        if way[y - 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y - 1][x] != 'B':
            exitFlag = True
        else:
            way[y - 1][x + 1] = n

    #Влево-Вниз
    if (x - 1 >= 0 and y + 1 < len(way) and way[y][x - 1] != 'B' and way[y + 1][x] != 'B' and way[y + 1][x - 1] == checkSym) or (way[y + 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y + 1][x] != 'B'):
        if way[y + 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y + 1][x] != 'B':
            exitFlag = True
        else:
            way[y + 1][x - 1] = n

    #Влево-Вверх
    if (x - 1 >= 0 and y - 1 >= 0 and way[y][x - 1] != 'B' and way[y - 1][x] != 'B' and way[y - 1][x - 1] == checkSym) or (way[y - 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y - 1][x] != 'B'):
        if way[y - 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y - 1][x] != 'B':
            exitFlag = True
        else:
            way[y - 1][x - 1] = n
    return exitFlag


def findBackWay (y, x, n, exitFlag, checkSym, symbol, nextStep,  way: List[List[int]]):
    #Влево-Вверх
    if (x - 1 >= 0 and y - 1 >= 0 and way[y][x - 1] != 'B' and way[y - 1][x] != 'B' and way[y - 1][x - 1] == checkSym) or (way[y - 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y - 1][x] != 'B'):
        if way[y - 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y - 1][x] != 'B':
            exitFlag = True
        else:
            way[y - 1][x - 1] = n
        nextStep = True

    #Влево-Вниз
    elif (x - 1 >= 0 and y + 1 < len(way) and way[y][x - 1] != 'B' and way[y + 1][x] != 'B' and way[y + 1][x - 1] == checkSym) or (way[y + 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y + 1][x] != 'B'):
        if way[y + 1][x - 1] == symbol and way[y][x - 1] != 'B' and way[y + 1][x] != 'B':
            exitFlag = True
        else:
            way[y + 1][x - 1] = n
        nextStep = True

    #Вправо-Вверх
    elif (x + 1 < len(way[y]) and y - 1 >= 0 and way[y][x + 1] != 'B' and way[y - 1][x] != 'B' and way[y - 1][x + 1] == checkSym) or (way[y - 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y - 1][x] != 'B'):
        if way[y - 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y - 1][x] != 'B':
            exitFlag = True
        else:
            way[y - 1][x + 1] = n
        nextStep = True

    #Вправо-Вниз
    elif (x + 1 < len(way[y]) and y + 1 < len(way) and way[y][x + 1] != 'B' and way[y + 1][x] != 'B' and way[y + 1][x + 1] == checkSym) or (way[y + 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y + 1][x] != 'B'):
        if way[y + 1][x + 1] == symbol and way[y][x + 1] != 'B' and way[y + 1][x] != 'B':
            exitFlag = True
        else:
            way[y + 1][x + 1] = n
        nextStep = True

    #Вверх
    elif (y - 1 >= 0 and way[y - 1][x] != 'B' and way[y - 1][x] == checkSym) or way[y - 1][x] == symbol:
        if way[y - 1][x] == symbol:
            exitFlag = True
        else:
            way[y - 1][x] = n
        nextStep = True

    #Вниз
    elif (y + 1 < len(way) and way[y + 1][x] != 'B' and way[y + 1][x] == checkSym) or way[y + 1][x] == symbol:
        if way[y + 1][x] == symbol:
            exitFlag = True
        else:
            way[y + 1][x] = n
        nextStep = True

    #Влево
    elif (x - 1 >= 0 and way[y][x - 1] != 'B' and way[y][x - 1] == checkSym) or way[y][x - 1] == symbol:
        if way[y][x - 1] == symbol:
            exitFlag = True
        else:
            way[y][x - 1] = n
        nextStep = True

    #Вправо
    elif (x + 1 < len(way[y]) and way[y][x + 1] != 'B' and way[y][x + 1] == checkSym) or way[y][x + 1] == symbol:
        if way[y][x + 1] == symbol:
            exitFlag = True
        else:
            way[y][x + 1] = n
        nextStep = True
    return exitFlag, nextStep

