import pygame
from paddles import Paddle, Ball
import numpy as np
from random import randint
from sklearn.linear_model import LinearRegression

def normalize(X):
    m = max(X)
    l = min(X)
    for i in range(len(X)):
        X[i] = (X[i] - l) / (m - l)
    return X

data = np.zeros(2000)
X1 = np.zeros(2000)
X2 = np.zeros(2000)

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")


ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

paddleA = Paddle(WHITE, 10, 50, 1)
paddleA.rect.x = 10
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 50, 1)
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


    data[i] = int(paddleA.rect.y)
    X1[i] = int(ball.rect.x)
    X2[i] = int(ball.rect.y)
    i += 1
    if i == (200):
        carryOn = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(10)
    if keys[pygame.K_s]:
        paddleA.moveDown(10)

    if paddleA.rect.y < paddleB.rect.y:
        paddleB.moveUp(10)
    if paddleA.rect.y > paddleB.rect.y:
        paddleB.moveDown(10)

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
    clock.tick(25)
pygame.quit()

p = normalize(X1)
q = normalize(X2)
X = np.zeros((data.shape[0], 2))

for i in range(data.shape[0]):
    X[i][0] = p[i] 
    X[i][1] = q[i]

model = LinearRegression()
model = LinearRegression().fit(X , data)
r_sq = model.score(X, data)

print(model.intercept_)
print(model.coef_)

#np.savetxt('y.txt', data, delimiter=',')
#np.savetxt('x1.txt', X1, delimiter=',')
#np.savetxt('X2.txt', X2, delimiter=',')