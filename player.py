import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, colour , *groups):
        super().__init__(*groups)
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.colour = colour
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.jumps = 0
        self.image = pygame.image.load('aim.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.image_play = pygame.Surface(self.size)
        self.image_play.fill(colour) 
        self.centers = pos

        self.image = pygame.transform.scale(self.image, (25 ,25))
        self.health = 4

    def rects(self ):
        return pygame.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])

    def update(self, movement, tilemap , bullets):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.centers = self.rects().center
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rects()
        for rect in tilemap.physcicsaround(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rects()
        for rect in tilemap.physcicsaround(self.pos, self.size):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
    
        if self.collisions['down']:
            self.velocity[1] = 0
            self.jumps = 0
        
        for bullet in bullets:
            if self.rects().colliderect(bullet.rect):
                bullet.kill()
                self.health -= 1
        
    def Render(self ):
        self.game.screen.blit(self.image_play , (self.pos))



    def aim(self):
        mpos = pygame.mouse.get_pos()
        self.game.screen.blit(self.image, mpos)
    
    def angle(self):
        mpos = pygame.mouse.get_pos()
        x_diff, y_diff = mpos[0] - self.pos[0], mpos[1] - self.pos[1]
        angle = math.degrees(math.atan2(-y_diff, x_diff))
        return angle

    def perform_jump(self):
        if self.jumps < 2:
            self.velocity[1] -= 5
            self.jumps += 1

    def Renderopp(self , pos ,bullets):

        rect = self.rects()
        rect.x , rect.y = pos
        self.game.screen.blit(self.image_play , (rect.x , rect.y))

        for bullet in bullets:
            if rect.colliderect(bullet.rect):
                bullet.kill()
    
    def draw_health_bar(self):
        health_bar_width = 40
        health_bar_height = 5
        health_bar_x = self.pos[0] + (self.size[0] - health_bar_width) / 2
        health_bar_y = self.pos[1] - 10

        health_ratio = self.health / 4
        current_health_bar_width = health_bar_width * health_ratio

        pygame.draw.rect(self.game.screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        pygame.draw.rect(self.game.screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))