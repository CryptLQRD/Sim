#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import numpy
import pyganim
from pygame import *
#from player import *
import player
#from blocks import *
import blocks
from monsters import *
import alg
import datetime
import time as tm
from time import sleep


#Объявляем переменные
WIN_WIDTH = 1024#672  #800   #Ширина создаваемого окна
WIN_HEIGHT = 800#384 #640   # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#003300"
#INFO_STRING_WIDTH = 165 # Ширина
#INFO_STRING_HEIGHT = 32 # Высота !!!ЕСЛИ БУДУ МЕНЯТЬ, ТО И В КАМЕРЕ НЕ ЗАБЫТЬ!!!
#INFO_STRING_COLOR = "#006000"
#PLAY = True    # Включить\Выключить управление игроком
#REPEAT = False # Включить\Выключить повторние игры с начала

FILE_DIR = os.path.dirname(__file__)


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

    levelFile = open('%s/levels/lvl1.txt' % FILE_DIR)
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
                    mn = Bat(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)
                if commands[0] == "monsterWraith":  # если первая команда monster, то создаем монстра
                    mn = Wraith(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


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
    resultFile.write('Эпизод № '+ str(episod) + '   Время: ' + str(workTime) + '\n') # выполнения эпизода
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

    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = blocks.Block(x,y)
                entities.add(pf)
                platforms.append(pf)
                way[int(y/32)][int(x/32)] = 1 #Если есть данный блок, то заполняем массив 1
            if col == "*":
                bd = blocks.BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
                way[int(y/32)][int(x/32)] = 1 #Если есть данный блок, то заполняем массив 1
            if col == "E":
                be = blocks.BigEnergy(x,y)
                entities.add(be)
                platforms.append(be)
                animatedEntities.add(be)
            if col == "W":
                pr = blocks.Exit(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
                way[int(y / 32)][int(x / 32)] = 2  # Если есть данный блок, то заполняем массив 2
            if col == "P":
                way[int(y / 32)][int(x / 32)] = 3  # Если есть данный блок, то заполняем массив 2

            x += blocks.PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += blocks.PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    #Выводим карту уровня
    print ("Карта уровня:")
    for row in way:
        for elem in row:
            print(elem, end=' ')
        print()
    print('')

    moveTime = 0
    PLAY = False   # Включить\Выключить управление игроком
    REPEAT = True # Включить\Выключить повторние игры с начала

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
                hero.winner = False
                hero.live = 3
                hero.score = 0
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
            if moveTime <= 0:
                #left, right, up, down, moveTime = alg.testMap(left, right, up, down, moveTime, hero, platforms, way)
                left, right, up, down, moveTime = alg.testRandom(left, right, up, down, moveTime)
                print ("Время движения: " + str(moveTime))
            else:
                moveTime -= 1

        window.blit(screen, (0,0)) # Каждую итерацию необходимо всё перерисовывать экран
        animatedEntities.update()  # показываеaм анимацию
        monsters.update(platforms) # передвигаем всех монстров
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.updatePlayer(left, right, up, down, platforms) # передвижение игроком
        #entities.draw(window) # отображение
        for e in entities:
            window.blit(e.image, camera.apply(e))
        window.blit(score_font.render("Счёт: " + str(hero.score), 1, (255, 255, 255)), (1, 1))
        window.blit(score_font.render("Жизни: " + str(hero.live), 1, (255, 255, 255)), (WIN_WIDTH-165, 1))
        # перерисовываем строку информации
        #info_string.clear()


        pygame.display.update()     # обновление и вывод всех изменений на экран
        
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()