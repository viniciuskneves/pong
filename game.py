import pygame, sys
from pygame.locals import *

# Game speed
FPS = 200

# Game's window size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

def main():
    pygame.init()
    global DISPLAY_SURF

    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    # Game main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()
