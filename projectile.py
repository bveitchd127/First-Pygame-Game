import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velx, vely):
        super().__init__()

        self.image = pygame.Surface( (10,10) )
        self.rect = pygame.Rect( (x, y), self.image.get_size() )

        self.image.fill("gray")
        self.velocity = pygame.math.Vector2( (velx, vely) )

        self.durability = 3
        self.damage = 1
    
    def getDamage(self):
        self.durability -= 1
        if self.durability <= 0:
            self.kill()
        return self.damage
    
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
