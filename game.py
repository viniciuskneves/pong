import pygame, sys
from pygame.locals import *

# Game speed
FPS = 200

# Game's window size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

# Arena settings
LINE_THICKNESS = 10
PADDLE_SIZE = 50
PADDLE_OFFSET = 20

# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Draws the game arena
def drawArena():
    DISPLAY_SURF.fill((0, 0, 0)) # Screen background
    # Draws the boundaries - (surface, color, ((top-cord, left-cord), (width, height)), thickness) - Half of the thickness is outside of the rectangle/window
    pygame.draw.rect(DISPLAY_SURF, WHITE, ((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS * 2)
    # Draws the center line
    pygame.draw.line(DISPLAY_SURF, WHITE, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), LINE_THICKNESS / 4)

# Draws a paddle
def drawPaddle(paddle):
    # Stop paddle moving too low or too high (out of boundaries)
    if paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
        paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS
    elif paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS;
    # Draws the paddle rectangle
    pygame.draw.rect(DISPLAY_SURF, WHITE, paddle)

# Draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAY_SURF, WHITE, ball)

# Moves the ball -- returns new ball position
def moveBall(ball, direction_x, direction_y):
    ball.x += direction_x
    ball.y += direction_y
    return ball

def main():
    pygame.init()
    global DISPLAY_SURF

    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    # Initial positions - Ball in the center - Paddles in the middle
    ball_x = (WINDOW_WIDTH - LINE_THICKNESS) / 2
    ball_y = (WINDOW_HEIGHT - LINE_THICKNESS) / 2
    player_left_position = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    player_right_position = (WINDOW_HEIGHT - PADDLE_SIZE) / 2

    # Create rectangles (x-cord, y-cord, width, height)
    paddle_left = pygame.Rect(PADDLE_OFFSET, player_left_position, LINE_THICKNESS, PADDLE_SIZE)
    paddle_right = pygame.Rect(WINDOW_WIDTH - PADDLE_OFFSET - LINE_THICKNESS, player_right_position, LINE_THICKNESS, PADDLE_SIZE)
    ball = pygame.Rect(ball_x, ball_y, LINE_THICKNESS, LINE_THICKNESS)

    # Defines ball starting directions
    ball_direction_x = -1 # Left --> -1  /  Right --> 1
    ball_direction_y = -1 # Up --> -1  /  Down --> 1

    # Drawing objects
    drawArena()
    drawPaddle(paddle_left)
    drawPaddle(paddle_right)
    drawBall(ball)

    # Game main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        drawArena()
        drawPaddle(paddle_left)
        drawPaddle(paddle_right)
        drawBall(ball)

        ball = moveBall(ball, ball_direction_x, ball_direction_y)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()
