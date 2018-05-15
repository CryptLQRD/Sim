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
import numpy as np
import observations
from termcolor import colored

def moveOn (left, right, up, down, hero, way: List[List[int]]):
    if left==True and up==True: #Движение влево-вверх в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX -= 1
        hero.myPosY -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif right==True and up==True: #Движение вправо-вверх в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX += 1
        hero.myPosY -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif right==True and down==True: #Движение вправо-вниз в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX += 1
        hero.myPosY += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif left==True and down==True: #Движение влево-вниз в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX -= 1
        hero.myPosY += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif left==True: #Движение влево в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif right==True: #Движение вправо в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosX += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif up == True: #Движение вверх в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosY -= 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

    elif down == True: #Движение вниз в матрице
        way[hero.myPosY][hero.myPosX] = '0'
        hero.myPosY += 1
        if blocks.Exit.myPosY == hero.myPosY and blocks.Exit.myPosX == hero.myPosX:
            hero.myPosX = int(hero.startX / 32)
            hero.myPosY = int(hero.startY / 32)
        way[hero.myPosY][hero.myPosX] = 'H'

def identificationAlg (hero, way: List[List[int]], masMon):
    if True:
        hero.obsCount += 1
        depth = 100 # Стоит делить на moveTime отдельного монстра, иначе следует сделать переменные с сохранением предыдущих результатов (Пример stepX и stepY) При depth=60 и moveTime=4 step =15
        alg111Check = 20
        if hero.obsCount < depth:
            epi = 0
            counter = hero.obsCount
        else:
            counter = depth#
            epi = hero.obsCount - depth
        monCounter = -1
        print() #Пустой принт для удобства отображения в консоли
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == 'M':
                    monCounter += 1
                    print ('Индекс монстра: ' + str(monCounter))
                    observations.addObservation(hero.monInfo, observations.Observation(timestamp=hero.obsCount, x=j, y=i), index=monCounter)
                    #MoveTime
                    newTimestamp = -1
                    x = hero.monInfo[monCounter].observations[epi].x
                    y = hero.monInfo[monCounter].observations[epi].y
                    if hero.monInfo[monCounter].moveTime < 0:
                        for k in range(counter):
                            if x != hero.monInfo[monCounter].observations[epi + k].x or y != hero.monInfo[monCounter].observations[epi + k].y:
                                x = hero.monInfo[monCounter].observations[epi + k].x
                                y = hero.monInfo[monCounter].observations[epi + k].y
                                if newTimestamp != -1:
                                    hero.monInfo[monCounter].moveTime = hero.monInfo[monCounter].observations[epi + k].timestamp - newTimestamp
                                    newTimestamp = -1
                                else: newTimestamp = hero.monInfo[monCounter].observations[epi + k].timestamp
                    #Alg
                    x = hero.monInfo[monCounter].observations[epi].x
                    y = hero.monInfo[monCounter].observations[epi].y
                    stepX = 0
                    stepY = 0
                    if hero.monInfo[monCounter].alg < 0:
                        for k in range(counter):
                            if x != hero.monInfo[monCounter].observations[epi + k].x or y != hero.monInfo[monCounter].observations[epi + k].y:
                                if x != hero.monInfo[monCounter].observations[epi + k].x:
                                    stepX += 1 #Если поменялся X, то проверяем меняетлся ли Y
                                    stepY = 0
                                    x = hero.monInfo[monCounter].observations[epi + k].x
                                if y != hero.monInfo[monCounter].observations[epi + k].y:
                                    stepY += 1 #Если поменялся X, то проверяем меняетлся ли Y
                                    stepX = 0
                                    y = hero.monInfo[monCounter].observations[epi + k].y
                                # Alg 111
                                if stepX >= alg111Check or stepY >= alg111Check:
                                    final111algCheck = 0
                                    if stepX > alg111Check:
                                        for c in range(hero.obsCount):
                                            if hero.monInfo[monCounter].observations[0].y == hero.monInfo[monCounter].observations[c].y:
                                                final111algCheck += 1
                                                print('Monster with final111algCheck {} and hero.obsCount {}'.format(final111algCheck, hero.obsCount))
                                    elif stepY > alg111Check:
                                        for c in range(hero.obsCount):
                                            if hero.monInfo[monCounter].observations[0].x == hero.monInfo[monCounter].observations[c].x:
                                                final111algCheck += 1
                                                print('Monster with final111algCheck {} and hero.obsCount {}'.format(final111algCheck, hero.obsCount))
                                    if final111algCheck == hero.obsCount:
                                        hero.monInfo[monCounter].alg = 111
                                #print('Monster with stepX {} and stepY {}'.format(stepX, stepY))
                            #if newTimestamp == -1:
                            #    newTimestamp = hero.monInfo[monCounter].observations[epi + k].timestamp
                            #elif hero.monInfo[monCounter].moveTime == :
                            #    hero.monInfo[monCounter].moveTime = hero.monInfo[monCounter].observations[epi + k].timestamp - newTimestamp

                        #hero.monInfo[monCounter].observations[epi+k].x = epi

                    #observations.ObservedMonster(Alg, moveTime, observations.Observation)
                    #hero.monInfo[monCounter].observations[hero.obsCount].x = 90   #Аналог   monsters[0].observations[1].x = 90
                    #hero.monInfo[monCounter].alg = 111
                    if hero.obsCount % 10 == 0:
                        observations.print_all_observations(hero.monInfo)
                        #print(hero.monInfo[monCounter].observations[hero.obsCount])
                    #print(hero.monInfo[monCounter].alg)
    else: 1

    #maps.printHeroInfo (hero.monInfo)


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


