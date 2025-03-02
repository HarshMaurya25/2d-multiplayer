import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 0)) 
        self.rect = self.image.get_rect(center=pos)
        self.speed = 15

    def update(self, left):
        if left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
