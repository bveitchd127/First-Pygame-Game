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
            print(len(projectiles))
            if event.button == 1 and p1.speed < 7:
                # Spawn projectile
                playerToMouse = pygame.math.Vector2( event.pos ) - p1.rect.center
                if playerToMouse.magnitude() > 0:
                    playerToMouse.scale_to_length( 10 )
                projectiles.add( Projectile(p1.rect.centerx, p1.rect.centery,  playerToMouse.x, playerToMouse.y) )

    # If there are no enemies in the enemies group
    # spawn enemies
    if len(enemies) == 0:
        waveNumber += 1
        spawnEnemies( waveToEnemyCount(waveNumber) )

    p1.update()
    enemies.update(p1)
    projectiles.update()

    # For every enemy...
    for enemy in enemies:
        # ... check every projectile for collision
        for projectile in projectiles:
            if projectile.rect.colliderect( enemy.rect ):
                enemy.damage( projectile.getDamage() )
        
        # ... check player collision
        if p1.rect.colliderect( enemy.rect ):
            p1.damage( enemy.getDamage() )

                
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

    playerHealthBarWidth = 400 * (p1.health / p1.maxHealth)
    pygame.draw.rect(screen, "gray",  pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 0, 15)
    pygame.draw.rect(screen, "red",   pygame.Rect(20, SCREEN_HEIGHT - (40+20) , playerHealthBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, "black", pygame.Rect(20, SCREEN_HEIGHT - (40+20) ,                  400, 40), 3, 15)

    playerStaminaBarWidth = 400 * (p1.stamina / p1.maxStamina)
    pygame.draw.rect(screen, "gray",  pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 0, 15)
    pygame.draw.rect(screen, "green", pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) , playerStaminaBarWidth, 40), 0, 15)
    pygame.draw.rect(screen, "black", pygame.Rect(SCREEN_WIDTH - 20 - 400, SCREEN_HEIGHT - (40+20) ,                   400, 40), 3, 15)
    
    
    pygame.display.flip()
    clock.tick(FRAME_RATE)  # limits FPS to 60

pygame.quit()