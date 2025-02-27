import pygame

class Player:
    def __init__(self, game, pos, size, colour):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.colour = colour
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.jumps = 0

    def rects(self ):
        return pygame.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])

    def update(self, movement, tilemap):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
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

    def Render(self ):
        pygame.draw.rect(self.game.screen, self.colour, self.rects())

    def perform_jump(self):
        if self.jumps < 2:
            self.velocity[1] -= 5
            self.jumps += 1

