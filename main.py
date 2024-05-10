import pygame

#     file          class
from player import Player
from enemy import Enemy
from boss import Boss
from projectile import Projectile
from settings import *
import random

username = input("What's your name?: ")

# pygame setup
pygame.init()
pygame.font.init()

button_font = pygame.font.SysFont(None, 72)
ui_font = pygame.font.SysFont(None, 32)
stat_font = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# "start", "play", "lost"
currentScene = "start"

waveNumber = 20

def waveToEnemyCount(waveNumber):
    return round(1/13 * waveNumber**2 + 10)

p1 = Player(200, 100, pygame.Color("#272910"))

# This spawns 5 enemies for our level
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

startButton = pygame.Rect(0,0,400,150)
startButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
startText = button_font.render("Start", True, "white")
startTextRect = startText.get_rect(center = startButton.center)

retryButton = pygame.Rect(0,0,400,150)
retryButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
retryText = button_font.render("Retry", True, "white")
retryTextRect = retryText.get_rect(center = retryButton.center)

exitButton  = pygame.Rect(0,0,400,150)
exitButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 250)
exitText = button_font.render("Exit", True, "white")
exitTextRect = exitText.get_rect(center = exitButton.center)


background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))

# random.randint(0,4) -> 0,1,2,3,4
# random.randint(0,4)*32 -> 0,32,64,96,128
# topleft corners of tiles (0,160) , (32, 160) , (64,160) , (96,160) , (128,160)
# tiles are 32x32
tileOffsetX = 352
tileOffsetY = 608
floorTileSet = pygame.image.load("TilesetFloor.png")
floorTileSet = pygame.transform.scale_by(floorTileSet, 2)
for r in range(0, SCREEN_HEIGHT, 32):
    for c in range(0, SCREEN_WIDTH, 32):
        randomTileX = max(0,random.randint(-8,4))*32
        background.blit(floorTileSet, (c, r), pygame.Rect(tileOffsetX + randomTileX, tileOffsetY, 32,32))



def spawnEnemies(numberOfEnemies):
    
    while (len(enemies) < numberOfEnemies):
        randX = random.randint(-1000, SCREEN_WIDTH + 1000)
        randY = random.randint(-1000, SCREEN_HEIGHT + 1000)

        # calculate the distance between random point and player
        distanceToPlayer = (pygame.math.Vector2(p1.rect.center) - (randX, randY)).magnitude()

        # If enemy spawn is too close, dont spawn there
        if distanceToPlayer < SAFE_ENEMY_RADIUS:
            continue

        if 0 < randX < SCREEN_WIDTH and 0 < randY < SCREEN_HEIGHT:
            continue
        
        bossChance = random.randint(0,100)
        if bossChance < waveNumber:
            enemies.add( Boss(randX, randY) )
        else:
            enemies.add( Enemy(randX, randY) )

def drawUi(screen):
    # Shows "Wave #: 3 at top left"
    waveNumberText = ui_font.render("Wave #: " + str(waveNumber), True, "white")
    screen.blit(waveNumberText, (20,20))

    # Shows "Enemy count: 57" below wave number
    enemyCountText = ui_font.render("Enemy count: " + str(len(enemies)), True, "white")
    screen.blit(enemyCountText, (20, 50))

    playerLevelText = ui_font.render("Player level: " + str(p1.level), True, "white")
    screen.blit(playerLevelText, (20, 110))

    playerXpText = ui_font.render("Player xp: " + str(p1.xp), True, "white")
    screen.blit(playerXpText, (20, 140))


    for i, statName in enumerate(p1.statLevels):
        statLevel = p1.statLevels[statName]

        statSurface = stat_font.render(statName + ": " + str(statLevel), True, "white")
        screen.blit(statSurface, (20, 200 + 24*i))

        



    # Player health bar
    playerHealthBarWidth = 400 * (p1.health / p1.maxHealth)
    pygame.draw.rect(screen, (58,54,66),  pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 0, 15)
    pygame.draw.rect(screen, (206,72,81),   pygame.Rect(20, SCREEN_HEIGHT - (40+20) , playerHealthBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, (21,27,27), pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 3, 15)

    staminaColor = "green"
    if p1.winded:
        staminaColor = (255, 200, 0)

    # Player stamina bar
    playerStaminaBarWidth = 400 * (p1.stamina / p1.maxStamina)
    pygame.draw.rect(screen, (58,54,66),  pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 0, 15)
    pygame.draw.rect(screen, staminaColor, pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) , playerStaminaBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, (21,27,27), pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 3, 15)

