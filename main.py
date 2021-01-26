import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load("Imp8bit.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("X-Wing Destroyer")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('Starjedi.ttf', 24)

textX = 10
textY = 5

# Game Over text
over_font = pygame.font.Font('Starjedi.ttf', 48)

textX = 10
textY = 5


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (250, 250))

# Game speed
playerSpeed = 0.5
enemySpeed = 0.8

# Player
playerImg = pygame.image.load('player.png')
playerX = 375
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    # Generate random position
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemySpeed)
    enemyY_change.append(40)

# Laser
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 500
laserX_change = 0
laserY_change = 5
laser_state = "ready"


def player(x, y):
    # Drop on the screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # Drop on the screen
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance < 27:
        return True
    else:
        return False


# Game main loop
running = True
while running:

    # RGB background
    screen.fill((0, 0, 120))
    # Background image
    screen.blit(background, (0, 0))

    # Checking if quit or any other button was pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If Keystroke is pressed check whether is right of left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    # Laser sound
                    laser_sound = mixer.Sound("laser.wav")
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Increase/decrease player position
    playerX += playerX_change
    # Adding boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Increase/decrease enemy position
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Adding boundaries
        if enemyX[i] <= 0:
            enemyX_change[i] = enemySpeed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemySpeed
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            # Laser sound
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Call enemy function
        enemy(enemyX[i], enemyY[i], i)

    # Laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"
    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    # Call player function
    player(playerX, playerY)

    # SHowe score
    show_score(textX, textY)

    # Update display
    pygame.display.update()
