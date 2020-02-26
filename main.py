import pygame
from paddles import Paddle, Ball
import numpy as np
from random import randint
    
    ################################
    #### use only PgUp and PgDn ####
    ################################


def normalizeX(X):
    m = 700
    l = 0
    if len(X) > 1:
        for i in range(len(X)):
            X[i] = (X[i] - l) / (m - l)
        return X
    
    return (X[0] - l) / (m - l)


def normalizeY(X):
    m = 500
    l = 0
    if len(X) > 1:
        for i in range(len(X)):
            X[i] = (X[i] - l) / (m - l)
        return X

    return (X[0] - l) / (m - l)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")


ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

paddleA = Paddle(WHITE, 10, 150)
paddleA.rect.x = 10
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 150)
paddleB.rect.x = 680
paddleB.rect.y = 200

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

clock = pygame.time.Clock()
carryOn = True

scoreA = 0
scoreB = 0

i = 0
while carryOn:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    x = ball.rect.x
    y = ball.rect.y
    
    # input your weights
    z = -16.052241547303225 + (8.8946012) * (normalizeX([x])) + (462.67319362) * (normalizeY([y]))
    #f = -16.052241547303225 + (8.8946012) * (normalizeX([x])) + (462.67319362) * (normalizeY([y])) 
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        paddleA.moveUp(10)
    if keys[pygame.K_DOWN]:
        paddleA.moveDown(10)
    q = z - paddleB.rect.y

    if q < 0:
        q *= -1
    if q > 4:
        if z > paddleB.rect.y:
            paddleB.moveDown(10)
        if z < paddleB.rect.y:
            paddleB.moveUp(10)

        #if f > paddleA.rect.y:
         #   paddleA.moveDown(10)
        #if f < paddleA.rect.y:
         #   paddleA.moveUp(10)

    if ball.rect.x >= 690:
        scoreA += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        ball.velocity = [randint(4, 8), randint(-8, 8)]

    if ball.rect.x <= 0:
        scoreB += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        velocity = [randint(4, 8), randint(-8, 8)]

    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    all_sprites_list.update()

    screen.fill(BLACK)

    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420, 10))

    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(100)

pygame.quit()



