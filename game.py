import pygame, sys
from pygame.locals import *

# Game speed
FPS = 500

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
    DISPLAY_SURF.fill(BLACK) # Screen background
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

# Check collision with a wall and bounces off the ball -- returns new directions
def checkEdgeCollision(ball, direction_x, direction_y):
    # Check if it hits the top or the bottom of the arena
    if ball.top == LINE_THICKNESS or ball.bottom == WINDOW_HEIGHT - LINE_THICKNESS:
        direction_y = -direction_y
    # Check if it hits the left or the right of the arena
    if ball.left == LINE_THICKNESS or ball.right == WINDOW_WIDTH - LINE_THICKNESS:
        direction_x = -direction_x

    return direction_x, direction_y

# Check if the ball hits the paddle -- Returns 1 if doesn't and 1 if does
def checkHit(ball, paddle_right, paddle_left, direction_x):
    # Check if the ball in between paddle limits
    if direction_x == 1 and paddle_right.left == ball.right and paddle_right.top <= ball.top and paddle_right.bottom >= ball.bottom:
        return -1
    elif direction_x == -1 and paddle_left.right == ball.left and paddle_left.top <= ball.top and paddle_left.bottom >= ball.bottom:
        return -1
    else:
        return 1

# Makes the paddle follows the ball
def computerMove(ball, direction_x, paddle):
    # If the ball is coming, track its movement after middle
    if direction_x == -1 and ball.centerx <= WINDOW_WIDTH / 2:
        if paddle.centery < ball.centery:
            paddle.y += 1
        elif paddle.centery > ball.centery:
            paddle.y -= 1

    return paddle

# 1 point for hitting the ball, 5 points for beating the computer and resets to 0 is loses
def checkPointScored(paddle_right, ball, score, direction_x):
    if ball.right == WINDOW_WIDTH - LINE_THICKNESS: # Resets to 0 if loses
        score = 0
    elif direction_x == 1 and paddle_right.left == ball.right and paddle_right.top <= ball.top and paddle_right.bottom >= ball.bottom:
        score += 1
    elif ball.left == LINE_THICKNESS:
        score += 5

    return score

# Displays the score on the board
def displayScore(score):
    text = FONT.render('Score = %s' %(score), True, WHITE)
    display = text.get_rect()
    display.topleft = (WINDOW_WIDTH - 150, 25)
    DISPLAY_SURF.blit(text, display)

def main():
    pygame.init()
    global DISPLAY_SURF
    # Font information
    global FONT, FONT_SIZE
    FONT_SIZE = 20
    FONT = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')

    # Initial positions - Ball in the center - Paddles in the middle
    ball_x = (WINDOW_WIDTH - LINE_THICKNESS) / 2
    ball_y = (WINDOW_HEIGHT - LINE_THICKNESS) / 2
    player_left_position = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    player_right_position = (WINDOW_HEIGHT - PADDLE_SIZE) / 2
    score = 0

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

    pygame.mouse.set_visible(0) # Makes cursor invisible
    # Game main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                paddle_right.y = mouse_y

        drawArena()
        drawPaddle(paddle_left)
        drawPaddle(paddle_right)
        drawBall(ball)

        ball = moveBall(ball, ball_direction_x, ball_direction_y)
        ball_direction_x, ball_direction_y = checkEdgeCollision(ball, ball_direction_x, ball_direction_y)
        score = checkPointScored(paddle_right, ball, score, ball_direction_x)
        ball_direction_x = ball_direction_x * checkHit(ball, paddle_right, paddle_left, ball_direction_x)
        paddle_left = computerMove(ball, ball_direction_x, paddle_left)

        displayScore(score)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()
