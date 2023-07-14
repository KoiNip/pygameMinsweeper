import random
import time

import pygame

pygame.init()
clock = pygame.time.Clock()

# Width and height of pygame window
WINDOW_WIDTH = 610
WINDOW_HEIGHT = 615
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Width and height of squares in the grid
width = 50
height = 50

# Number of rows and columns in the grid
rows = 11
cols = 11

# Creates a 2D array that represents the grid
grid = [[0 for x in range(12)] for y in range(12)]


# Text class, for drawing text on screen
class Text:
    def __init__(self, screen, color, x, y, size, text):
        font_name = pygame.font.match_font('arial')
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.text = text
        self.font = pygame.font.Font(font_name, self.size)

    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.x, self.y)
        self.screen.blit(text_surface, text_rect)


# Randomly add bombs, and the number surrounding them
i = 0
while i < 15:
    rand1 = random.randint(0, 10)
    rand2 = random.randint(0, 10)
    # If we have already placed a bomb here, stop and decrement i to go again
    if grid[rand1][rand2] >= 9:
        i -= 1
        continue
    # Adding numbers around the bomb
    if rand1 > 0:
        grid[rand1 - 1][rand2] += 1
        grid[rand1 - 1][rand2 + 1] += 1

    if rand2 > 0:
        grid[rand1][rand2 - 1] += 1
        grid[rand1 + 1][rand2 - 1] += 1

    if rand1 > 0 and rand2 > 0:
        grid[rand1 - 1][rand2 - 1] += 1

    grid[rand1 + 1][rand2] += 1
    grid[rand1 + 1][rand2 + 1] += 1
    grid[rand1][rand2 + 1] += 1
    grid[rand1][rand2] = 9
    i += 1

# Creates the text grid with all the text for the tiles
text_grid = [[0 for k in range(11)] for g in range(11)]
for i in range(11):
    for o in range(11):
        text_grid[i][o] = Text(screen, (255, 255, 255), i * 56, o * 56, 25, str(grid[i][o]))

# Creates array of text that needs to be drawn
draw_text = []


# Reveals all bombs when the game is lost
def reveal_bomb():
    for h in range(0, WINDOW_WIDTH, 56):
        for j in range(0, WINDOW_HEIGHT, 56):
            color = (100, 100, 100)
            if grid[int(h / 56)][int(j / 56)] >= 9:
                color = (255, 0, 0)
                pygame.draw.rect(screen, color, (h, j, width, height))
            pygame.draw.rect(screen, color, (h, j, width, height))


# Draws the grid
def draw_grid():
    lost_v = False
    for x in range(0, WINDOW_WIDTH, 56):
        for y in range(0, WINDOW_HEIGHT, 56):
            color = (100, 100, 100)
            # if grid[int(x / 56)][int(y / 56)] >= 9:
            #    color = (255, 0, 0)
            # elif grid[int(x / 56)][int(y / 56)] >= 1:
            #    color = (0, 255, 0)
            pygame.draw.rect(screen, color, (x, y, width, height))

    if pygame.mouse.get_pressed()[0] == 1:
        x, y = pygame.mouse.get_pos()
        if grid[int(x / 56)][int(y / 56)] >= 9:
            lost_v = True
        draw_text.append(
            text_grid[int(x / 56)][int(y / 56)])  # When we click on a tile, add it to the list of clicked tiles
        time.sleep(.2)
    return lost_v


lost = False
win = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
    screen.fill((0, 0, 0))
    if not lost:
        if draw_grid():
            lost = True
    if lost:
        reveal_bomb()

    # Draw all numbers on the screen
    for number in draw_text:
        number.draw()

# Detects when we win the game
    win_v = True
    for i in range(11):
        for j in range(11):
            if grid[i][j] < 9:
                if text_grid[i][j] not in draw_text:
                    win_v = False
    if win_v:
        print("You win!")