def algWave (hero, way: List[List[int]]):
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

    elif (way[hero.myPosY + 1][hero.myPosX + 1] == '+' or way[hero.myPosY + 1][hero.myPosX + 1] == 'W' or way[hero.myPosY + 1][hero.myPosX + 1] == 'E') and (way[hero.myPosY + 1][hero.myPosX] != 'B' and way[hero.myPosY][hero.myPosX + 1] != 'B'):
        if way[hero.myPosY + 1][hero.myPosX + 1] == 'W': moveTimeFlag = True
        right = True
        down = True
        print("Right-Down")

    elif (way[hero.myPosY - 1][hero.myPosX + 1] == '+' or way[hero.myPosY - 1][hero.myPosX + 1] == 'W' or way[hero.myPosY - 1][hero.myPosX + 1] == 'E') and (way[hero.myPosY - 1][hero.myPosX] != 'B' and way[hero.myPosY][hero.myPosX + 1] != 'B'):
        if way[hero.myPosY - 1][hero.myPosX + 1] == 'W': moveTimeFlag = True
        right = True
        up = True
        print("Right-Up")

    elif (way[hero.myPosY - 1][hero.myPosX - 1] == '+' or way[hero.myPosY - 1][hero.myPosX - 1] == 'W' or way[hero.myPosY - 1][hero.myPosX - 1] == 'E') and (way[hero.myPosY - 1][hero.myPosX] != 'B' and way[hero.myPosY][hero.myPosX - 1] != 'B'):
        if way[hero.myPosY - 1][hero.myPosX - 1] == 'W': moveTimeFlag = True
        left = True
        up = True
        print("Left-Up")

    elif (way[hero.myPosY + 1][hero.myPosX - 1] == '+' or way[hero.myPosY + 1][hero.myPosX - 1] == 'W' or way[hero.myPosY + 1][hero.myPosX - 1] == 'E') and (way[hero.myPosY + 1][hero.myPosX] != 'B' and way[hero.myPosY][hero.myPosX - 1] != 'B'):
        if way[hero.myPosY + 1][hero.myPosX - 1] == 'W': moveTimeFlag = True
        left = True
        down = True
        print("Left-Down")

    moveOn(left, right, up, down, hero, way)
    #maps.printInfo (hero, way)
    if moveTimeFlag == True:
        moveTime = 0
    #elif hero.imSlow == True: moveTime = 10
    else: moveTime = hero.startMoveTime#4 #Для плавного движения moveTime = 3
    return left, right, up, down, moveTime

