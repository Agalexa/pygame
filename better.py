import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3
posX = 50

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(posX)
    enemyY.append(100)
    enemyX_change.append(4)
    enemyY_change.append(40)
    posX += 80
# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and Wave Count
wave_value = 0
score_value = 0
score_track = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)


danger_font = pygame.font.Font('freesansbold.ttf', 42)


tenX = 300
tenY = 10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_warning():
    dangy = danger_font.render("WATCH OUT!!! THE BOSS IS ALMOST HERE! ", True, (255, 80, 160))
    screen.blit(dangy,(30,50))

def show_danger():
    dangy = danger_font.render("Danger! Boss incoming in  " + str(3 - wave_value) + " waves!", True, (255, 80, 160))
    screen.blit(dangy,(30,50))

def show_score():
    score = score_font.render("Score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))

#function to display wave level

def show_wave(): 
    wavey = score_font.render(str(wave_value) + " Waves", True, (255, 255, 255))
    screen.blit(wavey, (660,10))


####

#test function to help me determine programs position

def test_this(y):
    testy = score_font.render("test : " + str(y), True, (255, 255, 255))
    screen.blit(testy, (200,300))

def announce_score():
    ten_score = score_font.render(str(score_value) + " points!", True, (255,255,255))
    screen.blit(ten_score,(300,10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

hopefully = 2
    
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440 and enemyY[i] < 900:
            for j in range(num_of_enemies):
                enemyY[j] = 899
            game_over_text()
            break
        
        #made it so enemies move synchronously, and fixed a bug causing them to move too fast due weired interaction with off screen assets 
        #ENEMY MOVEMENT MECHANIC
        # SET UP CONDITION TO RESPAWN IN WAVES AFTER ALL 3 ARE DESTROYED, WILL ALSO INCREASE ENEMY SPEED EACH WAVE 
        if (((score_track % 3) == 0) and (score_track != 0)):
            hopefully += 2
            wave_value += 1
            numbX = 50
            for i in range(num_of_enemies):
                enemyX[i] = numbX
                enemyY[i] = 50
                enemyX[i] += enemyX_change[i]
                enemyX_change[i] = hopefully
                numbX += 80
            score_track = score_track - score_track
        
        else:
            enemyX[i] += enemyX_change[i]
            
####                #######         WORK IN PROGRESS

        if (enemyX[i] <= 0 and enemyY[i] <440):
            for i in range(num_of_enemies):
                enemyX_change[i] = hopefully
                enemyY[i] += enemyY_change[i]
                
        elif (enemyX[i] >= 736 and enemyY[i] <440) :
            for i in range(num_of_enemies):    
                enemyX_change[i] = -hopefully
                enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            score_track += 1
            enemyX[i] = 150
            enemyY[i] = 950
            #enemyX[i] = random.randint(250,300) #// open these variables
            #enemyY[i] = 50 #// to enable respawn
        #made it so enemies dissapear and dont respawn until the wave is over, will keep track of waves to introduce boss fights

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if (score_value == 6 or score_value == 12 or score_value == 18):
        announce_score()

    if (((score_value % 3) == 0) and (score_value != 0) and (score_value != 9)):
        show_danger()

    if score_value == 8:
        show_warning()



    
    show_wave()
    player(playerX, playerY)
    show_score()
    pygame.display.update()