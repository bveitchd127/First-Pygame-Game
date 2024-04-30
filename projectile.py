import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velx, vely):
        super().__init__()

        # sword is 6x15

        # Make 20x20 surface
        self.image = pygame.Surface( (20,20), pygame.SRCALPHA )
        self.rect = pygame.Rect( (x, y), self.image.get_size() )

        self.velocity = pygame.math.Vector2( (velx, vely) )

        print( -pygame.math.Vector2((0,-1)).angle_to(self.velocity) )

        canvasRect = pygame.Rect((0,0), self.rect.size)
        projectileAssetSurface = pygame.transform.rotate( pygame.image.load("projectile.png") , 90 )
        projectileAssetRect = projectileAssetSurface.get_rect(center = canvasRect.center)

        self.image.blit(projectileAssetSurface, projectileAssetRect)

        # self.image.fill("gray")
        

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
