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
from termcolor import colored

def printInfo (hero, way: List[List[int]]):
    #print('\nИнформация об алгоритме: ')
    #print ("Я вижу:")
    print('\nИнформация о карте: ')
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] == 'E':
                print(colored(way[i][j], 'blue'), end=' ')
            elif way[i][j] == 'B':
                print(colored(way[i][j], 'yellow'), end=' ')
            elif way[i][j] == 'H':
                print(colored(way[i][j], 'magenta'), end=' ')
            elif way[i][j] == 'M':
                print(colored(way[i][j], 'red'), end=' ')
            elif way[i][j] == '@':
                print(colored(way[i][j], 'cyan'), end=' ')
            elif way[i][j] == 0 or way[i][j] == '0':
                print(colored(way[i][j], 'white'), end=' ')
            elif way[i][j] == '+':
                print(colored(way[i][j], 'grey'), end=' ')
            elif way[i][j] == 'W':
                print(colored(way[i][j], 'green'), end=' ')
            else: print(way[i][j], end=' ')
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
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'P': # and way[i][j] != 'H'
                way[i][j] = 0
            #print(way[i][j], end=' ')

def clearWayNumFromMap (way: List[List[int]]): # Функция забивающая неверные позиции алгоритма нулями для нормального отображения, оставляя энергии на карте
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'H' and way[i][j] != 'P' and way[i][j] != 'M' and way[i][j] != 'E':
                way[i][j] = 0
            #print(way[i][j], end=' ')

def clearNumFromMap (way: List[List[int]]): # Функция забивающая неверные позиции алгоритма нулями для нормального отображения, оставляя энергии и проложенный маршрут на карте
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'H' and way[i][j] != 'P' and way[i][j] != 'M' and way[i][j] != 'E' and way[i][j] != '+': # and way[i][j] != 'o':
                way[i][j] = 0
            #print(way[i][j], end=' ')

def clearHeroFromMap (way: List[List[int]]):
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] == 'H':
                way[i][j] = 0
            #print(way[i][j], end=' ')

def printMonsterInfo (way: List[List[int]]):
    #print('\nИнформация об алгоритме: ')
    #print ("Я вижу:")
    print('\nКарта монстра: ')
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] == 'E':
                print(colored(way[i][j], 'blue'), end=' ')
            elif way[i][j] == 'B':
                print(colored(way[i][j], 'yellow'), end=' ')
            elif way[i][j] == 'H':
                print(colored(way[i][j], 'magenta'), end=' ')
            elif way[i][j] == 'M':
                print(colored(way[i][j], 'red'), end=' ')
            elif way[i][j] == '@':
                print(colored(way[i][j], 'cyan'), end=' ')
            elif way[i][j] == 0 or way[i][j] == '0':
                print(colored(way[i][j], 'white'), end=' ')
            elif way[i][j] == '+':
                print(colored(way[i][j], 'grey'), end=' ')
            elif way[i][j] == 'W':
                print(colored(way[i][j], 'green'), end=' ')
            else: print(way[i][j], end=' ')
        print()
    #print('')
    #print("Позиция  ГЕРОЯ  в массиве  X: " + str(hero.myPosX) + "  Y: " + str(hero.myPosY))
    #print("Позиция ПОРТАЛА в массиве  X: " + str(blocks.Exit.myPosX)  + "  Y: " + str(blocks.Exit.myPosY))

def clearMonsterWayFromMap (way: List[List[int]]):
    for i in range(len(way)):
        for j in range(len(way[i])):
            if way[i][j] != 'B' and way[i][j] != 'W' and way[i][j] != 'M':
                way[i][j] = 0