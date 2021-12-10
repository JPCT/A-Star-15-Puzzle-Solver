import time
from ManhattanDistance import ManhattanDistance
from AStar import AStar
from Node import Node
from pprint import pprint
import pygame,sys, random
from threading import Thread
from pygame.locals import *
import collections

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
ERROR_MESSAGE = ""
TIME_SEARCHING = 0
SOLUTION_FINDED = False
MOVEMENTS_NEEDED = 0
START_COMPLEXITY = 0

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

def timeCounterThread():
    global TIME_SEARCHING, SOLUTION_FINDED
    while not SOLUTION_FINDED:
        TIME_SEARCHING += 1
        pygame.time.delay(1000)


def solve():
    global start, WINDOW, SOLUTION_FINDED, MOVEMENTS_NEEDED, START_COMPLEXITY

    process = Thread(target = timeCounterThread, name = "Thread TimeCounter")
    process.daemon = True
    process.start()

    heuristic = ManhattanDistance()
    astar = AStar(heuristic)

    startComplexity = heuristic.compute(
        Node(start, [], None)
    )

    result = astar.solve(start)

    SOLUTION_FINDED = True

    if result is None:
        print('No se encontro solución en ' + TIME_SEARCHING + " segundos")
        WINDOW = 2
        exit()
    else:
        WINDOW = 2

        process = Thread(target = calculateMove, name = "Thread #", args = (result,))
        process.daemon = True
        process.start()

        START_COMPLEXITY = startComplexity
        MOVEMENTS_NEEDED = len(result)


def verifyValues(values):
    expectedValues = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    for i in range(0,len(values)):
        try:
            values[i] = int(values[i])
        except:
            return (False, "Valor incorrecto (" + values[i] + ")")
        
    if not (collections.Counter(expectedValues) == collections.Counter(values)):
        return (False, "No fueron indicados todos los números requeridos 0-15")
    return (True, "Exito")

def fillMatrix(values):
    global start
    iterator = 0
    for i in range(0, 4):
        for j in range(0, 4):
            start[i][j] = values[iterator]
            iterator += 1

def solveThread(values):
    global WINDOW, ERROR_MESSAGE
    WINDOW = 1
    tuple = verifyValues(values)
    
    if tuple[0] == False:
        ERROR_MESSAGE = tuple[1]
        WINDOW = 0
        return
    fillMatrix(values)

    process = Thread(target = solve, name = "Thread Solve")
    process.daemon = True
    process.start()


