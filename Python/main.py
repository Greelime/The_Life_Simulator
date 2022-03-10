import pygame
import random
import sys

pygame.init()
pygame.display.set_caption('life')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
rand_on = False
pvp_on = False
speed = 100
count = 0
k = 0
countILL = 0
screen = pygame.display.set_mode((1200, 840))

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive = (174, 174, 174)
        self.active = (59, 59, 59)

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active, (x, y, self.width, self.height))
            if click[0] == True:
                action()
        else:
            pygame.draw.rect(screen, self.inactive, (x, y, self.width, self.height))
        print_text(message, x + 10, y + 10)

class ButtonClr:
    def __init__(self, width, height, inactive, active):
        self.width = width
        self.height = height
        self.inactive = inactive
        self.active = active

    def draw(self, x, y, message=None, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active, (x, y, self.width, self.height))
            if click[0] == True:
                action()
        else:
            pygame.draw.rect(screen, self.inactive, (x, y, self.width, self.height))
        print_text(message, x + 10, y + 10)

def random_on():
    global rand_on
    rand_on = True
    pygame.time.delay(50)
    return rand_on

def speedPL():
    global speed
    speed += 50
    pygame.time.delay(50)

def speedNG():
    global speed
    speed -= 50
    if speed < 0:
        speed = 0
    pygame.time.delay(50)

def clear():
    global cells
    cells = [[0 for j in range((screen.get_height()) // 20)] for i in range(screen.get_width() // 20)]
    pygame.time.delay(50)

def print_text(message, x, y, font_color = (black), font_size = 20):
    font = pygame.font.SysFont('Arial', font_size)
    text = font.render(message, True, font_color)
    screen.blit(text, (x,y))

def near(pos: list):
    global count, countILL
    system = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    count = 0
    countILL = 0
    for i in system:
        if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])] == 1:
            count += 1
        if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])] == 2:
            countILL += 1

def kolv(cells):
    global k
    k_unill = 0
    k_ill = 0
    with open('result.txt', "a") as f:
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j] == 1:
                    k_unill += 1
                if cells[i][j] == 2:
                    k_ill += 1
        print(k, k_unill, k_ill, file=f)


buttonRand = Button(100, 40)
buttonPN = Button(30, 40)
buttonPvP = Button(75, 40)
buttonBlue = ButtonClr(40, 40, (255, 0, 0), (111, 0, 0))
buttonRed = ButtonClr(40, 40, (0, 0, 255), (0, 0, 130))

def update(cells):
    screen.fill(white)
    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
            if cells[i][j] == 1:
                pygame.draw.rect(screen, black, [i * 20, j * 20 + 40, 20, 20])
            elif cells[i][j] == 2:
                pygame.draw.rect(screen, red, [i * 20, j * 20 + 40, 20, 20])
            else:
                pygame.draw.rect(screen, white, [i * 20, j * 20 + 40, 20, 20])

    for i in range(2, (screen.get_height()) // 20):
        pygame.draw.line(screen, black, (0, i * 20), (screen.get_width(), i * 20))
    for j in range(screen.get_width() // 20):
        pygame.draw.line(screen, black, (j * 20, 40), (j * 20, screen.get_height()))
    buttonRand.draw(0, 0, 'Random', random_on)
    buttonPN.draw(110, 0, '+', speedPL)
    buttonPN.draw(140, 0, '-', speedNG)
    buttonRand.draw(1100, 0, 'Clear', clear)
    print_text(('Current delay (ms): ' + str(speed)), 180, 10)
    pygame.display.flip()

game_on = False
game_set = True

cells = [[0 for j in range((screen.get_height()) // 20)] for i in range(screen.get_width() // 20)]


while True:
    while game_set:
        update(cells)
        if rand_on:
            cells = [[random.choice([0, 1]) for j in range((screen.get_height()) // 20)] for i in range(screen.get_width() // 20)]
            rand_on = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = event.pos
                    if cells[position[0] // 20][position[1] // 20 - 2] == 0:
                        cells[position[0] // 20][position[1] // 20 - 2] = 1
                    else:
                        cells[position[0] // 20][position[1] // 20 - 2] = 0
                elif event.button == 3:
                    position = event.pos
                    if (cells[position[0] // 20][position[1] // 20 - 2] == 0) or (cells[position[0] // 20][position[1] // 20 - 2] == 1):
                        cells[position[0] // 20][position[1] // 20 - 2] = 2
                    else:
                        cells[position[0] // 20][position[1] // 20 - 2] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_set = False
                    game_on = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    while game_on:
        k += 1
        cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                near([i, j])
                if cells[i][j] != 0:
                    if (count + countILL) not in (2, 3):
                        cells2[i][j] = 0
                    elif countILL >= 3 and cells[i][j] == 1:
                        cells2[i][j] = 2
                    elif countILL == 2 and cells[i][j] == 1:
                        cells2[i][j] = int(random.choice([1, 2]))
                    elif countILL == 1 and cells[i][j] == 1:
                        q = random.choices([1, 2], weights=[0.75, 0.25])
                        cells2[i][j] = q[0]
                    else:
                        if cells[i][j] == 1:
                            cells2[i][j] = 1
                        if cells[i][j] == 2:
                            cells2[i][j] = 2
                    continue
                else:
                    if (count+countILL) == 3 and countILL < 1:
                        cells2[i][j] = 1
                    elif (count+countILL) == 3 and countILL >= 2:
                        cells2[i][j] = 2
                    elif (count+countILL) == 3 and countILL == 1:
                        cells2[i][j] = int(random.choice([1, 2]))
                    else:
                        cells2[i][j] = 0
        cells = cells2.copy()
        update(cells)
        kolv(cells)
        pygame.time.delay(speed)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_set = True
                    game_on = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

