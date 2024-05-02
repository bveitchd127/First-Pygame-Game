import pygame
import random
from settings import *

def xpToNextLevel(level):
    return round(1/4 * level**2 + 10)


class Player:
    def __init__(self, x, y, color):

        playerScale = 3
        
        originalImage = pygame.image.load("player_spritesheet.png")
        originalImage = pygame.transform.scale_by(originalImage, playerScale)
        self.image = pygame.Surface( (playerScale*16, playerScale*16), pygame.SRCALPHA )

        self.image.blit(originalImage, (0,0), pygame.Rect(0,0, playerScale*16, playerScale*16))

        self.rect = pygame.Rect( (x, y), self.image.get_size() )

        self.vel = pygame.math.Vector2()


        self.level = 1
        self.xp = 0

        self.damage = 1 # upgradeable
        self.piercing = 1  # upgradeable

        self.health = 10
        self.healthRegen = 0  # upgradeable
        self.maxHealth = 10 # upgradeable

        self.stamina = 10
        self.staminaRegen = 1  # upgradeable
        self.maxStamina = 10 # upgradeable
        self.winded = False

        self.speed = 5
        self.baseSpeed = 5  # upgradeable
        self.invincibleCooldown = 0
    
    def takeDamage(self, damageAmount):
        if self.invincibleCooldown <= 0:
            self.invincibleCooldown = 1 # timer in seconds
            self.health -= damageAmount

    def levelUp(self):
        self.level += 1
        self.xp -= xpToNextLevel(self.level)

        """
        randomNum = 0 - 6
        0: damage           0.5
        1: piercing         1
        2: healthRegen      0.1
        3: maxHealth        1
        4: staminaRegen     0.1
        5: maxStamina       1
        6: baseSpeed        0.5
        """
        numToStat = {
            0: "damage",
            1: "piercing",
            2: "healthRegen",
            3: "maxHealth",
            4: "staminaRegen",
            5: "maxStamina",
            6: "baseSpeed"
        }
        randomStatNum = random.randint(0,6)
        print(numToStat[randomStatNum])
        if randomStatNum == 0:
            self.damage += 0.1
        elif randomStatNum == 1:
            self.piercing += 1
        elif randomStatNum == 2:
            self.healthRegen += 0.1
        elif randomStatNum == 3:
            self.maxHealth += 1
        elif randomStatNum == 4:
            self.staminaRegen += 0.1
        elif randomStatNum == 5:
            self.maxStamina += 1
        elif randomStatNum == 6:
            self.baseSpeed += 0.5
        else:
            print("Error: No matching perk to level up...")

        self.health = self.maxHealth
        self.stamina = self.maxStamina

    def update(self):

        if self.xp >= xpToNextLevel(self.level + 1):
            self.levelUp()



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



        if keys[pygame.K_LSHIFT] and self.stamina > 0 and not self.winded:
            self.stamina -= 2/FRAME_RATE
            self.speed = self.baseSpeed * 1.5
        elif self.stamina <= 0:
            self.winded = True
            self.stamina = self.stamina + self.staminaRegen/FRAME_RATE
            self.speed = self.baseSpeed
        elif self.stamina == self.maxStamina:
            self.winded = False
        else:
            self.stamina = min(self.stamina + self.staminaRegen/FRAME_RATE, self.maxStamina)
            self.speed = self.baseSpeed

        if self.vel.magnitude() > 0:
            self.vel.scale_to_length(self.speed)


        self.health = min(self.health + self.healthRegen/FRAME_RATE, self.maxHealth)


        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.rect.top < SCREEN_BORDER_WIDTH:
            self.rect.top = SCREEN_BORDER_WIDTH
        if self.rect.left < SCREEN_BORDER_WIDTH:
            self.rect.left = SCREEN_BORDER_WIDTH
        if self.rect.right > SCREEN_WIDTH - SCREEN_BORDER_WIDTH:
            self.rect.right = SCREEN_WIDTH - SCREEN_BORDER_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT - SCREEN_BORDER_WIDTH:
            self.rect.bottom = SCREEN_HEIGHT - SCREEN_BORDER_WIDTH
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)