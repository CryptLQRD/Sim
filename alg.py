#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import blocks
import pyganim
import monsters
import os
import random
import player

def test (left, right, up, down, moveTime):
    number = random.randint (1, 9)
    moveTime = random.randint (3, 25)
    if number == 1:
        left= True
        right = False
        up = False
        down = False
        print ("Left")
    if number == 2:
        left = False
        right = True
        up = False
        down = False
        print ("Right")
    if number == 3:
        left = False
        right = False
        up= True
        down = False
        print("Up")
    if number == 4:
        left = False
        right = False
        up = False
        down= True
        print("Down")
    if number == 5:
        left = False
        right = False
        up = False
        down = False
        print("Stop")
    if number == 6:
        left= True
        right = False
        up = True
        down = False
        print ("Left-Up")
    if number == 7:
        left = True
        right = False
        up = False
        down = True
        print("Left-Down")
    if number == 8:
        left = False
        right = True
        up = True
        down = False
        print("Right-Up")
    if number == 9:
        left = False
        right = True
        up = False
        down = True
        print("Right-Down")
    return left, right, up, down, moveTime