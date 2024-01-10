import pygame
import sys
import math
sys.path.append('../GoGolf')
from Logger import *


pygame.init()

# Logger
LOGGER = logging.getLogger(f"{__name__}")
starting_check()

# Game window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366
LOWER_MARGIN = 100
SIDE_MARGIN = 300

#Colours
Blue = "#2596be"

screen = pygame.display.set_mode(((SCREEN_WIDTH + SIDE_MARGIN), (SCREEN_HEIGHT + LOWER_MARGIN)))
pygame.display.set_caption("GoGolf Level Editor")

# Images
background_img = pygame.image.load('Levels/Level1/bg.png').convert_alpha()

def draw_background(background_scroll):
    tiles = math.ceil((SCREEN_WIDTH - SIDE_MARGIN) / background_img.get_width()) + 1
    background_widith = background_img.get_width()
    print(tiles)
    for i in range(0, tiles):
        screen.blit(background_img, (i * background_widith + background_scroll, 0))

    if abs(background_scroll) > background_widith:
            background_scroll = 0

    #Reset Scroll (For going backward)
    if abs(background_scroll) <background_widith and background_scroll > 0:
        background_scroll = background_scroll - background_widith

    return background_scroll


def LevelEditorLoop():
    run = True
    background_scroll = 0

    while run:
        screen.fill(color=Blue)  # Fill the screen only once

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        # Modify background_scroll based on user input or scrolling mechanism
        # For example, you can use the arrow keys:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            background_scroll += 5
        if keys[pygame.K_RIGHT]:
            background_scroll -= 5

        background_scroll = draw_background(background_scroll)
        pygame.display.update()

if __name__ == "__main__":
    LOGGER.info('Hello')
    LevelEditorLoop()