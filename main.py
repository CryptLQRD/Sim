#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
import numpy as np
import pyganim
from pygame import *
#from player import *
import player
#from blocks import *
import blocks
from monsters import *
#import monsters
import alg
import datetime
import maps
import time as tm
from time import sleep
import random
import observations
from termcolor import colored



#Объявляем переменные
WIN_WIDTH = 608#800#672  #1024   #Ширина создаваемого окна
WIN_HEIGHT = 640#640#384 #800   # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#003300"
#INFO_STRING_WIDTH = 165 # Ширина
#INFO_STRING_HEIGHT = 32 # Высота !!!ЕСЛИ БУДУ МЕНЯТЬ, ТО И В КАМЕРЕ НЕ ЗАБЫТЬ!!!
#INFO_STRING_COLOR = "#006000"
levelName = 'lvl3.txt' #Название уровня
FILE_DIR = os.path.dirname(__file__)
PLAY = False # Включить\Выключить управление игроком
REPEAT = True  # Включить\Выключить повторние игры с начала
amEpisod = 120000   # Через какое кол-во эпизодов алгоритмы монстров меняются
STARTDELAY = 16 #Базовая скорость симулятора. Чем больше значение, тем быстрее симулятор. Чем меньше значение, тем медленее симулятор.

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel(): # Работа с файлом уровня

    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open(('%s/levels/'+levelName) % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                if commands[0] == "portal":  # если первая команда portal, то создаем портал
                    tp = blocks.BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)
                if commands[0] == "monsterBat":  # если первая команда monster, то создаем монстра
                    mn = Bat(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)
                if commands[0] == "monsterWraith":  # если первая команда monster, то создаем монстра
                    mn = Wraith(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)
                if commands[0] == "monsterBird":  # если первая команда monster, то создаем монстра
                    mn = Bird(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)
                if commands[0] == "monsterPursuer":  # если первая команда monster, то создаем монстра
                    mn = Pursuer(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)


def saveResult(hero, workTime, masMons): # Работа с файлом result
    #Определяем № эпизода
    numEpisod (hero)
    hero.episod += 1

    winScore = 20
    monScore = 0
    hero.finalScore = hero.score + (hero.live) * 5 #Прибавляем + 1 за собранную энергию и 5 очков за каждую жизнь
    if (hero.winner):                              #Прибавляем + 15 за победу
        hero.finalScore += winScore
    else: winScore = 0
    hero.finalScore -= hero.amMove/10
    #for mn in masMons:
    #    if hero.monInfo[mn.index].alg == mn.algorithm:
    #        monScore += 5
    # hero.finalScore += monScore

    #print('monScore ' + str(monScore))
    #hero.finalScore -= workTime.seconds

    #Добавить зависимость от кол-ва шагов
    #Усреднять данные с Х эпизодов


        #Сохраняем в файл
    resultFile = open('%s/levels/episodes/result.txt' % FILE_DIR, 'a')
    resultFile.write('Эпизод № '+ str(hero.episod) + '   Время: ' + str(workTime) + '   Уровень: ' +  levelName +'\n') # выполнения эпизода
    if (hero.live <= 0):
        resultFile.write('Поражение!')
    elif (hero.winner):
        resultFile.write('Победа!')
    else:
        resultFile.write('Соединение разорвано!')
    resultFile.write('  |  Энергии: ' + str(hero.score) + '  |  Жизни: ' + str(hero.live) + '  |  Счёт: ' + str(hero.finalScore) \
                     + '  ('+ str(hero.score) + ' + ' + str((hero.live)*5) + ' + ' + str(winScore) + ' - ' +str(hero.amMove/10)  + ')' + '\n\n') #+ ' - ' + str(workTime.seconds) + ')'
    for mn in masMons:
        resultFile.write('MONSTER: ' + str(mn.name) + ' | Alg: ' + str(mn.algorithm) + ' | startMT: ' + str(mn.startMoveTime) + '\n')
    for mn in masMons:
        resultFile.write('ID:' + str(mn.index) +' | Имя: ' + str(mn.name) + ' | Alg: ' + str(hero.monInfo[mn.index].alg) + ' | startMT: ' + str(hero.monInfo[mn.index].moveTime) + '\n')
    resultFile.write('\n\n\n')
    #print('Name: ' + str(mn.name) + '  Alg: ' + str(mn.algorithm) + '  moveTime: ' + str(mn.moveTime))
    resultFile.close()

