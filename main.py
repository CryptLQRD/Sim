#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
import numpy
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



#Объявляем переменные
WIN_WIDTH = 800#672  #1024   #Ширина создаваемого окна
WIN_HEIGHT = 640#384 #800   # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#003300"
#INFO_STRING_WIDTH = 165 # Ширина
#INFO_STRING_HEIGHT = 32 # Высота !!!ЕСЛИ БУДУ МЕНЯТЬ, ТО И В КАМЕРЕ НЕ ЗАБЫТЬ!!!
#INFO_STRING_COLOR = "#006000"
#PLAY = True    # Включить\Выключить управление игроком
#REPEAT = False # Включить\Выключить повторние игры с начала
levelName = 'lvl1.txt' #Название уровня
FILE_DIR = os.path.dirname(__file__)
PLAY = False  # Включить\Выключить управление игроком
REPEAT = True  # Включить\Выключить повторние игры с начала


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
                    mn = Bat(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)
                    #monsters.myCoord(mn)
                if commands[0] == "monsterWraith":  # если первая команда monster, то создаем монстра
                    mn = Wraith(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                    #Добавляем монстра в массив
                    masMons.append(mn)


def saveResult(hero, workTime): # Работа с файлом result
    #Определяем № эпизода
    resultFile = open('%s/levels/episodes/result.txt' % FILE_DIR)
    episod = 0
    line = " "
    commands = []
    if line[0] != "":
        for line in resultFile.readlines():
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "Эпизод" and commands[1] == "№":
                    episod = int(commands[2])
    episod += 1
    resultFile.close()

    #Сохраняем в файл
    resultFile = open('%s/levels/episodes/result.txt' % FILE_DIR, 'a')
    resultFile.write('Эпизод № '+ str(episod) + '   Время: ' + str(workTime) + '   Уровень: ' +  levelName +'\n') # выполнения эпизода
    if (hero.live <= 0):
        resultFile.write('Поражение!')
    elif (hero.winner):
        resultFile.write('Победа!')
    else:
        resultFile.write('Соединение разорвано!')
    resultFile.write('  |  Счёт: ' + str(hero.score) + '  |  Жизни: ' + str(hero.live) + '\n\n')
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

    total_level_width  = len(level[0])*blocks.PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*blocks.PLATFORM_HEIGHT   # Высчитываем фактическую высоту уровня
    print ("Размер уровня:   Ширина: " + str(total_level_width) + "   Высота: " + str(total_level_height))
    camera = Camera(camera_configure, total_level_width, total_level_height)
    blocks.levelSize(total_level_width, total_level_height)  # Определение размера уровня для метода teleporting класса BigEnergy

    way = [[0] * len(level[0]) for i in range(len(level))] # Создаем карту уровня для алгоритма


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
            if col == "*":
                bd = blocks.BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
                way[int(y/32)][int(x/32)] = 'B' #Если есть данный блок, то заполняем массив B
            if col == "E":
                be = blocks.BigEnergy(x,y)
                entities.add(be)
                platforms.append(be)
                animatedEntities.add(be)
                way[int(y / 32)][int(x / 32)] = 'E' #Если есть данный блок, то заполняем массив E
                masBE.append(be)
                blocks.BigEnergy.myCoord(be)
                amountBigEnergy += 1 # Запоминаем кол-во энергий на карте
                #blocks.Platform.rect = (be, )
                #blocks.BigEnergy.be.myPosX = int(x/32)
                #blocks.BigEnergy.be.myPosY = int(y/32)
            if col == "W":
                ex = blocks.Exit(x,y)
                entities.add(ex)
                platforms.append(ex)
                animatedEntities.add(ex)
                way[int(y / 32)][int(x / 32)] = 'W' # Если есть данный блок, то заполняем массив W
                blocks.Exit.myPosX = int(x/32)
                blocks.Exit.myPosY = int(y/32)

            x += blocks.PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += blocks.PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    for mn in masMons:
        Monster.myCoord(mn)
        way[mn.myPosY][mn.myPosX] = 'M'  # Если есть данный блок, то заполняем массив M
    #    print('BigEnergy.myPosX: ' + str(i.myPosX) + '   BigEnergy.myPosY: ' + str(i.myPosY))

    bigEnergyCounter = maps.amountBigEnerge(way)
    if not PLAY:
        if (amountBigEnergy == 0):
            alg.algWaveFindExit('W', hero, way, 0)
        else:
            alg.algWaveFindExit('E', hero, way, masBE) #[amountBigEnergy-1])
    elif PLAY:
        maps.printInfo(hero, way)

    #Выводим карту уровня
    #maps.clearNumberFromMap(way)

    moveTime = 0  # Необходима для плавного движения персонажа т.к. его скорость 8 пикселей, а не 32, как расчитана карта(массив)
    # определение времени
    #todayTime = datetime.datetime.today()   #date = todayTime.strftime("%d-%m-%y")   #time = todayTime.strftime("%H-%M-%S")
    startTime = datetime.datetime.now()
    while True: # Основной цикл программы  #not hero.winner:
        timer.tick(40)
        if hero.live <= 0 or hero.winner:
            if hero.live <= 0:
                print('Поражение!\n')
            elif hero.winner:
                print('Победа!\n')
            # Подсчитываем время
            finishTime = datetime.datetime.now() # Время конца цикла
            workTime = finishTime - startTime    # Вычисление времени работы цикла
            #print (workTime) # если написать workTime.seconds то выведется время в секундах
            saveResult(hero, workTime)
            if (REPEAT == True):
                print('Новый эпизод!')
                hero.winner = False # Возвращаем стартовое значение поля победы
                hero.imDie = False
                hero.live = 3       # Возвращаем стартовое значение жизней
                hero.score = 0      # Возвращаем стартовое значение очков
                maps.clearMap(way)  # Очищаем карту от предыдущих путей, энергий, монстров, героя
                #maps.clearHeroFromMap(way)
                moveTime = 0
                way[hero.myPosY][hero.myPosX] = 'H'
                for mn in masMons:  # Возвращаем монстров на свою позицию
                    Monster.teleporting(mn, mn.startX, mn.startY, platforms, hero, way)
                    Monster.myCoord(mn)
                    mn.moveTime = 0
                    way[int(mn.rect.y / 32)][int(mn.rect.x / 32)] = 'M'
                    Monster.algMove(mn, way)
                for be in masBE:
                    blocks.BigEnergy.teleporting(be, 32 * random.randint(3, 3), 64, platforms, True)
                    while (hero.rect.x == be.rect.x and hero.rect.y == be.rect.y) or (ex.rect.x == be.rect.x and ex.rect.y == be.rect.y) or (way[int(be.rect.y / 32)][int(be.rect.x / 32)] == 'M'):
                        blocks.BigEnergy.teleporting(be, 32, 32 * random.randint(4, 5), platforms, True)
                    blocks.BigEnergy.myCoord(be)
                    way[int(be.rect.y / 32)][int(be.rect.x / 32)] = 'E'
                amountBigEnergy = maps.amountBigEnerge(way)
                if not PLAY:
                    if (amountBigEnergy == 0):
                        print('Прокладываю путь до W')
                        alg.algWaveFindExit('W', hero, way, 0) #Прокладываем новый маршрут до конечной точки
                    else:
                        print('Прокладываю путь до E')
                        alg.algWaveFindExit('E', hero, way, masBE) #[amountBigEnergy-1]) #Прокладываем новый маршрут до конечной точки
                elif PLAY:
                    maps.printInfo(hero, way)
                #maps.printInfo(hero, way)  # Выводим карту на экран
                #maps.clearNumberFromMap(way) #Очищаем карту от всех прочих путей не вошедших в итоговый маршрут
                startTime = datetime.datetime.now()
            else:
                raise SystemExit("QUIT")
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                print('Соединение разорвано!')
                #Подсчитываем время
                finishTime = datetime.datetime.now() # Время конца цикла
                workTime = finishTime - startTime    # Вычисление времени работы цикла
                saveResult(hero, workTime)
                raise SystemExit("QUIT")
            if e.type == KEYUP and e.key == K_SPACE:
                print('Пауза!')
                pause = True
                while pause:
                    for e in pygame.event.get():  # Обрабатываем события
                        if e.type == KEYUP and e.key == K_SPACE:
                            pause = False
                            print('Продолжаем!')
                        if e.type == QUIT:
                            raise SystemExit("QUIT")

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

        if not PLAY:

            if moveTime == 0 or (hero.imDie == True and hero.live > 0):
                #if hero.imDie == True:
                    #hero.imDie = False
                if amountBigEnergy >= 0:  # Если энергии, которые присутствовали на карте ещё не собраны
                    bigEnergyCounter = maps.amountBigEnerge(way)  # тогда сверяем их с текущим количеством на карте
                    print('BigEnergyCounter: ' + str(bigEnergyCounter) + '  ;  AmountBigEnergy: ' + str(amountBigEnergy))
                if ((bigEnergyCounter != amountBigEnergy and amountBigEnergy >= 0) or hero.imDie == True): #or (bigEnergyCounter == 0): #если кол-во на карте и общее различается, то прокладываем маршрут до следующей цели
                    if hero.imDie == True:
                        hero.imDie = False
                        maps.clearHeroFromMap(way)
                        moveTime = 0
                        way[hero.myPosY][hero.myPosX] = 'H'
                    if bigEnergyCounter != amountBigEnergy and amountBigEnergy >= 0:
                        amountBigEnergy = maps.amountBigEnerge(way)
                    for be in masBE:
                        blocks.BigEnergy.myCoord(be)
                    maps.clearWayNumFromMap(way) # Очищаем карту, чтобы можно было проложить новый маршрут до другого объекта
                    #amountBigEnergy -= 1  # Уменьшаем общее кол-во энергий
                    if bigEnergyCounter <= 0 or amountBigEnergy <= 0: # если энергии на карте закончились, тогда строим путь к выходу
                        print('Прокладываю путь до W')
                        alg.algWaveFindExit('W', hero, way, 0) #amountBigEnergy-1
                    else:
                        print('Прокладываю путь до E')
                        alg.algWaveFindExit('E', hero, way, masBE)#[amountBigEnergy-1])
            #else: print('Проскочил')
            if moveTime <= 0: # если перемещение героя в планируемую точку закончилось, вычисляем следующее движение
                left, right, up, down, moveTime = alg.algWave(hero, way)
                maps.clearNumFromMap(way) # очищаю карту от всех возможных путей(чисел) и оставляю только проложенный (+) (для удобства отображения)

                #print ("Время движения: " + str(moveTime))
            else:
                moveTime -= 1


        for mn in masMons: #Алгоритм движения монстров
            if mn.moveTime <= 0:
                Monster.algMove(mn, way)
            else: mn.moveTime -= 1
        #maps.printInfo(hero, way)


        window.blit(screen, (0,0)) # Каждую итерацию необходимо всё перерисовывать экран
        animatedEntities.update()  # показываеaм анимацию
        #mn.update(platforms, mleft, mright, mup, mdown, way)  # передвигаем всех монстров
        monsters.update(platforms, way, hero) # передвигаем всех монстров
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.updatePlayer(left, right, up, down, platforms, way) # передвижение игроком
        #entities.draw(window) # отображение
        for e in entities:
            window.blit(e.image, camera.apply(e))
        window.blit(score_font.render("Счёт: " + str(hero.score), 1, (255, 255, 255)), (1, 1))
        window.blit(score_font.render("Жизни: " + str(hero.live), 1, (255, 255, 255)), (WIN_WIDTH-165, 1))

        pygame.display.update()     # обновление и вывод всех изменений на экран
        #maps.printInfo(hero, way)

masBE = []  # Создаем массив для каждого элемента BigEnergy
masMons = [] # Массив со всеми монстрами
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()