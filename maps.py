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

def printInfo (hero, way: List[List[int]]):
    #print('\nИнформация об алгоритме: ')
    #print ("Я вижу:")
    print('\nИнформация о карте: ')
    for i in range(len(way)):
        for j in range(len(way[i])):
            #if way[i][j] == 3:
            #    hero.myPosX = j
            #    hero.myPosY = i
            print(way[i][j], end=' ')
        print()
    print('')
    print("Позиция  ГЕРОЯ  в массиве  X: " + str(hero.myPosX) + "  Y: " + str(hero.myPosY))
    print("Позиция ПОРТАЛА в массиве  X: " + str(blocks.Exit.myPosX)  + "  Y: " + str(blocks.Exit.myPosY))

def amountBigEnerge (way: List[List[int]]):
    bigEnergyCounter = 0
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] == 'E':
                bigEnergyCounter += 1
    #print("Число больших энергий: = " + str(bigEnergyCounter))
    return bigEnergyCounter

def clearMap (way: List[List[int]]):
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'H' and way[i][j] != 'P': #and way[i][j] != 'E'
                way[i][j] = 0
            #print(way[i][j], end=' ')

def clearNumberFromMap (way: List[List[int]]): # Функция забивающая неверные позиции алгоритма нулями для нормального отображения
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'H' and way[i][j] != 'P' and way[i][j] != '+' and way[i][j] != 'E':
                way[i][j] = 0
            #print(way[i][j], end=' ')