def choseNameWindow():
    global WINDOW, ERROR_MESSAGE, TIME_SEARCHING, START_COMPLEXITY
    pygame.init()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Proyecto: 15-Puzzle")
    running = True #Estado de la ventana
    fontBig = pygame.font.SysFont("italic", 60)
    fontMedium = pygame.font.SysFont("italic", 40)
    fontSmall = pygame.font.SysFont("italic", 30)
    running = True #Estado de la ventana

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
                            texts[i] = str(texts[i])[:-1]
                        elif len(str(texts[i])) < 2:
                            texts[i] += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(input_boxes)):
                    if input_boxes[i].collidepoint(event.pos):
                        active[i] = not active[i]
                        if texts[i] == str(matrixValues[i]):
                            texts[i]=''
                    else:
                        active[i] = False
                    colors[i] = color_active if active[i] else color_inactive

        surface.fill(WHITE)

        titleMessage = fontBig.render("15-Puzzle", True, BLACK)
        titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
        surface.blit(titleMessage, titleMessage_rect)

        if WINDOW == 0:
            for i in range(0, len(input_boxes)):
                txt_surface = fontMedium.render(str(texts[i]), True, colors[i])
                width = max(120, txt_surface.get_width())
                input_boxes[i].w = width
                surface.blit(txt_surface, (input_boxes[i].x + 50, input_boxes[i].y + 50))
                pygame.draw.rect(surface, colors[i], input_boxes[i], 2)
                names[i] = texts[i] if texts[i] != '' else texts[i]

            errorMessage = fontSmall.render(ERROR_MESSAGE, True, RED)
            errorMessage_rect = errorMessage.get_rect(center=(SCREEN_WIDTH/2, 650))
            surface.blit(errorMessage, errorMessage_rect)

            button("Iniciar", 300, 700, 200, 50, BLUE, LIGHT_BLUE,30, surface, solveThread, texts)
        elif WINDOW == 1:
            if TIME_SEARCHING % 2 == 0: 
                searchingMessage = fontMedium.render("Buscando la solución más optima...", True, BLACK)
                searchingMessage_rect = (170, 400, 50, 50)
                surface.blit(searchingMessage, searchingMessage_rect)
            else:
                searchingMessage = fontMedium.render("Buscando la solución más optima.", True, BLACK)
                searchingMessage_rect = (170, 400, 50, 50)
                surface.blit(searchingMessage, searchingMessage_rect)

            timeLabelMessage = fontSmall.render("Tiempo transcurrido", True, BLACK)
            timeLabelMessage_rect = timeLabelMessage.get_rect(center=(SCREEN_WIDTH/2, 600))
            surface.blit(timeLabelMessage, timeLabelMessage_rect)

            timeMessage = fontSmall.render(str(TIME_SEARCHING) + " segundos", True, BLACK)
            timeMessage_rect = timeMessage.get_rect(center=(SCREEN_WIDTH/2, 650))
            surface.blit(timeMessage, timeMessage_rect)
        else:
            continueMessage = fontBig.render(moveName, True, BLACK)
            continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 770))
            surface.blit(continueMessage, continueMessage_rect)

            titleMessage = fontBig.render("15-Puzzle", True, BLACK)
            titleMessage_rect = titleMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
            surface.blit(titleMessage, titleMessage_rect)

            xValue = 200
            yValue = 150
            
            for i in range(0, len(start)):
                for j in range(0, len(start[i])):
                    pygame.draw.rect(surface, (BLACK), (xValue + (j * 120) - 50, yValue + (i * 120) - 50, 120, 120), 2)
                    if start[i][j] != 0 and start[i][j] != lastMoveVal:
                        if start[i][j] > 9:
                            continueMessage = fontBig.render(str(start[i][j]), True, BLACK)
                            surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                        else:
                            continueMessage = fontBig.render(str(start[i][j]), True, BLACK)
                            surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))
                    if start[i][j] == lastMoveVal:
                        if start[i][j] > 9:
                            continueMessage = fontBig.render(str(start[i][j]), True, RED)
                            surface.blit(continueMessage, (xValue + (j * 120) - 10, yValue + (i * 120)))
                        else:
                            continueMessage = fontBig.render(str(start[i][j]), True, RED)
                            surface.blit(continueMessage, (xValue + (j * 120), yValue + (i * 120)))

            complexityMessage = fontSmall.render("Complejidad heuristica: " + str(START_COMPLEXITY), True, BLACK)
            complexityMessage_rect = complexityMessage.get_rect(center=(SCREEN_WIDTH/2, 620))
            surface.blit(complexityMessage, complexityMessage_rect)

            timeMessage = fontSmall.render("Solución encontrada en " + str(TIME_SEARCHING) + " segundos", True, BLACK)
            timeMessage_rect = timeMessage.get_rect(center=(SCREEN_WIDTH/2, 650))
            surface.blit(timeMessage, timeMessage_rect)

            movementsMessage = fontSmall.render(str(MOVEMENTS_NEEDED) + " movimientos necesarios", True, BLACK)
            movementsMessage_rect = movementsMessage.get_rect(center=(SCREEN_WIDTH/2, 680))
            surface.blit(movementsMessage, movementsMessage_rect)

        pygame.display.update()

if __name__ == "__main__":
    choseNameWindow()





