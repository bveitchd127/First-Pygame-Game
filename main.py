import pygame

#     file          class
from player import Player
from enemy import Enemy
from projectile import Projectile
from settings import *
import random

# pygame setup
pygame.init()
pygame.font.init()

ui_font = pygame.font.SysFont(None, 32)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

waveNumber = 0

def waveToEnemyCount(waveNumber):
    return round(1/13 * waveNumber**2 + 10)

p1 = Player(200, 100, pygame.Color("#272910"))

# This spawns 5 enemies for our level
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

def spawnEnemies(numberOfEnemies):
    while (len(enemies) < numberOfEnemies):
        randX = random.randint(0, SCREEN_WIDTH)
        randY = random.randint(0, SCREEN_HEIGHT)

        # calculate the distance between random point and player
        distanceToPlayer = (pygame.math.Vector2(p1.rect.center) - (randX, randY)).magnitude()

        # If enemy spawn is too close, dont spawn there
        if distanceToPlayer < SAFE_ENEMY_RADIUS:
            continue

        enemies.add( Enemy(randX, randY) )

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and p1.speed < p1.baseSpeed*1.5:
                # Spawn projectile
                playerToMouse = pygame.math.Vector2( event.pos ) - p1.rect.center
                if playerToMouse.magnitude() > 0:
                    playerToMouse.scale_to_length( 10 )
                projectiles.add( Projectile(p1.rect.centerx, p1.rect.centery,  playerToMouse.x, playerToMouse.y, p1.damage, p1.piercing) )

    # If there are no enemies in the enemies group
    # spawn enemies
    if len(enemies) == 0:
        waveNumber += 1
        spawnEnemies( waveToEnemyCount(waveNumber) )
    
    currentEnemies = len(enemies)

    p1.update()
    enemies.update(p1)
    projectiles.update()

    # For every enemy...
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
                
    # Background Layer
    screen.fill(BACKGROUND_COLOR)

    # Entity Layer
    p1.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)

    # User Interface Layer
    # playerHealthText = ui_font.render("Health: " + str(p1.health), True, "white")
    # screen.blit(playerHealthText, (20,20))

    waveNumberText = ui_font.render("Wave #: " + str(waveNumber), True, "white")
    screen.blit(waveNumberText, (20,20))

    enemyCountText = ui_font.render("Enemy count: " + str(len(enemies)), True, "white")
    screen.blit(enemyCountText, (20, 50))

    playerLevelText = ui_font.render("Player level: " + str(p1.level), True, "white")
    screen.blit(playerLevelText, (20, 110))

    playerXpText = ui_font.render("Player xp: " + str(p1.xp), True, "white")
    screen.blit(playerXpText, (20, 140))


    playerHealthBarWidth = 400 * (p1.health / p1.maxHealth)
    pygame.draw.rect(screen, "gray",  pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 0, 15)
    pygame.draw.rect(screen, "red",   pygame.Rect(20, SCREEN_HEIGHT - (40+20) , playerHealthBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, "black", pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 3, 15)

    staminaColor = "green"
    if p1.winded:
        staminaColor = (255, 200, 0)

    playerStaminaBarWidth = 400 * (p1.stamina / p1.maxStamina)
    pygame.draw.rect(screen, "gray",  pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 0, 15)
    pygame.draw.rect(screen, staminaColor, pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) , playerStaminaBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, "black", pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 3, 15)
    
    
    pygame.display.flip()
    clock.tick(FRAME_RATE)  # limits FPS to 60

pygame.quit()