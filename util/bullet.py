import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, size , angle, *groups):
        super().__init__(*groups)
        self.angle = angle
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 0)) 
        self.image = pygame.transform.rotate(self.image , self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 45
        self.initial = pos

    def update(self , tile):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(-self.angle))

        if math.dist(self.initial , self.rect.center) > 600:
            self.kill()

        for rect in tile.Bullet_physcicsaround(self.rect.center):
            if self.rect.colliderect(rect):
                self.kill()

class oppBullet(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 0)) 
        self.image = pygame.transform.rotate(self.image , self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 15
        self.initial = pos


