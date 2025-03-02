import pygame
from client import Client
from protocols import Protocol
from player import Player
from tilemap import TileSheet
import time
from bullet import Bullet

class Game:
    def __init__(self):

        self.font = None
        self.text = ''
        self.done = False
        self.logged_in = False

        self.color_inactive = (0, 0, 100)
        self.color_active = (0, 0, 250)
        self.color = self.color_inactive

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 32)
        self.input_rect = pygame.Rect(100, 100, 400, 60)

        self.player = Player(self, (100, 100), (30, 30), (255, 0, 0))
        self.opponent = Player(self, (100, 100), (30, 30), (0, 255, 0))
        self.data = {
            'pos': self.player.pos
        }
        self.movement = [False, False]
        self.tiles = TileSheet(self, 20)
        self.bullet_g = pygame.sprite.Group()
        self.left = False

    def run(self):
        while True:
            self.clock.tick(60)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                else:
                    self.handle_event(event)

            self.draw()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.movement[0] = True
                self.left = False
            if event.key == pygame.K_a:
                self.movement[1] = True
                self.left = True

            if event.key == pygame.K_SPACE:
                self.player.perform_jump()
            if event.key == pygame.K_RETURN:
                Bullet(self.player.rects().center, (10,5), self.bullet_g)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.movement[0] = False
            if event.key == pygame.K_a:
                self.movement[1] = False

    def draw(self):
        self.screen.fill((200, 200, 200))
        if False:
            pass
        else:
            self.run_game()

    def draw_waiting(self):
        text = 'waiting for players'
        text_surface = self.font.render(text, 1, (0, 0, 0))
        self.screen.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() / 2, self.screen.get_height() / 2))

    def run_game(self):
        self.player.update((self.movement[0] - self.movement[1], 0), self.tiles)
        self.bullet_g.update(self.left)
        self.bullet_g.draw(self.screen)
        self.player.Render()
        self.opponent.Render()
        self.tiles.render()

if __name__ == "__main__":
    game = Game()
    game.run()