def gameUpdate():
    global waveNumber, currentScene
    # Part of Game Loop
    if len(enemies) == 0:
        waveNumber += 1
        spawnEnemies( waveToEnemyCount(waveNumber) )
    
    currentEnemies = len(enemies)

    p1.update()
    enemies.update(p1)
    projectiles.update()

    #   Checking collisions for enemies and projectiles
    for enemy in enemies:
        # ... check every projectile for collision
        for projectile in projectiles:
            if projectile.rect.colliderect( enemy.rect ):
                if not enemy in projectile.exemptEnemies:
                    enemy.damage( projectile.getDamage() )
                    projectile.exemptEnemies.add(enemy)
        
        # ... check player collision
        if p1.rect.colliderect( enemy.rect ):
            p1.takeDamage( enemy.getDamage() )

    enemiesEliminated = currentEnemies - len(enemies)

    for i in range(enemiesEliminated):
        # add random amount of xp to player
        xpAmount = max(random.randint(-2, 3), 0)
        p1.xp += xpAmount
    
    if p1.health <= 0:
        with open("leaderboard.txt", "a") as textFile:
            textFile.write(f"{username} {waveNumber}\n")
        currentScene = "lost"

def resetGame():
    global p1, waveNumber

    p1 = Player(200, 100, pygame.Color("#272910"))
    waveNumber = 0
    enemies.empty()
    projectiles.empty()

while running:

    # Check keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if currentScene == "play":
                if event.button == 1 and p1.speed < p1.baseSpeed*1.5:
                    # Spawn projectile
                    playerToMouse = pygame.math.Vector2( event.pos ) - p1.rect.center
                    if playerToMouse.magnitude() > 0:
                        playerToMouse.scale_to_length( 10 )
                    projectiles.add( Projectile(p1.rect.centerx, p1.rect.centery,  playerToMouse.x, playerToMouse.y, p1.damage, p1.piercing) )
            elif currentScene == "start":
                if event.button == 1 and startButton.collidepoint( pygame.mouse.get_pos() ):
                    currentScene = "play"
                elif event.button == 1 and exitButton.collidepoint( pygame.mouse.get_pos() ):
                    running = False
            elif currentScene == "lost":
                if event.button == 1 and retryButton.collidepoint( pygame.mouse.get_pos() ):
                    currentScene = "play"
                    resetGame()
                elif event.button == 1 and exitButton.collidepoint( pygame.mouse.get_pos() ):
                    running = False


    if currentScene == "play":
        gameUpdate()


    # Background Layer
    # screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0,0))

    # Entity Layer
    p1.draw(screen)
    for e in enemies:
        e.draw(screen)
    projectiles.draw(screen)

    # Draw User Interface
    if currentScene == "play":
        drawUi(screen)
    elif currentScene == "start":
        pygame.draw.rect(screen, "green", startButton, 0, 50) # button background
        screen.blit(startText, startTextRect)
        pygame.draw.rect(screen, "black", startButton, 5, 50) # button border

        pygame.draw.rect(screen, "green", exitButton,  0, 50)
        screen.blit(exitText, exitTextRect)
        pygame.draw.rect(screen, "black", exitButton,  5, 50)
    else:
        pygame.draw.rect(screen, "green", retryButton, 0, 50)
        screen.blit(retryText, retryTextRect)
        pygame.draw.rect(screen, "black", retryButton, 5, 50)

        pygame.draw.rect(screen, "green", exitButton,  0, 50)
        screen.blit(exitText, exitTextRect)
        pygame.draw.rect(screen, "black", exitButton,  5, 50)

    pygame.display.flip()
    clock.tick(FRAME_RATE)  # limits FPS to 60

pygame.quit()