def numEpisod (hero):
    resultFile = open('%s/levels/episodes/result.txt' % FILE_DIR)
    #episod = 0
    line = " "
    commands = []
    if line[0] != "":
        for line in resultFile.readlines():
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "Эпизод" and commands[1] == "№":
                    hero.episod = int(commands[2])
    resultFile.close()

def main():
    loadLevel()
    pygame.init() # Инициация PyGame, обязательная строчка 
    window = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Simulator") # Пишем в шапку
    screen = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности. будем использовать как фон
    screen.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом. 
    #Вместо BACKGROUND_COLOR могу сделать ((0, 255, 0))

    #Создание окна информации
    #info_string = Surface((INFO_STRING_WIDTH, INFO_STRING_HEIGHT))  # Создание видимой поверхности для строки инф
    #info_string.fill(Color(INFO_STRING_COLOR))
    #info_string.set_colorkey(Color(INFO_STRING_COLOR))

    #Шрифты
    font.init()
    score_font = font.SysFont('Comic Sans MS', 50, False, True)
    # score_font = font.Font(None,32)

    hero = player.Player(playerX,playerY) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = down = False

    entities.add(hero)
    timer = pygame.time.Clock()
    numEpisod(hero) # Определяю номер эпизода (это для удобства вывода)

    total_level_width  = len(level[0])*blocks.PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*blocks.PLATFORM_HEIGHT   # Высчитываем фактическую высоту уровня
    print ("Размер уровня:   Ширина: " + str(total_level_width) + "   Высота: " + str(total_level_height))
    camera = Camera(camera_configure, total_level_width, total_level_height)
    blocks.levelSize(total_level_width, total_level_height)  # Определение размера уровня для метода teleporting класса BigEnergy

    way = [[0] * len(level[0]) for i in range(len(level))] # Создаем карту уровня для алгоритма
    monWay = [[0] * len(level[0]) for i in range(len(level))]  # Создаем карту уровня для алгоритма


    way[int(hero.startY / 32)][int(hero.startX / 32)] = 'H' # Добавляем расположение героя на карту (в массив)
    hero.myPosX = int(hero.startX / 32)
    hero.myPosY = int(hero.startY / 32)

    amountBigEnergy = 0 # Общее кол-во Больших энергий на карте

    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = blocks.Block(x,y)
                entities.add(pf)
                platforms.append(pf)
                way[int(y/32)][int(x/32)] = 'B' #Если есть данный блок, то заполняем массив B
                monWay[int(y / 32)][int(x / 32)] = 'B'  # Если есть данный блок, то заполняем массив B для монстра
            if col == "*":
                bd = Bomb(x, y, 0, 0, 444, 0) #(x, y, 0, 0, 444, 0)
                entities.add(bd)
                platforms.append(bd)
                monsters.add(bd)
                # Добавляем монстра в массив
                masMons.append(bd)
                way[int(y/32)][int(x/32)] = 'M' #Если есть данный блок, то заполняем массив B
                monWay[int(y / 32)][int(x / 32)] = 'M'  # Если есть данный блок, то заполняем массив B для монстра
            if col == "@":
                bh = blocks.BlackHole(x,y)
                entities.add(bh)
                platforms.append(bh)
                animatedEntities.add(bh)
                masBlHole.append(bh)
                #way[int(y/32)][int(x/32)] = '@' #'@' #Если есть данный блок, то заполняем массив @
                monWay[int(y / 32)][int(x / 32)] = '@'  # '@' #Если есть данный блок, то заполняем массив @
                blocks.BlackHole.myCoord(bh)
            if col == "E":
                be = blocks.BigEnergy(x,y)
                entities.add(be)
                platforms.append(be)
                animatedEntities.add(be)
                way[int(y / 32)][int(x / 32)] = 'E' #Если есть данный блок, то заполняем массив E
                masBE.append(be)
                blocks.BigEnergy.myCoord(be)
                amountBigEnergy += 1 # Запоминаем кол-во энергий на карте
            if col == "W":
                ex = blocks.Exit(x,y)
                entities.add(ex)
                platforms.append(ex)
                animatedEntities.add(ex)
                way[int(y / 32)][int(x / 32)] = 'W' # Если есть данный блок, то заполняем массив W
                monWay[int(y / 32)][int(x / 32)] = 'W'  # Если есть данный блок, то заполняем массив W для монстра
                blocks.Exit.myPosX = int(x/32)
                blocks.Exit.myPosY = int(y/32)

            x += blocks.PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += blocks.PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    index = 0
    bomb = 0
    for mn in masMons:
        Monster.myCoord(mn)
        mn.index = index
        #print(mn.index)
        mn.moveTime = mn.startMoveTime
        way[mn.myPosY][mn.myPosX] = 'M'  # Если есть данный блок, то заполняем массив M
        monWay[mn.myPosY][mn.myPosX] = 'M'  # Если есть данный блок, то заполняем массив M для монстра
        index += 1
        if mn.algorithm == 444:
            bomb += 1
        elif mn.algorithm == 333:
            mn.myTargetPosX = mn.myPosX
            mn.myTargetPosY = mn.myPosY

    #bigEnergyCounter = maps.amountBigEnerge(way)
    if not PLAY:
        if (amountBigEnergy == 0):
            alg.algWaveFindExit('W', hero, way, 0, monWay, masBlHole)
        else:
            alg.algWaveFindExit('E', hero, way, masBE, monWay, masBlHole)
    elif PLAY:
        maps.printInfo(hero, way) # Выводим карту уровня, если управляет игрок

    #Для идентификации монстров
    #print('')
    #amountMonster = maps.amountMonster(way) #Подсчитываем кол-во монстров на карте
    #monParam = 5 # Имя X Y Alg moveTime #Кол-во параметров массива для каждого монстра
    #hero.monInfo = [[0] * monParam for i in range(amountMonster)] # Создается массив по кол-ву монстров

    # hero.monInfo[0][1][]
    

    #hero.monArray1 = np.array(['Number', 'Name', 'x', 'y', 'Alg', 'moveTime'])

    for mn in masMons:
        hero.monInfo.append(observations.ObservedMonster(-999999, -999999, observations=[observations.Observation(timestamp=-1, x=int(mn.startX/32), y=int(mn.startY/32))]))
        observations.addObservation(hero.monInfo, observations.Observation(timestamp=0, x=int(mn.startX/32), y=int(mn.startY/32)), index=mn.index)
        #print('Name: ' + str(mn.name) + '  Alg: ' + str(mn.algorithm) + '  moveTime: ' + str(mn.moveTime))

    #    hero.monArray1 = np.append(hero.monArray1, [mn, 'Name', 'x', 'y', 'Alg', 'moveTime'])
    #    print('Array: \n' + str(hero.monArray1))
    #1 monstr, 1 zahod, 3 elem

    #maps.printHeroInfo(hero.monInfo) # Вывод информации о массиве
    #print('')

    hero.moveTime = hero.startMoveTime  # Необходима для плавного движения персонажа т.к. его скорость 8 пикселей, а не 32, как расчитана карта(массив)
    # определение времени
    #todayTime = datetime.datetime.today()   #date = todayTime.strftime("%d-%m-%y")   #time = todayTime.strftime("%H-%M-%S")
    slowSpeed = 0  # Переменная для искуственного замедления симулятора
    if PLAY: wait = 0 # Переменная для искуственного замедления симулятора
    else: wait = 4 # Переменная для искуственного замедления симулятора
    stayHide = 0 # Переменная отвечающая за кол-во шагов (moveTime), которое агент просидит в укрытии после того как опасность уйдет

    DELAY = STARTDELAY
    startTime = datetime.datetime.now()
    while True: # Основной цикл программы  #not hero.winner:
        timer.tick(DELAY)
        #slowSpeed -= 1
        if hero.live <= 0 or hero.winner:
            if hero.live <= 0:
                print('Поражение!\n')
            elif hero.winner:
                print('Победа!\n')
            # Подсчитываем время
            if hero.live < 0: hero.live = 0  # Почему-то по итогу эпизода иногда отрицательная жизнь.
            finishTime = datetime.datetime.now() # Время конца цикла
            workTime = finishTime - startTime    # Вычисление времени работы цикла
            #print (workTime) # если написать workTime.seconds то выведется время в секундах
            saveResult(hero, workTime, masMons)
            if (REPEAT == True):
                print('Новый эпизод!')
                #Отрисовываем блоки еще раз
                x = y = 0  # координаты
                for row in level:  # вся строка
                    for col in row:  # каждый символ
                        if col == "-":
                            way[int(y / 32)][int(x / 32)] = 'B'  # Если есть данный блок, то заполняем массив B
                            monWay[int(y / 32)][int(x / 32)] = 'B'  # Если есть данный блок, то заполняем массив B для монстра
                        x += blocks.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                    y += blocks.PLATFORM_HEIGHT  # то же самое и с высотой
                    x = 0  # на каждой новой строчке начинаем с нуля
                hero.winner = False # Возвращаем стартовое значение поля победы
                hero.imDie = False
                hero.live = 2       # Возвращаем стартовое значение жизней
                hero.score = 0      # Возвращаем стартовое значение очков
                hero.amMove = 0     # Выставляем количство шагов на 0
                maps.clearMap(way)  # Очищаем карту от предыдущих путей, энергий, монстров, героя
                maps.clearMonsterMap(monWay)  # Очищаем карту от предыдущих путей, энергий, монстров, героя
                #maps.clearHeroFromMap(way)
                hero.moveTime = hero.startMoveTime
                way[hero.myPosY][hero.myPosX] = 'H'
                if hero.episod % amEpisod == 0: #Для изменения алгоритмов монстров
                    hero.monInfo = [] #append(observations.ObservedMonster(-999999, -999999, observations=[observations.Observation(timestamp=-1, x=int(mn.startX / 32), y=int(mn.startY / 32))]))
                    hero.obsCount = 0
                    hero.indexForThisMon = []
                    hero.myLastPosXforMonTop = -1
                    hero.myLastPosYforMonTop = -1
                    hero.oCforLastMonTop = -1
                    hero.myLastPosXforMonBot = -1
                    hero.myLastPosYforMonBot = -1
                    hero.oCforLastMonBot = -1
                    hero.myLastPosXforMonRight = -1
                    hero.myLastPosYforMonRight = -1
                    hero.oCforLastMonRight = -1
                    hero.myLastPosXforMonLeft = -1
                    hero.myLastPosYforMonLeft = -1
                    hero.oCforLastMonLeft = -1
                    hero.finalAlgCheck111 = []
                    hero.finalAlgCheck222 = []
                    hero.finalAlgCheck333 = []
                    #hero.known = -1
                for mn in masMons:  # Возвращаем монстров на свою позицию
                    Monster.teleporting(mn, mn.startX, mn.startY, platforms, hero, way)
                    Monster.myCoord(mn)
                    mn.moveTime = mn.startMoveTime
                    way[int(mn.rect.y / 32)][int(mn.rect.x / 32)] = 'M'
                    monWay[int(mn.rect.y / 32)][int(mn.rect.x / 32)] = 'M'
                    if hero.episod % amEpisod == 0:
                        hero.monInfo.append(observations.ObservedMonster(-999999, -999999, observations=[observations.Observation(timestamp=-1, x=int(mn.startX / 32), y=int(mn.startY / 32))]))
                        observations.addObservation(hero.monInfo,observations.Observation(timestamp=0, x=int(mn.startX / 32),y=int(mn.startY / 32)), index=mn.index)
                        if mn.name != 'Bomb':
                            numberAlg = random.randint(1, 3)
                            numberMT = random.randint(2, 4)
                            #print ('number: ' + str(numberAlg))
                            if numberAlg == 1:
                                mn.algorithm = 111
                                mn.startMoveTime = numberMT
                                mn.moveOnLeft = mn.moveOnRight = mn.moveOnUp = mn.moveOnDown = False
                                numberLRUD = random.randint(1, 4)
                                if numberLRUD == 1: mn.moveOnLeft = True
                                if numberLRUD == 2: mn.moveOnRight = True
                                if numberLRUD == 3: mn.moveOnUp = True
                                if numberLRUD == 4: mn.moveOnDown = True
                            elif numberAlg == 2:
                                mn.algorithm = 222
                                mn.startMoveTime = numberMT
                            elif numberAlg == 3:
                                mn.algorithm = 333
                                mn.startMoveTime = numberMT
                            print('Name: ' + str(mn.name) + '  Alg: ' + str(mn.algorithm) + '  moveTime: ' + str(mn.moveTime))
                    if mn.algorithm == 333:
                        mn.myTargetPosX = mn.myPosX
                        mn.myTargetPosY = mn.myPosY
                    #mn.myPosX = int(mn.rect.x / 32)
                    #mn.myPosY = int(mn.rect.y / 32)
                    #mn.myPrevPosX = -1
                    #mn.myPrevPosY = -1
                    print('x:   ' + str(mn.rect.x / 32))
                    print('y:   ' + str(mn.rect.y / 32))
                    #Monster.algMove(mn, hero, way)
                for be in masBE: # Распределяем энергии по карте
                    blocks.BigEnergy.teleporting(be, 32 * random.randint(6, 6), 224, platforms, True, way)
                    while (hero.rect.x == be.rect.x and hero.rect.y == be.rect.y) or (ex.rect.x == be.rect.x and ex.rect.y == be.rect.y) or (way[int(be.rect.y / 32)][int(be.rect.x / 32)] == 'M'):
                        blocks.BigEnergy.teleporting(be, 32, 32 * random.randint(4, 5), platforms, True, way)
                    blocks.BigEnergy.myCoord(be)
                    way[int(be.rect.y / 32)][int(be.rect.x / 32)] = 'E'
                amountBigEnergy = maps.amountBigEnerge(way)
                #maps.printInfo(hero, way)
                if not PLAY:
                    if (amountBigEnergy == 0):
                        print('Прокладываю путь до W')
                        alg.algWaveFindExit('W', hero, way, 0, monWay, masBlHole) #Прокладываем новый маршрут до конечной точки
                    else:
                        print('Прокладываю путь до E')
                        alg.algWaveFindExit('E', hero, way, masBE, monWay, masBlHole) #[amountBigEnergy-1]) #Прокладываем новый маршрут до конечной точки
                elif PLAY:
                    maps.printInfo(hero, way)
                #maps.printInfo(hero, way)  # Выводим карту на экран
                #maps.clearNumberFromMap(way) #Очищаем карту от всех прочих путей не вошедших в итоговый маршрут
                startTime = datetime.datetime.now()
            else:
                raise SystemExit("QUIT")

        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                print('Соединение разорвано!')
                #Подсчитываем время
                finishTime = datetime.datetime.now() # Время конца цикла
                workTime = finishTime - startTime    # Вычисление времени работы цикла
                saveResult(hero, workTime, masMons)
                raise SystemExit("QUIT")
            if e.type == KEYUP and e.key == K_SPACE:
                print('Пауза!')
                pause = True
                while pause:
                    for e in pygame.event.get():  # Обрабатываем события
                        if e.type == KEYUP and e.key == K_SPACE:
                            pause = False
                            print('Продолжаем!')
                        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                            raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_MINUS:
                if DELAY > 2:
                    DELAY = 15
                    wait = 4
                    print('Скорость симулятора понижена!   DELAY = ' + str(DELAY))
                else: print('Отказ! Достигнута минимальная разрешенная скорость!   DELAY = ' + str(DELAY))
            if e.type == KEYDOWN and e.key == K_EQUALS:
                DELAY = 999
                wait = 0
                #DELAY += 50
                print('Скорость симулятора повышена!   DELAY = ' + str(DELAY))
            if e.type == KEYDOWN and e.key == K_BACKSPACE:
                DELAY = STARTDELAY
                print('Скорость симулятора восстановлена!   DELAY = ' + str(DELAY))

            if PLAY:
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                #if e.type == KEYDOWN and e.key == K_LSHIFT:
                #    lS = True
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                #if e.type == KEYUP and e.key == K_LSHIFT:
                #    lS = False
                maps.clearHeroFromMap(way)
                way[int(hero.rect.y / 32)][int(hero.rect.x / 32)] = 'H'


        if slowSpeed == 0:
            slowSpeed = wait
            #for mn in masMons:  # Возможно будет актуально, как будет карта личных маршрутов монстров. Но moveTime вычитается чуть позже и из-за этого не обновляется маршрут pendingMove
                #if mn.moveTime <= 0:
                #    maps.clearMonsterWayFromMap(monWay)
            maps.clearMonsterWayFromMap(monWay)
            for bh in masBlHole:
                blocks.BlackHole.myCoord(bh)
                #way[bh.myPosY][bh.myPosX] = '@'
                monWay[bh.myPosY][bh.myPosX] = '@'
            for mn in masMons:  # Алгоритм движения монстров
                if mn.moveTime <= 0:
                    # if mn.myPrevPosY == mn.myPosY and mn.myPrevPosX == mn.myPosX:
                    #    way[mn.myPrevPosY][mn.myPrevPosX] = 'M'
                    # else:
                    way[mn.myPosY][mn.myPosX] = '0'  # Показывает текущую позицию (До выбора следующего пути по алгоритму!)
                    monWay[mn.myPosY][mn.myPosX] = '0'
                    # if way[mn.myPrevPosY][mn.myPrevPosX] != 'H':
                    #    way[mn.myPrevPosY][mn.myPrevPosX] = '0'  # Отмечаем на карте, что ушли с предыдущей позиции
                    if mn.algorithm == 111:
                        Monster.patrolMove(mn, way, monWay)
                        #Monster.monsterPatrolWay(mn, monWay)
                    elif mn.algorithm == 222:
                        Monster.randMove(mn, way, monWay)
                        #Monster.monsterRandWay(mn, monWay)
                    elif mn.algorithm == 333:
                        Monster.pendingMove(mn, monWay , way)
                        #Monster.monsterPendingWay(mn, monWay)

                    if hero.monInfo[mn.index].alg == 111:
                        Monster.monsterPatrolWay(mn, monWay)
                    elif hero.monInfo[mn.index].alg == 222:
                        Monster.monsterRandWay(mn, monWay)
                    elif hero.monInfo[mn.index].alg == 333:
                        Monster.monsterPendingWay(mn, monWay)

                else:
                    mn.moveTime -= 1
                    mn.left = mn.right = mn.up = mn.down = False  # Для плавного движения это убирается

                    if mn.algorithm == 333:
                        Monster.checkForPendingMove(mn, monWay, way)

                    if hero.monInfo[mn.index].alg == 111:
                        Monster.monsterPatrolWay(mn, monWay)
                    elif hero.monInfo[mn.index].alg == 222:
                        Monster.monsterRandWay(mn, monWay)
                    elif hero.monInfo[mn.index].alg == 333:
                        Monster.monsterPendingWay(mn, monWay)

                    #if mn.algorithm == 111:
                    #    Monster.monsterPatrolWay(mn, monWay)
                    #elif mn.algorithm == 222:
                    #    Monster.monsterRandWay(mn, monWay)
                    #elif mn.algorithm == 333:
                    #    Monster.checkForPendingMove(mn, monWay, way)
                    #    Monster.monsterPendingWay(mn, monWay)

                    # way[mn.myPrevPosY][mn.myPrevPosX] = 'M' #На карте видна лишь предыдущая позиция! Куда двигается монстр - не видно!

            for mn in masMons:
                way[mn.myPosY][mn.myPosX] = 'M'  # На карте видна лишь предыдущая позиция! Куда двигается монстр - не видно!
                monWay[mn.myPosY][mn.myPosX] = 'M'  # На карте видна лишь предыдущая позиция! Куда двигается монстр - не видно!
                #print(str(mn.name) + ' MOVETIME: ' + str(mn.moveTime))
                #if mn.moveTime == mn.startMoveTime:
                #maps.printMonsterInfo(monWay)



            if not PLAY:
                alg.identificationAlg(hero, way, masMons, monWay)
                #knownCount = 0
                how333 = 0
                for mn in masMons:
                    if hero.monInfo[mn.index].alg == 333:
                        how333 += 1
                #print('Монстров осталось изучить: ' + str(knownCount) + ' | Episod: ' + str(hero.episod))
                if hero.lastLeft == hero.lastRight == hero.lastUp == hero.lastDown == False:
                    hero.checkMoveTime += 1   #print(colored(str(hero.checkMoveTime), 'cyan'))
                    if hero.checkMoveTime > hero.startMoveTime:
                        hero.moveTime = 0
                else: hero.checkMoveTime = 0
                run = True
                hide = False
                if hero.known == -1: dangerous = False
                else: dangerous = alg.radar(hero, way, masMons, monWay)
                #maps.printInfo(hero, way)
                if hero.moveTime <= 0 or (hero.imDie == True and hero.live > 0):
                    #if amountBigEnergy >= 0:  # Если энергии, которые присутствовали на карте ещё не собраны
                        #way[ex.myPosY][ex.myPosX] = 'W'  # Если есть данный блок, то заполняем массив W
                        #monWay[ex.myPosY][ex.myPosX] = 'W'  # Если есть данный блок, то заполняем массив W для монстра
                        bigEnergyCounter = maps.amountBigEnerge(way)  # тогда сверяем их с текущим количеством на карте
                        amountBigEnergy = 0
                    #if ((bigEnergyCounter != amountBigEnergy and amountBigEnergy >= 0) or hero.imDie == True): #or (bigEnergyCounter == 0): #если кол-во на карте и общее различается, то прокладываем маршрут до следующей цели
                        if hero.imDie == True:
                            hero.imDie = False
                            maps.clearHeroFromMap(way)
                            hero.moveTime = hero.startMoveTime
                            way[hero.myPosY][hero.myPosX] = 'H'
                        #if bigEnergyCounter != amountBigEnergy and amountBigEnergy >= 0:
                            #amountBigEnergy = maps.amountBigEnerge(way)
                        for be in masBE:
                            blocks.BigEnergy.myCoord(be)
                            if be.myPosY > 0 and be.myPosX > 0 and way[be.myPosY][be.myPosX] != 'M':
                                amountBigEnergy += 1
                                way[be.myPosY][be.myPosX] = 'E'
                        if bigEnergyCounter != amountBigEnergy: #Если кол-во энергий на карте != кол-ву энергий фактически, то стираем их и отрисовываем снова
                            maps.deleteBigEnerge(way)
                            print('BigEnergyCounter: ' + str(bigEnergyCounter) + '  |  AmountBigEnergy: ' + str(amountBigEnergy))
                            for be in masBE:
                                blocks.BigEnergy.myCoord(be)
                                if be.myPosY > 0 and be.myPosX > 0 and way[be.myPosY][be.myPosX] != 'M':
                                    way[be.myPosY][be.myPosX] = 'E'
                        maps.clearWayNumFromMap(way) # Очищаем карту, чтобы можно было проложить новый маршрут до другого объекта
                        #amountBigEnergy -= 1  # Уменьшаем общее кол-во энергий
                        #print('Кол-во монстров (без бомб): ' + str(index-bomb) + ' (' + str((index-1-bomb)/2) +') | Алг333: ' + str(how333))
                        if dangerous == True:
                            for bh in masBlHole:
                                if bh.myPosY == hero.myPosY and bh.myPosX == hero.myPosX:
                                    hide = True
                                    stayHide = hero.startMoveTime*3

                        if stayHide <= 0:
                            if dangerous == True and hide == False:
                                symbol = alg.calcWay(hero, way, monWay, '@', 'W')
                                #print('Прокладываю путь до @')
                                if symbol == 'W':
                                    print('Прокладываю путь до W')
                                    alg.algWaveFindExit('W', hero, way, 0, monWay, masBlHole)  # amountBigEnergy-1
                                else:
                                    print('Прокладываю путь до @')
                                    alg.algWaveFindExit('@', hero, way, masBE, monWay, masBlHole)  # [amountBigEnergy-1])
                            elif hide == False:
                                #if (index-1-bomb)/2 > how333:    #Если количество монстров с алгоритмом 333 меньше чем половина монстров, то
                                #    if bigEnergyCounter <= 0: #or amountBigEnergy <= 0: # если энергии на карте закончились, тогда строим путь к выходу
                                #        print('Прокладываю путь до W')
                                #        alg.algWaveFindExit('W', hero, way, 0, monWay, masBlHole) #amountBigEnergy-1
                                #    else:
                                #        print('Прокладываю путь до E')
                                #        alg.algWaveFindExit('E', hero, way, masBE, monWay, masBlHole)#[amountBigEnergy-1])
                                #else:
                                    symbol = alg.calcWay(hero, way, monWay, 'E', 'W')
                                    #print('symbol: ' + str(symbol))
                                    #maps.clearWayNumFromMap(way)  # Очищаем карту, чтобы можно было проложить новый маршрут до другого объекта
                                    if symbol == 'W':
                                        print('Прокладываю путь до W')
                                        alg.algWaveFindExit('W', hero, way, 0, monWay, masBlHole) #amountBigEnergy-1
                                    else:
                                        print('Прокладываю путь до E')
                                        alg.algWaveFindExit('E', hero, way, masBE, monWay, masBlHole)#[amountBigEnergy-1])
                        else: stayHide -= 1
                        #maps.printInfo(hero, way) #Если раскоментить здесь: Отображает виденее героя и его действия

                        #Если на позиции героя иконка монстра, а герой еще жив, значит они совершат движение одновременно
                        #if way[hero.myPosY][hero.myPosX] == 'M':
                        #    hero.wait = True
                        #maps.clearNumFromMap(way)  # очищаю карту от всех возможных путей(чисел) и оставляю только проложенный (+) (для удобства отображения)
                #else: print('Проскочил')
                if hero.moveTime <= 0: # если перемещение героя в планируемую точку закончилось, вычисляем следующее движение
                    # Укажем место героя на карте (почему-то редко-редко теряется)
                    maps.clearHeroFromMap(way)
                    hero.myPosX = int(hero.rect.x / 32)
                    hero.myPosY = int(hero.rect.y / 32)
                    way[int(hero.myPosY)][hero.myPosX] = 'H'  # Добавляем расположение героя на карту (в массив)
                    #way[int(hero.startY / 32)][int(hero.startX / 32)] = 'H'
                    if dangerous == True:
                        for bh in masBlHole:
                            if bh.myPosY == hero.myPosY and bh.myPosX == hero.myPosX:
                                hero.checkMoveTime += 1
                                run = False
                                maps.clearWayNumFromMap(way)
                                #hero.startMoveTime = 15
                                #hero.moveTime = hero.startMoveTime
                    if run == True:
                        if dangerous == True:
                            left, right, up, down, hero.moveTime = alg.algWave(hero, way, monWay, '@')
                        else:
                            left, right, up, down, hero.moveTime = alg.algWave(hero, way, monWay, 'E')
                        #left, right, up, down, hero.moveTime = alg.algWave(hero, way, monWay, '@')

                    if left==True or right==True or up==True or down==True:
                        hero.amMove += 1
                    #maps.printInfo(hero, way) #Если раскоментить здесь: Отображает место куда герой уже наступил
                    #maps.clearNumFromMap(way) # очищаю карту от всех возможных путей(чисел) и оставляю только проложенный (+) (для удобства отображения)

                    #print ("Время движения: " + str(moveTime))
                else:
                    hero.moveTime -= 1
                    left = right = up = down = False #Для плавного движения это убирается
                    maps.clearWayNumFromMap(way)
                    #maps.printInfo(hero, way)
                #print('hero.amMove: ' + str(hero.amMove))

        else: slowSpeed -= 1

        #for mn in masMons: #Для плавного движения
        #    way[mn.myPrevPosY][mn.myPrevPosX] = 'M' #На карте видна лишь предыдущая позиция! Куда двигается монстр - не видно!

        window.blit(screen, (0,0)) # Каждую итерацию необходимо всё перерисовывать экран
        animatedEntities.update()  # показываеaм анимацию
        #mn.update(platforms, mleft, mright, mup, mdown, way)  # передвигаем всех монстров
        if slowSpeed == wait:
            monsters.update(platforms, way, hero)  # передвигаем всех монстров
            hero.updatePlayer(left, right, up, down, platforms, way)  # передвижение игроком
        camera.update(hero)  # центризируем камеру относительно персонажа
        #entities.draw(window) # отображение
        for e in entities:
            window.blit(e.image, camera.apply(e))
        window.blit(score_font.render("Счёт: " + str(hero.score), 1, (255, 255, 255)), (1, 1))
        window.blit(score_font.render("Жизни: " + str(hero.live), 1, (255, 255, 255)), (WIN_WIDTH-165, 1))

        pygame.display.update()     # обновление и вывод всех изменений на экран

        if slowSpeed == wait:
            if PLAY:
                maps.printInfo(hero, way)
            #for mn in masMons:
            #maps.printMonsterInfo(monWay)

masBlHole = []
masBE = []  # Создаем массив для каждого элемента BigEnergy
masMons = [] # Массив со всеми монстрами
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()