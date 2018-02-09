#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import blocks
import pyganim
import monsters
import os
import random
import player
timer = pygame.time.Clock()

def test (left, right, up, down):
    timer.tick(5)
    number = random.randint (1, 5)
    if number == 1:
        left= True
        print ("Left")
    if number == 2:
        right = True
        print ("Right")
    if number == 3:
        up= True
        print("Up")
    if number == 4:
        down= True
        print("Down")
    if number == 5:
        left = False
        right = False
        up = False
        down = False
        print("Stop")
    return left, right, up, down