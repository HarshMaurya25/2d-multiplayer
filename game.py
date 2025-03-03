import pygame
from client import Client
from protocols import Protocol
from player import Player
from tilemap import TileSheet
import time
from bullet import Bullet, oppBullet

class Game:
    def __init__(self, client):
        self.client = client
        client.start()

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
        self.movement = [False, False]
        self.tiles = TileSheet(self, 20)
        self.shoot = 0
        self.bullet_g = pygame.sprite.Group()
        self.opponent_bullet = pygame.sprite.Group()
        self.data = {
            'pos': self.player.pos,
            'bullet': []
        }

    def run(self):
        while not self.client.closed:
            self.clock.tick(60)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                    return
                else:
                    self.handle_event(event)

            self.draw()

    def handle_event(self, event):
        if self.client.receive_ and self.client.info:
            print(self.client.info)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.color = self.color_active
            else:
                self.color = self.color_inactive

        if event.type == pygame.KEYUP and self.color == self.color_inactive:
            return
        if not self.client.started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    if not self.logged_in:
                        self.client.send(Protocol.Request.Nickname, self.text)
                        self.client.nickname = self.text
                        self.logged_in = True
                        self.text = ''
                else:
                    self.text += event.unicode
        else:
            if self.shoot > 0:
                self.shoot -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement[0] = True
                if event.key == pygame.K_a:
                    self.movement[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.perform_jump()

            if event.type == pygame.KEYUP:
                if self.client.started:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.shoot == 0 and self.client.started:
                if event.button == 1:
                    self.shoot = 2
                    Bullet(self.player.rects().center, (10, 10), self.player.angle(), self.bullet_g)

    def draw(self):
        self.screen.fill((200, 200, 200))

        if not self.logged_in and not self.client.started:
            self.draw_login()

        elif not self.client.started:
            self.draw_waiting()
        else:
            self.run_game()

    def draw_login(self):
        prompt = 'Enter the nickname'
        prompt_surface = self.font.render(prompt, 1, (0, 0, 0))
        self.screen.blit(prompt_surface, (100, 50))
        self.draw_input()

    def draw_input(self):
        pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
        txt_surface = self.font.render(self.text, 1, self.color)
        self.screen.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(500, txt_surface.get_width() + 10)

    def draw_waiting(self):
        text = 'waiting for players'
        text_surface = self.font.render(text, 1, (0, 0, 0))
        self.screen.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() / 2, self.screen.get_height() / 2))

    def run_game(self):
        length = []
        pos = (0, 0)
        if self.client.started:
            for bullet in self.bullet_g:
                length.append([bullet.rect.x, bullet.rect.y])
            self.data = {
                'pos': self.player.pos,
                'bullet': length
            }
            if 'bullet' in self.client.opponent_moved:
                self.opponent_bullet.empty()
                for bullet_pos in self.client.opponent_moved['bullet']:
                    oppBullet((bullet_pos[0], bullet_pos[1]), (10, 10), self.opponent_bullet)
            self.client.send(Protocol.Request.Move, self.data)

        pos = self.client.opponent_moved
        print(type(pos))

        self.player.update((self.movement[0] - self.movement[1], 0), self.tiles)
        self.player.Render()
        print(pos)
        self.opponent.Renderopp(pos)
        self.tiles.render()
        self.bullet_g.update(self.tiles)
        self.bullet_g.draw(self.screen)
        self.opponent_bullet.update(self.tiles)
        self.opponent_bullet.draw(self.screen)

if __name__ == "__main__":
    game = Game(Client())
    game.run()