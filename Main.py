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
    input_box1 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 200, 100, 50)
    input_box2 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 100, 50)
    color_inactive = (193, 193, 193)
    color_active = BLACK
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    text1 = 'Player 1'
    text2 = 'Player 2'
    name1 = ""
    name2 = ""

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    elif len(text1) < 9:
                        text1 += event.unicode
            if active2:
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                elif len(text2) < 9:
                    text2 += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
				# If the user clicked on the input_box rect.
                if input_box1.collidepoint(event.pos):
					# Toggle the active variable.
                    active1 = not active1
                    if text1 == 'Player 1':
                        text1=''
                else:
                    active1 = False
				# Change the current color of the input box.
                color1 = color_active if active1 else color_inactive

                if input_box2.collidepoint(event.pos):
					# Toggle the active variable.
                    active2 = not active2
                    if text2 == 'Player 2':
                        text2=''
                else:
                    active2 = False
				# Change the current color of the input box.
                color2 = color_active if active2 else color_inactive

        surface.fill(WHITE)

        titleMessage = font.render("15-Puzzle", True, BLACK)
        titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
        surface.blit(titleMessage, titleMessage_rect)

        if WINDOW == 0:

            name1Message = fontSmall.render("Nombre jugador 1", True, BLACK)
            surface.blit(name1Message, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 230))

            name1Message = fontSmall.render("Nombre jugador 2", True, BLACK)
            surface.blit(name1Message, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 70))

            # Render the current text.
            txt_surface1 = fontMedium.render(text1, True, color1)
            # Resize the box if the text is too long.
            width1 = max(200, txt_surface1.get_width()+10)
            input_box1.w = width1
            # Blit the text.
            surface.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(surface, color1, input_box1, 2)

            # Render the current text.
            txt_surface2 = fontMedium.render(text2, True, color2)
            # Resize the box if the text is too long.
            width2 = max(200, txt_surface2.get_width() + 10)
            input_box2.w = width2
            # Blit the text.
            surface.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
            # Blit the input_box rect.
            pygame.draw.rect(surface, color2, input_box2, 2)

            name1 = text1 if text1 != '' else "Player 1"
            name2 = text2 if text2 != '' else "Player 2"
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





