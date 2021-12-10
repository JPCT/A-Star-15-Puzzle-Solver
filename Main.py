# -*- coding: UTF-8 -*-
import time
from ManhattanDistance import ManhattanDistance
from AStar import AStar
from Node import Node
from pprint import pprint
import pygame,sys, random
from threading import Thread
from pygame.locals import *


WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (220,220,220)
RED = (255,0,0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
BLUE = (7, 88, 230)
LIGHT_BLUE = (47, 128, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

start = [
            [ 1,  6,  7,  5],
            [ 9,  3, 10,  2],
            [13,  8,  4, 12],
            [14, 11, 15,  0]
        ]

moveName = ""
lastMoveVal = None
WINDOW = 0


def getZeroPosition():
    global start
    for i in range(0, len(start)):
        for j in range(0, len(start[i])):
            if start[i][j] == 0:
                return (i, j)

def calculateMove(result):
    global moveName, lastMoveVal
    
    for move in result:
        pygame.time.delay(1500)

        tuple = getZeroPosition()

        if move == "up":
            tempValue = start[tuple[0] - 1][tuple[1]]
            start[tuple[0]][tuple[1]] = tempValue
            start[tuple[0] - 1][tuple[1]] = 0
            lastMoveVal = tempValue
            moveName = str(tempValue) + " abajo"
        elif move == "down":
            tempValue = start[tuple[0] + 1][tuple[1]]
            start[tuple[0]][tuple[1]] = tempValue
            start[tuple[0] + 1][tuple[1]] = 0
            lastMoveVal = tempValue
            moveName = str(tempValue) + " arriba"
        elif move == "left":
            tempValue = start[tuple[0]][tuple[1] - 1]
            start[tuple[0]][tuple[1]] = tempValue
            start[tuple[0]][tuple[1] - 1] = 0
            lastMoveVal = tempValue
            moveName = str(tempValue) + " derecha"
        elif move == "right":
            tempValue = start[tuple[0]][tuple[1] + 1]
            start[tuple[0]][tuple[1]] = tempValue
            start[tuple[0]][tuple[1] + 1] = 0
            lastMoveVal = tempValue
            moveName = str(tempValue) + " izquierda"

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

def button(msg,x,y,w,h,ic,ac, fontSize, gameDisplay, action=None, parameter=None):

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		AAfilledRoundedRect(gameDisplay, (x,y,w,h), ac, 0.25)


		if click[0] == 1 and action != None:
			if parameter != None:
				action(parameter)
			else:
				action()
	else:
		AAfilledRoundedRect(gameDisplay, (x,y,w,h), ic, 0.25)

	smallText = pygame.font.SysFont("ocraextended", fontSize)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)


def solve():
    global start, result, WINDOW
    heuristic = ManhattanDistance()
    astar = AStar(heuristic)


    startTime = time.time()
    startComplexity = heuristic.compute(
        Node(start, [], None)
    )

    result = astar.solve(start)

    if result is None:
        print('No solution found')
    else:
        WINDOW = 2
        pprint(result)
        
        process = Thread(target = calculateMove, name = "Thread #", args = (result,))
        #daemon: indica si quiero que los hilos mueran cuando el programa se cierre
        process.daemon = True
        process.start()

        
        print('Heuristic said at least %d moves were needed.' % startComplexity)
        print('Actually solution is %d moves away. Best solution found guaranteed!' % len(result))
        print('Solved in %d seconds.' % (time.time() - startTime))

def solveThread():
    global WINDOW
    WINDOW = 1

    process = Thread(target = solve, name = "Thread #")
    #daemon: indica si quiero que los hilos mueran cuando el programa se cierre
    process.daemon = True
    process.start()


def choseNameWindow():
    global WINDOW
    pygame.init()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Proyecto: 15-Puzzle")
    running = True #Estado de la ventana
    font = pygame.font.SysFont("italic", 60)
    fontBig = pygame.font.SysFont("ocraextended", 60)
    fontMedium = pygame.font.SysFont("ocraextended", 40)
    fontSmall = pygame.font.SysFont("ocraextended", 20)
    running = True #Estado de la ventana
    # input_box1 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 200, 120, 120)
    # input_box2 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box3 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box4 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box5 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box6 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box7 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box8 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box9 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box10 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box11 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box12 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box13 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box14 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box15 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)
    # input_box16 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 120, 50)

    input_boxes = []
    xValueInput = 200
    yValueInput = 150
    for i in range(0,4):
        for j in range(0,4):
            input_boxes.append(pygame.Rect((xValueInput + (j * 120) - 50, yValueInput + (i * 120) - 50, 120, 120)))
    
    color_inactive = (193, 193, 193)
    color_active = BLACK

    colors = []
    active = []
    texts = []
    names = []
    matrixValues = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    random.shuffle(matrixValues)
    for i in range(0,16):
        colors.append(color_inactive)
        active.append(False)
        texts.append(str(matrixValues[i]))
        names.append("")

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for i in range(0, len(input_boxes)):
                    if active[i]:
                        if event.key == pygame.K_BACKSPACE:
                            texts[i] = texts[i][:-1]
                        elif len(texts[i]) < 2:
                            texts[i] += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                for i in range(0, len(input_boxes)):
                    if input_boxes[i].collidepoint(event.pos):
                        # Toggle the active variable.
                        active[i] = not active[i]
                        if texts[i] == str(matrixValues[i]):
                            texts[i]=''
                    else:
                        active[i] = False
                    # Change the current color of the input box.
                    colors[i] = color_active if active[i] else color_inactive

        surface.fill(WHITE)

        titleMessage = font.render("15-Puzzle", True, BLACK)
        titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
        surface.blit(titleMessage, titleMessage_rect)

        if WINDOW == 0:
            for i in range(0, len(input_boxes)):
                txt_surface = fontMedium.render(texts[i], True, colors[i])
                width = max(120, txt_surface.get_width())
                input_boxes[i].w = width
                surface.blit(txt_surface, (input_boxes[i].x, input_boxes[i].y))
                pygame.draw.rect(surface, colors[i], input_boxes[i], 2)
                names[i] = texts[i] if texts[i] != '' else texts[i]

            button("Inicio", 300, 700, 200, 50, BLUE, LIGHT_BLUE,30, surface, solveThread)
        elif WINDOW == 1:
            titleMessage = font.render("CARGANDO", True, BLACK)
            titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 400))
            surface.blit(titleMessage, titleMessage_rect)
        else:
            continueMessage = font.render(moveName, True, BLACK)
            continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 720))
            surface.blit(continueMessage, continueMessage_rect)

            titleMessage = font.render("15-Puzzle", True, BLACK)
            titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
            surface.blit(titleMessage, titleMessage_rect)

            xValue = 200
            yValue = 150
            
            for i in range(0, len(start)):
                for j in range(0, len(start[i])):
                    pygame.draw.rect(surface, (BLACK), (xValue + (j * 120) - 50, yValue + (i * 120) - 50, 120, 120), 2)
                    if start[i][j] != 0 and start[i][j] != lastMoveVal:
                        if start[i][j] > 9:
                            continueMessage = font.render(str(start[i][j]), True, BLACK)
                            surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                        else:
                            continueMessage = font.render(str(start[i][j]), True, BLACK)
                            surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))
                    if start[i][j] == lastMoveVal:
                        if start[i][j] > 9:
                            continueMessage = font.render(str(start[i][j]), True, RED)
                            surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                        else:
                            continueMessage = font.render(str(start[i][j]), True, RED)
                            surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))

        pygame.display.update()