def algWaveFindExit (symbol, hero, way: List[List[int]], masBE: List[int], monWay: List[List[int]]):
    #Сперва ищем все пути до цели
    n = 1
    exitCounter = 0
    maxEC = len(way)*len(way[0])#50
    exitFlag = False
    x = hero.myPosX#blocks.Exit.myPosX#hero.myPosX
    y = hero.myPosY#blocks.Exit.myPosY#hero.myPosY
    exitFlag = findWays(y, x, n, exitFlag, 0, symbol, way)
    while exitFlag != True and exitCounter < maxEC:
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == n:
                    exitCounter = 0
                    exitFlag = findWays(i, j, n+1, exitFlag, 0, symbol, way) # посылаю координаты y и x; следующее число; проверку на конец алг; знак который буду менять; что ищу; массив
        exitCounter += 1
        if exitCounter > maxEC-1:
            print(colored("ВНИМАНИЕ:", 'red'), " Выход из поиска маршрута!   exitCounter=" + str(exitCounter))
        if exitFlag != True:
            n += 1
    #maps.printInfo(hero, way) # Выводим информацию о посланной волне

    #Теперь записываем путь для последующего движения
    exitFlag = False
    nextStep = False
    if (way[y][x+1] == 'E' or way[y+1][x] == 'E' or way[y][x-1] == 'E' or way[y-1][x] == 'E') \
            or (way[y + 1][x + 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M'))\
            or (way[y - 1][x + 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M')) \
            or (way[y + 1][x - 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M')) \
            or (way[y - 1][x - 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M')):
        exitFlag = True # Заканчиваем работу алгоритма т.к. энергия уже находится рядом с героем.
        #maps.printInfo(hero, way)
    elif symbol == 'E':
        print("Кол-во шагов алгоритма: N=" + str(n))
        for be in masBE:
            #if way[be.myPosY-1][be.myPosX] == n or way[be.myPosY][be.myPosX-1] == n or way[be.myPosY -1][be.myPosX-1] == n or way[be.myPosY -1][be.myPosX + 1] == n or way[be.myPosY][be.myPosX+1] == n or way[be.myPosY+1][be.myPosX+1] == n or way[be.myPosY +1][be.myPosX] == n or way[be.myPosY +1][be.myPosX-1] == n:
            if be.myPosX < 0 or be.myPosY < 0:
                1 # Ничего не делаем т.к. позиция энергии находится за картой, то мы ее игнорируем
            elif way[be.myPosY-1][be.myPosX] == n or way[be.myPosY][be.myPosX-1] == n or way[be.myPosY][be.myPosX+1] == n or way[be.myPosY +1][be.myPosX] == n \
                    or (way[be.myPosY + 1][be.myPosX + 1] == n and (way[be.myPosY + 1][be.myPosX] != 'B' and way[be.myPosY + 1][be.myPosX] != 'M') and (way[be.myPosY][be.myPosX + 1] != 'B' and way[be.myPosY][be.myPosX + 1] != 'M')) \
                    or (way[be.myPosY - 1][be.myPosX + 1] == n and (way[be.myPosY - 1][be.myPosX] != 'B' and way[be.myPosY - 1][be.myPosX] != 'M') and (way[be.myPosY][be.myPosX + 1] != 'B' and way[be.myPosY][be.myPosX + 1] != 'M')) \
                    or (way[be.myPosY + 1][be.myPosX - 1] == n and (way[be.myPosY + 1][be.myPosX] != 'B' and way[be.myPosY + 1][be.myPosX] != 'M') and (way[be.myPosY][be.myPosX - 1] != 'B' and way[be.myPosY][be.myPosX - 1] != 'M')) \
                    or (way[be.myPosY - 1][be.myPosX - 1] == n and (way[be.myPosY - 1][be.myPosX] != 'B' and way[be.myPosY - 1][be.myPosX] != 'M') and (way[be.myPosY][be.myPosX - 1] != 'B' and way[be.myPosY][be.myPosX - 1] != 'M')):
                x = be.myPosX
                y = be.myPosY
                print('Выбрана начальная точка: BigEnergy.myPosX: ' + str(be.myPosX) + '   BigEnergy.myPosY: ' + str(be.myPosY))
                #break
                #maps.printInfo(hero, way)
        exitFlag, nextStep = findBackWay(y, x, '+', exitFlag, n, 'H', nextStep, way, monWay)
    elif symbol == 'W':
        x = blocks.Exit.myPosX
        y = blocks.Exit.myPosY
        exitFlag, nextStep = findBackWay(y, x, '+', exitFlag, n, 'H', nextStep, way, monWay)

    n -= 1
    nextStep = False
    exitCounter = 0
    while exitFlag != True and exitCounter < maxEC:
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == '+':
                    if nextStep == True:
                        exitCounter = 0
                        break
                    else: exitFlag, nextStep = findBackWay(i, j, '+',exitFlag, n, 'H', nextStep, way, monWay)
            if nextStep == True:
                break
        exitCounter += 1
        if exitCounter > maxEC-1:
            print(colored("ВНИМАНИЕ:", 'red'), " Выход из прокладывания(+) маршрута!   exitCounter=" + str(exitCounter))
        nextStep = False
        if exitFlag != True:
            n -= 1
    #maps.printInfo(hero, way) #Выводим информацию о карте после построения маршрута

