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

def identificationAlg (hero, way: List[List[int]], masMons):
    if True:
        hero.obsCount += 1
        depth = 240 # Стоит делить на moveTime отдельного монстра, иначе следует сделать переменные с сохранением предыдущих результатов (Пример stepX и stepY) При depth=60 и moveTime=4 step =15
        checkList = []
        timesXY111alg = 15 # Сколько раз подряд монстр должен сходить по одной и той же координате для того, чтобы алгоритм посчитал его 111
        alg111 = 120
        alg222 = 45    #кол-во проверок для alg222
        alg333 = 15    #кол-во проверок для alg333
        if hero.obsCount < depth:
            epi = 0
            counter = hero.obsCount
        else:
            counter = depth#
            epi = hero.obsCount - depth
        #monCounter = -1
        amountMon = 0
        delFromList = 3
        print() #Пустой принт для удобства отображения в консоли
        print(colored('Наблюдение №' + str(hero.obsCount) ,'white'))
        for i in range(len(way)):
            for j in range(len(way[i])):
                if way[i][j] == 'M':
                    for mn in masMons:
                        if j == mn.myPosX and i == mn.myPosY:
                            if checkList.count(mn.index) == 0:
                                amountMon += 1
                                #print('checkList.count(mn.index) {}'.format(checkList.count(mn.index)))
                                #print('X: ' + str(mn.myPosX))
                                #print('j: ' + str(j))
                                #print('Y: ' + str(mn.myPosY))
                                #print('i: ' + str(i))
                                mon = mn
                                monCounter = mn.index
                                checkList.append(mn.index)
                                #print (checkList)
                                #monCounter += 1
                                print ('Индекс монстра: ' + str(monCounter) + '   Имя: ' + str(mon.name))
                                observations.addObservation(hero.monInfo, observations.Observation(timestamp=hero.obsCount, x=j, y=i), index=monCounter)
                                #Вычисляем MoveTime монстров
                                newTimestamp = -1
                                x = hero.monInfo[monCounter].observations[epi].x #Устанавливаю текущий х и у
                                y = hero.monInfo[monCounter].observations[epi].y
                                if hero.monInfo[monCounter].moveTime < 0: #если у текущего монстра не определен МТ
                                    for k in range(counter):
                                        if x != hero.monInfo[monCounter].observations[epi + k].x or y != hero.monInfo[monCounter].observations[epi + k].y: #если х или у поменялись
                                            x = hero.monInfo[monCounter].observations[epi + k].x
                                            y = hero.monInfo[monCounter].observations[epi + k].y
                                            if newTimestamp != -1: # проверяем сделано ли за эту проверку это 2-ой раз? Если да, то разница и является МТ
                                                hero.monInfo[monCounter].moveTime = hero.monInfo[monCounter].observations[epi + k].timestamp - newTimestamp - 1
                                                newTimestamp = -1
                                            else: newTimestamp = hero.monInfo[monCounter].observations[epi + k].timestamp #иначе устанавливаем 1-ый Timestamp

                                #Вычисляем Alg монстров
                                if mon.moveTime == 0:
                                    x = hero.monInfo[monCounter].observations[epi].x
                                    y = hero.monInfo[monCounter].observations[epi].y

                                    stepX = 0
                                    stepY = 0
                                    Q = 0
                                    invis = False
                                    flag111alg = False
                                    flag222alg = False
                                    flag333alg = False
                                    if hero.monInfo[monCounter].alg < 0:
                                        for k in range(counter):
                                            #print('K: ' + str(k))
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
                                                if (stepX >= timesXY111alg or stepY >= timesXY111alg) and flag111alg == False: #Если много раз менялся только х или у, то проверяем мб это алг 111
                                                    #hero.final111algCheck = 0
                                                    if stepX > timesXY111alg:
                                                        #for c in range(hero.obsCount):
                                                        if (hero.monInfo[monCounter].observations[hero.obsCount - 2].x <= hero.monInfo[monCounter].observations[hero.obsCount - 1].x <= hero.monInfo[monCounter].observations[hero.obsCount].x) or \
                                                           (hero.monInfo[monCounter].observations[hero.obsCount - 2].x >= hero.monInfo[monCounter].observations[hero.obsCount - 1].x >= hero.monInfo[monCounter].observations[hero.obsCount].x):
                                                            print ('stepX: ' + str(stepX) + ' | stepY: ' + str(stepY))
                                                            print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(1) + ' Alg111','blue'))
                                                            flag111alg = True
                                                            hero.finalAlgCheck111.append(monCounter)
                                                            for dFL in range(delFromList):
                                                                if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                    hero.finalAlgCheck222.remove(monCounter)
                                                                if hero.finalAlgCheck333.count(monCounter) > 0:
                                                                    hero.finalAlgCheck333.remove(monCounter)
                                                    if stepY > timesXY111alg:
                                                        if (hero.monInfo[monCounter].observations[hero.obsCount - 2].y <= hero.monInfo[monCounter].observations[hero.obsCount - 1].y <= hero.monInfo[monCounter].observations[hero.obsCount].y) or\
                                                           (hero.monInfo[monCounter].observations[hero.obsCount - 2].y >= hero.monInfo[monCounter].observations[hero.obsCount - 1].y >= hero.monInfo[monCounter].observations[hero.obsCount].y):
                                                            print('stepX: ' + str(stepX) + ' | stepY: ' + str(stepY))
                                                            print(colored("Монстру " + str(mon.name) + ' (ind:' + str( monCounter) + ') добавлено ' + str( 1) + ' Alg111', 'blue'))
                                                            flag111alg = True
                                                            hero.finalAlgCheck111.append(monCounter)
                                                            for dFL in range(delFromList):
                                                                if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                    hero.finalAlgCheck222.remove(monCounter)
                                                                if hero.finalAlgCheck333.count(monCounter) > 0:
                                                                    hero.finalAlgCheck333.remove(monCounter)
                                                                #final111algCheck += 1
                                                                #print('Monster with final111algCheck {} and hero.obsCount {}'.format(final111algCheck, hero.obsCount))
                                                    #elif stepY > timesXY111alg:
                                                        #for c in range(hero.obsCount):
                                                        #    if hero.monInfo[monCounter].observations[0].x == hero.monInfo[monCounter].observations[c].x:
                                                        #       hero.finalAlgCheck111.append(monCounter)

                                                                #final111algCheck += 1
                                                                #print('Monster with final111algCheck {} and hero.obsCount {}'.format(final111algCheck, hero.obsCount))
                                                    if hero.finalAlgCheck111.count(monCounter) > alg111:
                                                        hero.monInfo[monCounter].alg = 111
                                                else:
                                                    check = 0
                                                    for q in range(len(way)):
                                                        if q == 0:
                                                            invis = False
                                                        else:
                                                            #Проверка монстров сверху
                                                            if hero.myPosY - q < 0:
                                                                1
                                                                #print('Q для верха: X=' + str(hero.myPosX) + ' Y=' + str(hero.myPosY - q) + ' way: ' + str(way[hero.myPosY - q][hero.myPosX]))
                                                            else:
                                                                #print('Q для верха: X=' + str(hero.myPosX) + ' Y=' + str(hero.myPosY - q) + ' way: ' + str(way[hero.myPosY - q][hero.myPosX]))
                                                                #print ('monCounter: ' + str(monCounter) + '   k: ' + str(k))
                                                                #print('hero.oCforLastMonTop: ' + str(hero.oCforLastMonTop) + '   epi + k: ' + str(epi + k))
                                                                if way[hero.myPosY - q][hero.myPosX] == 'B' or way[hero.myPosY - q][hero.myPosX] == 'W':
                                                                    invis = True
                                                                elif way[hero.myPosY - q][hero.myPosX] != 'B' and way[hero.myPosY - q][hero.myPosX] != 'W' and invis == False:
                                                                    if way[hero.myPosY - q][hero.myPosX] == 'M':
                                                                        # print('ВИЖУ МОНСТРА: X=' + str(hero.myPosX) + ' Y='+ str(hero.myPosY - q))
                                                                        Q = q
                                                                        mon.reward = q
                                                                        #print(colored("Q (top)=" + str(Q),'red'))
                                                                        if hero.indexForThisMon.count(monCounter) == 0:
                                                                            hero.indexForThisMon.append(monCounter)
                                                                        hero.oCforLastMonTop = hero.obsCount
                                                                        hero.myLastPosXforMonTop = hero.myPosX
                                                                        hero.myLastPosYforMonTop = hero.myPosY
                                                                        #print('Q=' + str(Q))
                                                                # print('stepX=' + str(stepX) + ' stepY='+ str(stepY))
                                                                elif (hero.monInfo[monCounter].observations[hero.oCforLastMonTop].x == hero.monInfo[monCounter].observations[epi + k].x) and (stepX == 0) and (stepY > 2 and stepY >= Q) and (way[hero.myLastPosYforMonTop][hero.myLastPosXforMonTop] == 'M' and (hero.myLastPosXforMonTop == mon.myPosX and hero.myLastPosYforMonTop == mon.myPosY) and (hero.monInfo[monCounter].observations[hero.oCforLastMonTop].y < hero.monInfo[monCounter].observations[epi + k].y)) and flag333alg == False:
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    flag333alg = True
                                                                    #hero.final333algCheck += 1
                                                                    for qSum in range(mon.reward):
                                                                        hero.finalAlgCheck333.append(monCounter)
                                                                        #print(colored('qSumTop: ' + str(qSum) + ' ', 'red'))
                                                                    check = 0
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(mon.reward) + ' Alg333(Top)', 'red'))
                                                                    # hero.indexForThisMon = monCounter
                                                                    for dFL in range(delFromList):
                                                                        if hero.finalAlgCheck111.count(monCounter) > 0:
                                                                            hero.finalAlgCheck111.remove(monCounter)
                                                                        if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                            hero.finalAlgCheck222.remove(monCounter)
                                                                    if  hero.finalAlgCheck333.count(monCounter) > alg333:
                                                                        hero.monInfo[monCounter].alg = 333
                                                                        check = 0
                                                                elif (((hero.monInfo[monCounter].observations[hero.oCforLastMonTop].x != hero.monInfo[monCounter].observations[epi + k].x) and (stepX > 0)) or (hero.monInfo[monCounter].observations[hero.oCforLastMonTop].y > hero.monInfo[monCounter].observations[epi + k].y)) and hero.indexForThisMon.count(monCounter) == 1 and flag222alg == False:
                                                                    check += 1
                                                                    flag222alg = True
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(1) + ' Alg222(Top)', 'green'))
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    if Q < check:
                                                                        hero.finalAlgCheck222.append(monCounter)
                                                                    if  hero.finalAlgCheck222.count(monCounter) > alg222:
                                                                        hero.monInfo[monCounter].alg = 222

                                                    for q in range(len(way)):
                                                        if q == 0:
                                                            invis = False
                                                        else:
                                                            #Проверка монстров снизу
                                                            if hero.myPosY + q >= len(way):
                                                                1
                                                                #print('Q для низа: X=' + str(hero.myPosX) + ' Y=' + str(hero.myPosY - q) + ' way: ' + str(way[hero.myPosY - q][hero.myPosX]))
                                                            else:
                                                                #print('Q для низа: X=' + str(hero.myPosX) + ' Y='+ str(hero.myPosY + q) + ' way: ' + str(way[hero.myPosY + q][hero.myPosX]))
                                                                if way[hero.myPosY + q][hero.myPosX] == 'B' or way[hero.myPosY + q][hero.myPosX] == 'W':
                                                                    invis = True
                                                                elif way[hero.myPosY + q][hero.myPosX] != 'B' and way[hero.myPosY + q][hero.myPosX] != 'W' and invis == False:
                                                                    if way[hero.myPosY + q][hero.myPosX] == 'M':
                                                                        # print('ВИЖУ МОНСТРА: X=' + str(hero.myPosX) + ' Y='+ str(hero.myPosY - q))
                                                                        Q = q
                                                                        mon.reward = q
                                                                        #print(colored("Q (bot)=" + str(Q), 'red'))
                                                                        if hero.indexForThisMon.count(monCounter) == 0:
                                                                            hero.indexForThisMon.append(monCounter)
                                                                        hero.oCforLastMonBot = hero.obsCount
                                                                        hero.myLastPosXforMonBot = hero.myPosX
                                                                        hero.myLastPosYforMonBot = hero.myPosY
                                                                        #print('Q=' + str(Q))
                                                                # print('stepX=' + str(stepX) + ' stepY='+ str(stepY))
                                                                elif (hero.monInfo[monCounter].observations[hero.oCforLastMonBot].x == hero.monInfo[monCounter].observations[epi + k].x) and (stepX == 0) and (stepY > 2 and stepY >= Q) and (way[hero.myLastPosYforMonBot][hero.myLastPosXforMonBot] == 'M' and (hero.myLastPosXforMonBot == mon.myPosX and hero.myLastPosYforMonBot == mon.myPosY) and (hero.monInfo[monCounter].observations[hero.oCforLastMonBot].y > hero.monInfo[monCounter].observations[epi + k].y)) and flag333alg == False:
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    flag333alg = True
                                                                    #hero.final333algCheck += 1
                                                                    for qSum in range(mon.reward):
                                                                        hero.finalAlgCheck333.append(monCounter)
                                                                        #print(colored('qSumBot: ' + str(qSum) + ' ', 'red'))
                                                                    check = 0
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(mon.reward) + ' Alg333(Bot)', 'red'))
                                                                    for dFL in range(delFromList):
                                                                        if hero.finalAlgCheck111.count(monCounter) > 0:
                                                                            hero.finalAlgCheck111.remove(monCounter)
                                                                        if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                            hero.finalAlgCheck222.remove(monCounter)
                                                                    # hero.indexForThisMon = monCounter
                                                                    if  hero.finalAlgCheck333.count(monCounter) > alg333:
                                                                        hero.monInfo[monCounter].alg = 333

                                                                        check = 0
                                                                elif (((hero.monInfo[monCounter].observations[hero.oCforLastMonBot].x != hero.monInfo[monCounter].observations[epi + k].x) and (stepX > 0)) or (hero.monInfo[monCounter].observations[hero.oCforLastMonBot].y < hero.monInfo[monCounter].observations[epi + k].y)) and hero.indexForThisMon.count(monCounter) == 1 and flag222alg == False:
                                                                    check += 1
                                                                    flag222alg = True
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(1) + ' Alg222(Bot)', 'green'))
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    if Q < check:
                                                                        hero.finalAlgCheck222.append(monCounter)
                                                                    if  hero.finalAlgCheck222.count(monCounter) > alg222:
                                                                        hero.monInfo[monCounter].alg = 222

                                                    for q in range(len(way[0])):
                                                        if q == 0:
                                                            invis = False
                                                        else:
                                                            # Проверка монстров справа
                                                            if hero.myPosX + q >= len(way[0]):
                                                                1
                                                            else:
                                                                #print('Q для права: X=' + str(hero.myPosX + q) + ' Y=' + str(hero.myPosY) + ' way: ' + str(way[hero.myPosY][hero.myPosX + q]))
                                                                #print('hero.oCforLastMonRight' + str(hero.oCforLastMonRight) + '   epi + k: ' + str(epi+k))
                                                                if way[hero.myPosY][hero.myPosX + q] == 'B' or way[hero.myPosY][hero.myPosX + q] == 'W':
                                                                    invis = True
                                                                    #print(colored("q (rgh)=" + str(q) + '   invis = ' + str(invis),'red'))
                                                                elif way[hero.myPosY][hero.myPosX + q] != 'B' and way[hero.myPosY][hero.myPosX + q] != 'W' and invis == False:
                                                                    if way[hero.myPosY][hero.myPosX + q] == 'M':
                                                                        # print('ВИЖУ МОНСТРА: X=' + str(hero.myPosX) + ' Y='+ str(hero.myPosY - q))
                                                                        Q = q
                                                                        mon.reward = q
                                                                        #print(colored("Q (rgh)=" + str(Q), 'red'))
                                                                        if hero.indexForThisMon.count(monCounter) == 0:
                                                                            hero.indexForThisMon.append(monCounter)
                                                                        hero.oCforLastMonRight = hero.obsCount
                                                                        hero.myLastPosXforMonRight = hero.myPosX
                                                                        hero.myLastPosYforMonRight = hero.myPosY
                                                                        #print(colored('hero.oCforLastMonRight: ' + str(hero.oCforLastMonRight) + ' ', 'green'))
                                                                        #print('Q=' + str(Q))
                                                                # print('stepX=' + str(stepX) + ' stepY='+ str(stepY))
                                                                elif (hero.monInfo[monCounter].observations[hero.oCforLastMonRight].y == hero.monInfo[monCounter].observations[epi + k].y) and (stepY == 0) and (stepX > 2 and stepX >= Q) and (way[hero.myLastPosYforMonRight][hero.myLastPosXforMonRight] == 'M' and (hero.myLastPosXforMonRight == mon.myPosX and hero.myLastPosYforMonRight == mon.myPosY) and (hero.monInfo[monCounter].observations[hero.oCforLastMonRight].x > hero.monInfo[monCounter].observations[epi + k].x)) and flag333alg == False:
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    flag333alg = True
                                                                    #hero.final333algCheck += 1
                                                                    for qSum in range(mon.reward):
                                                                        hero.finalAlgCheck333.append(monCounter)
                                                                        #print(colored('qSumRgh: ' + str(qSum) + ' ', 'red'))
                                                                    check = 0
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(mon.reward) + ' Alg333(Rgh)', 'red'))
                                                                    for dFL in range(delFromList):
                                                                        if hero.finalAlgCheck111.count(monCounter) > 0:
                                                                            hero.finalAlgCheck111.remove(monCounter)
                                                                        if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                            hero.finalAlgCheck222.remove(monCounter)
                                                                    # hero.indexForThisMon = monCounter
                                                                    if  hero.finalAlgCheck333.count(monCounter) > alg333:
                                                                        hero.monInfo[monCounter].alg = 333
                                                                elif (((hero.monInfo[monCounter].observations[hero.oCforLastMonRight].y != hero.monInfo[monCounter].observations[epi + k].y) and (stepY > 0)) or (hero.monInfo[monCounter].observations[hero.oCforLastMonRight].x < hero.monInfo[monCounter].observations[epi + k].x)) and hero.indexForThisMon.count(monCounter) == 1 and flag222alg == False:
                                                                    check += 1
                                                                    flag222alg = True
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(1) + ' Alg222(Rgh)', 'green'))
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    if Q < check:
                                                                        hero.finalAlgCheck222.append(monCounter)
                                                                    if  hero.finalAlgCheck222.count(monCounter) > alg222:
                                                                        hero.monInfo[monCounter].alg = 222

                                                    for q in range(len(way[0])):
                                                        if q == 0:
                                                            invis = False
                                                        else:
                                                            # Проверка монстров слева
                                                            if hero.myPosX - q < 0:
                                                                1
                                                            else:
                                                                #print('Q для лева: X=' + str(hero.myPosX - q) + ' Y=' + str(hero.myPosY) + ' way: ' + str(way[hero.myPosY][hero.myPosX - q]))
                                                                if way[hero.myPosY][hero.myPosX - q] == 'B' or way[hero.myPosY][hero.myPosX - q] == 'W':
                                                                    invis = True
                                                                elif way[hero.myPosY][hero.myPosX - q] != 'B' and way[hero.myPosY][hero.myPosX - q] != 'W' and invis == False:
                                                                    if way[hero.myPosY][hero.myPosX - q] == 'M':
                                                                        # print('ВИЖУ МОНСТРА: X=' + str(hero.myPosX) + ' Y='+ str(hero.myPosY - q))
                                                                        Q = q
                                                                        mon.reward = q
                                                                        #print(colored("Q (lft)=" + str(Q), 'red'))
                                                                        if hero.indexForThisMon.count(monCounter) == 0:
                                                                            hero.indexForThisMon.append(monCounter)
                                                                        hero.oCforLastMonLeft = hero.obsCount
                                                                        hero.myLastPosXforMonLeft = hero.myPosX
                                                                        hero.myLastPosYforMonLeft = hero.myPosY
                                                                        #print('Q=' + str(Q))
                                                                # print('stepX=' + str(stepX) + ' stepY='+ str(stepY))
                                                                elif (hero.monInfo[monCounter].observations[hero.oCforLastMonLeft].y == hero.monInfo[monCounter].observations[epi + k].y) and (stepY == 0) and (stepX > 2 and stepX >= Q) and (way[hero.myLastPosYforMonLeft][hero.myLastPosXforMonLeft] == 'M' and (hero.myLastPosXforMonLeft == mon.myPosX and hero.myLastPosYforMonLeft == mon.myPosY) and (hero.monInfo[monCounter].observations[hero.oCforLastMonLeft].x < hero.monInfo[monCounter].observations[epi + k].x)) and flag333alg == False:
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    flag333alg = True
                                                                    #hero.final333algCheck += 1
                                                                    for qSum in range(mon.reward):
                                                                        hero.finalAlgCheck333.append(monCounter)
                                                                        #print(colored('qSumLft: ' + str(qSum) + ' ', 'red'))
                                                                    check = 0

                                                                    # hero.indexForThisMon = monCounter
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(mon.reward) + ' Alg333(Lft)', 'red'))
                                                                    for dFL in range(delFromList):
                                                                        if hero.finalAlgCheck111.count(monCounter) > 0:
                                                                            hero.finalAlgCheck111.remove(monCounter)
                                                                        if hero.finalAlgCheck222.count(monCounter) > 0:
                                                                            hero.finalAlgCheck222.remove(monCounter)
                                                                    #print ('Индекс монстра: ' + str(monCounter) + '   Имя: ' + str())
                                                                    if hero.finalAlgCheck333.count(monCounter) > alg333:
                                                                        hero.monInfo[monCounter].alg = 333
                                                                        check = 0
                                                                elif (((hero.monInfo[monCounter].observations[hero.oCforLastMonLeft].y != hero.monInfo[monCounter].observations[epi + k].y) and (stepY > 0)) or (hero.monInfo[monCounter].observations[hero.oCforLastMonLeft].x > hero.monInfo[monCounter].observations[epi + k].x)) and hero.indexForThisMon.count(monCounter) == 1 and flag222alg == False:
                                                                    check += 1
                                                                    flag222alg = True
                                                                    print(colored("Монстру " + str(mon.name) + ' (ind:' + str(monCounter) + ') добавлено ' + str(1) + ' Alg222(Lft)', 'green'))
                                                                    if hero.indexForThisMon.count(monCounter) == 1:
                                                                        hero.indexForThisMon.remove(monCounter)
                                                                    if Q < check:
                                                                        hero.finalAlgCheck222.append(monCounter)
                                                                    if  hero.finalAlgCheck222.count(monCounter) > alg222:
                                                                        hero.monInfo[monCounter].alg = 222


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
                                    #observations.print_all_observations(hero.monInfo)
                                    observations.printObs(hero.monInfo, monCounter, False)
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
    hero.lastLeft = left
    hero.lastRight = right
    hero.lastUp = up
    hero.lastDown = down

    if moveTimeFlag == True:
        hero.moveTime = 0
    #elif hero.imSlow == True: moveTime = 10
    else: hero.moveTime = hero.startMoveTime#4 #Для плавного движения moveTime = 3
    return left, right, up, down, hero.moveTime

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
    if ((way[y][x + 1] == 'E' and monWay[y][x + 1] != hero.startMoveTime*hero.known) or (way[y + 1][x] == 'E' and monWay[y + 1][x] != hero.startMoveTime*hero.known)\
        or (way[y][x - 1] == 'E' and monWay[y][x - 1] != hero.startMoveTime*hero.known) or (way[y - 1][x] == 'E' and monWay[y - 1][x] != hero.startMoveTime*hero.known)) \
        or (way[y + 1][x + 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (monWay[y + 1][x + 1] != hero.startMoveTime*hero.known))\
        or (way[y - 1][x + 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (monWay[y - 1][x + 1] != hero.startMoveTime*hero.known))\
        or (way[y + 1][x - 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (monWay[y + 1][x - 1] != hero.startMoveTime*hero.known))\
        or (way[y - 1][x - 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (monWay[y - 1][x - 1] != hero.startMoveTime*hero.known)):

        exitFlag = True # Заканчиваем работу алгоритма т.к. энергия уже находится рядом с героем.
    #if (way[y][x + 1] == 'E' or way[y + 1][x] == 'E' or way[y][x - 1] == 'E' or way[y - 1][x] == 'E') \
    #        or (way[y + 1][x + 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M')) \
    #        or (way[y - 1][x + 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M')) \
    #        or (way[y + 1][x - 1] == 'E' and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M')) \
    #        or (way[y - 1][x - 1] == 'E' and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M')):
    #        exitFlag = True  # Заканчиваем работу алгоритма т.к. энергия уже находится рядом с героем.
        #!= (hero.startMoveTime)
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
        exitFlag, nextStep = findBackWay(y, x, '+', exitFlag, n, 'H', nextStep, way, monWay, hero)
    elif symbol == 'W':
        x = blocks.Exit.myPosX
        y = blocks.Exit.myPosY
        exitFlag, nextStep = findBackWay(y, x, '+', exitFlag, n, 'H', nextStep, way, monWay, hero)

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
                    else: exitFlag, nextStep = findBackWay(i, j, '+',exitFlag, n, 'H', nextStep, way, monWay, hero)
            if nextStep == True:
                break
        exitCounter += 1
        if exitCounter > maxEC-1:
            #hero.wait = True
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
def findBackWay (y, x, n, exitFlag, checkSym, symbol, nextStep, way: List[List[int]], monWay: List[List[int]], hero):
    #Влево-Вверх
    if (x - 1 >= 0 and y - 1 >= 0 and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x - 1] == checkSym and (monWay[y - 1][x - 1]) != checkSym*hero.known and (monWay[y - 1][x - 1]) != (hero.startMoveTime*hero.known)) or (way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x - 1] = n
        nextStep = True

    #Влево-Вниз
    elif (x - 1 >= 0 and y + 1 < len(way) and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x - 1] == checkSym and (monWay[y + 1][x - 1]) != checkSym*hero.known and (monWay[y + 1][x - 1]) != (hero.startMoveTime*hero.known)) or (way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x - 1] == symbol and (way[y][x - 1] != 'B' and way[y][x - 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x - 1] = n
        nextStep = True

    #Вправо-Вверх
    elif (x + 1 < len(way[y]) and y - 1 >= 0 and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M') and way[y - 1][x + 1] == checkSym and (monWay[y - 1][x + 1]) != checkSym*hero.known and (monWay[y - 1][x + 1]) != (hero.startMoveTime*hero.known)) or (way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M')):
        if way[y - 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y - 1][x] != 'B' and way[y - 1][x] != 'M'):
            exitFlag = True
        else:
            way[y - 1][x + 1] = n
        nextStep = True

    #Вправо-Вниз
    elif (x + 1 < len(way[y]) and y + 1 < len(way) and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M') and way[y + 1][x + 1] == checkSym and (monWay[y + 1][x + 1]) != checkSym*hero.known and (monWay[y + 1][x + 1]) != (hero.startMoveTime*hero.known)) or (way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M')):
        if way[y + 1][x + 1] == symbol and (way[y][x + 1] != 'B' and way[y][x + 1] != 'M') and (way[y + 1][x] != 'B' and way[y + 1][x] != 'M'):
            exitFlag = True
        else:
            way[y + 1][x + 1] = n
        nextStep = True

    #Вверх
    elif (y - 1 >= 0 and way[y - 1][x] != 'B' and way[y - 1][x] != 'M' and way[y - 1][x] == checkSym and (monWay[y - 1][x]) != checkSym*hero.known and (monWay[y - 1][x]) != (hero.startMoveTime*hero.known)) or way[y - 1][x] == symbol:
        if way[y - 1][x] == symbol:
            exitFlag = True
        else:
            way[y - 1][x] = n
        nextStep = True

    #Вниз
    elif (y + 1 < len(way) and way[y + 1][x] != 'B' and way[y + 1][x] != 'M' and way[y + 1][x] == checkSym and (monWay[y + 1][x]) != checkSym*hero.known and (monWay[y + 1][x]) != (hero.startMoveTime*hero.known)) or way[y + 1][x] == symbol:
        if way[y + 1][x] == symbol:
            exitFlag = True
        else:
            way[y + 1][x] = n
        nextStep = True

    #Влево
    elif (x - 1 >= 0 and way[y][x - 1] != 'B' and way[y][x - 1] != 'M' and way[y][x - 1] == checkSym and (monWay[y][x - 1]) != checkSym*hero.known and (monWay[y][x - 1]) != (hero.startMoveTime*hero.known)) or way[y][x - 1] == symbol:
        if way[y][x - 1] == symbol:
            exitFlag = True
        else:
            way[y][x - 1] = n
        nextStep = True

    #Вправо
    elif (x + 1 < len(way[y]) and way[y][x + 1] != 'B' and way[y][x + 1] != 'M' and way[y][x + 1] == checkSym and (monWay[y][x + 1]) != checkSym*hero.known and (monWay[y][x + 1]) != (hero.startMoveTime*hero.known)) or way[y][x + 1] == symbol:
        if way[y][x + 1] == symbol:
            exitFlag = True
        else:
            way[y][x + 1] = n
        nextStep = True
    return exitFlag, nextStep