def openWindow():
    global start, moveName, lastMoveVal



    pygame.init()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Proyecto: 15-Puzzle")
    running = True #Estado de la ventana
    font = pygame.font.SysFont("italic", 60)


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()


        surface.fill(WHITE)

        continueMessage = font.render(moveName, True, BLACK)
        continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 720))
        surface.blit(continueMessage, continueMessage_rect)

        titleMessage = font.render("15-Puzzle", True, BLACK)
        titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
        surface.blit(titleMessage, titleMessage_rect)

        xValue = 200
        yValue = 150
        
        for i in range(0, len(start)):
            for j in range(0, len(start[i])):
                pygame.draw.rect(surface, (BLACK), (xValue + (j * 120) - 50, yValue + (i * 120) - 50, 120, 120), 2)
                if start[i][j] != 0 and start[i][j] != lastMoveVal:
                    if start[i][j] > 9:
                        continueMessage = font.render(str(start[i][j]), True, BLACK)
                        surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                    else:
                        continueMessage = font.render(str(start[i][j]), True, BLACK)
                        surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))
                if start[i][j] == lastMoveVal:
                    if start[i][j] > 9:
                        continueMessage = font.render(str(start[i][j]), True, RED)
                        surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                    else:
                        continueMessage = font.render(str(start[i][j]), True, RED)
                        surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))
        
        pygame.display.update()



choseNameWindow()