# Запуск волны, где У и Х - координаты, n - текущее число волны, exitFlag - флаг конца алгоритма, checkSym - какой символ на карте заменяем числом n,
# symbol - волна будет распространяться пока мы не найдем этот символ на карте, way - наш массив (карта)
def findWays (y, x, n, exitFlag, checkSym, symbol, way: List[List[int]]):
    #Вверх
    if (y - 1 >= 0 and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x] == checkSym) or way[y - 1][x] == symbol:
        if way[y - 1][x] == symbol:
            exitFlag = True
        else:
            way[y - 1][x] = n

    #Вниз
    if (y + 1 < len(way) and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x] == checkSym) or way[y + 1][x] == symbol:
        if way[y + 1][x] == symbol:
            exitFlag = True
        else:
            way[y + 1][x] = n

    #Влево
    if (x - 1 >= 0 and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and way[y][x - 1] == checkSym) or way[y][x - 1] == symbol:
        if way[y][x - 1] == symbol:
            exitFlag = True
        else:
            way[y][x - 1] = n

    #Вправо
    if (x + 1 < len(way[y]) and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and way[y][x + 1] == checkSym) or way[y][x + 1] == symbol:
        if way[y][x + 1] == symbol:
            exitFlag = True
        else:
            way[y][x + 1] = n

    #Вправо-Вниз
    if (x + 1 < len(way[y]) and y + 1 < len(way) and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x + 1] == checkSym) or (way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x + 1] = n

    #Вправо-Вверх
    if (x + 1 < len(way[y]) and y - 1 >= 0 and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x + 1] == checkSym) or (way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x + 1] = n

    #Влево-Вниз
    if (x - 1 >= 0 and y + 1 < len(way) and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x - 1] == checkSym) or (way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x - 1] = n

    #Влево-Вверх
    if (x - 1 >= 0 and y - 1 >= 0 and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x - 1] == checkSym) or (way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x - 1] = n
    return exitFlag

# Построение маршрута от цели, где У и Х - координаты, n - текущее число волны, exitFlag - флаг конца алгоритма, checkSym - какой символ на карте заменяем числом n,
# symbol - волна будет распространяться пока мы не найдем этот символ на карте, way - наш массив (карта), nextStep - флаг сообщающий о нахождении symbol'а или установке '+' (прокладывание маршрута до цели)
def findBackWay (y, x, n, exitFlag, checkSym, symbol, nextStep, way: List[List[int]], monWay: List[List[int]]):
    #Влево-Вверх
    if (x - 1 >= 0 and y - 1 >= 0 and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x - 1] == checkSym and (monWay[y - 1][x - 1]) != checkSym) or (way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x - 1] = n
        nextStep = True

    #Влево-Вниз
    elif (x - 1 >= 0 and y + 1 < len(way) and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x - 1] == checkSym and (monWay[y + 1][x - 1]) != checkSym) or (way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x - 1] = n
        nextStep = True

    #Вправо-Вверх
    elif (x + 1 < len(way[y]) and y - 1 >= 0 and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x + 1] == checkSym and (monWay[y - 1][x + 1]) != checkSym) or (way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x + 1] = n
        nextStep = True

    #Вправо-Вниз
    elif (x + 1 < len(way[y]) and y + 1 < len(way) and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x + 1] == checkSym and (monWay[y + 1][x + 1]) != checkSym) or (way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x + 1] = n
        nextStep = True

    #Вверх
    elif (y - 1 >= 0 and way[y - 1][x] != 'B' and way[y - 1][x] != 'M' and way[y - 1][x] == checkSym and (monWay[y - 1][x]) != checkSym) or way[y - 1][x] == symbol:
        if way[y - 1][x] == symbol:
            exitFlag = True
        else:
            way[y - 1][x] = n
        nextStep = True

    #Вниз
    elif (y + 1 < len(way) and way[y + 1][x] != 'B' and way[y + 1][x] != 'M' and way[y + 1][x] == checkSym and (monWay[y + 1][x]) != checkSym) or way[y + 1][x] == symbol:
        if way[y + 1][x] == symbol:
            exitFlag = True
        else:
            way[y + 1][x] = n
        nextStep = True

    #Влево
    elif (x - 1 >= 0 and way[y][x - 1] != 'B' and way[y][x - 1] != 'M' and way[y][x - 1] == checkSym and (monWay[y][x - 1]) != checkSym) or way[y][x - 1] == symbol:
        if way[y][x - 1] == symbol:
            exitFlag = True
        else:
            way[y][x - 1] = n
        nextStep = True

    #Вправо
    elif (x + 1 < len(way[y]) and way[y][x + 1] != 'B' and way[y][x + 1] != 'M' and way[y][x + 1] == checkSym and (monWay[y][x + 1]) != checkSym) or way[y][x + 1] == symbol:
        if way[y][x + 1] == symbol:
            exitFlag = True
        else:
            way[y][x + 1] = n
        nextStep = True
    return exitFlag, nextStep

