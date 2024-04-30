import pygame
from settings import *

class Player:
    def __init__(self, x, y, color):

        playerScale = 3
        
        originalImage = pygame.image.load("player_spritesheet.png")
        originalImage = pygame.transform.scale_by(originalImage, playerScale)
        self.image = pygame.Surface( (playerScale*16, playerScale*16), pygame.SRCALPHA )

        self.image.blit(originalImage, (0,0), pygame.Rect(0,0, playerScale*16, playerScale*16))

        self.rect = pygame.Rect( (x, y), self.image.get_size() )

        self.vel = pygame.math.Vector2()

        self.health = 10
        self.speed = 5
        self.invincibleCooldown = 0
    
    def damage(self, damageAmount):
        if self.invincibleCooldown <= 0:
            self.invincibleCooldown = 1 # timer in seconds
            self.health -= damageAmount

    def update(self):
        if self.invincibleCooldown > 0:
            self.invincibleCooldown -= 1/FRAME_RATE

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]):
            self.vel.y = -1
        elif (keys[pygame.K_s]):
            self.vel.y = 1
        else:
            self.vel.y = 0
        
        if (keys[pygame.K_a]):
            self.vel.x = -1
        elif (keys[pygame.K_d]):
            self.vel.x = 1
        else:
            self.vel.x = 0

        if (keys[pygame.K_LSHIFT]):
            self.speed = 7
        else:
            self.speed = 4

        if self.vel.magnitude() > 0:
            self.vel.scale_to_length(self.speed)

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)