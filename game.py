import pygame
from util.client import Client
from util.protocols import Protocol
from util.player import Player
from util.tilemap import TileSheet
import time
from util.bullet import Bullet, oppBullet
import json

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
        self.bullet_g = pygame.sprite.Group()
        self.opponent_bullet = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 32)
        self.input_rect = pygame.Rect(100, 100, 400, 60)

        self.player = Player(self, (100, 100), (30, 30), (255, 0, 0), self.player_group)
        self.opponent = Player(self, (100, 100), (30, 30), (0, 255, 0) , self.player_group)

        self.movement = [False, False]
        self.tiles = TileSheet(self, 30)
        self.shoot = 0
        self.loser = False

        self.data = {
            'pos': self.player.pos
        }
        self.bullet_pos = []
        self.close = False

        self.tiles.load('util/map.json')

    def run(self):
        while not self.client.closed:
            self.clock.tick(60)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.closed = True
                else:
                    self.handle_event(event)

            self.draw()
        
    def End(self):
        run = True
        while run:
            self.screen.fill((200, 200, 200))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.client.client.close()

                if event.type == pygame.KEYDOWN:
                    run = False
            if self.client.winner:
                text = f"{self.client.winner} win the game"
            else:
                text = f"opponent left!!!"
            self.client.winner = None
            text_surface = self.font.render(text, 1, (0, 0, 0))
            self.screen.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() / 2, self.screen.get_height() / 2))
            pygame.display.update()
            
        self.client.start()
        self.done = False
        self.logged_in = False
        self.client.closed = False
        self.run()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.color = self.color_active
            else:
                self.color = self.color_inactive

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
            if event.type == pygame.KEYUP and self.color == self.color_inactive:
                return
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
                    angle = self.player.angle()
                    Bullet(self.player.rects().center, (10, 10), angle, self.bullet_g)
                    self.bullet_pos.append(angle)

    def draw(self):
        self.screen.fill((200, 200, 200))

        if not self.logged_in and not self.client.started:
            self.loser = False
            self.draw_login()

        elif not self.client.started:
            self.draw_waiting()
        elif not self.loser or self.client.winner == True:
            pygame.mouse.set_visible(False)
            self.run_game()
            self.player.aim()
    
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

    def handle_end(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.closed = True
                return

        text = f"{self.client.winner} win the game" if self.client.winner else "opponent left!!!"
        text_surface = self.font.render(text, 1, (0, 0, 0))
        self.screen.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() / 2, self.screen.get_height() / 2))
        pygame.display.update()

    def run_game(self):
        if self.client.started:
            self.data = {
                'pos': (self.player.pos[0], self.player.pos[1]),
                'center': self.player.centers,
                'bullet': self.bullet_pos
            }
            self.client.send(Protocol.Request.Move, self.data)

        pos = self.client.opponent_moved.get('pos', (0, 0))
        center = self.client.opponent_moved.get('center', (0, 0))
        list = self.client.opponent_moved.get('bullet', [])

        try:
            Bullet(center, (10, 10), list[0], self.opponent_bullet)
        except:
            pass
        self.player.update((self.movement[0] - self.movement[1], 0), self.tiles, self.opponent_bullet)
        self.player.Render()
        self.player.draw_health_bar()

        self.opponent.Renderopp(pos, self.bullet_g)

        self.tiles.render()
        self.bullet_g.update(self.tiles)
        self.bullet_g.draw(self.screen)
        self.opponent_bullet.update(self.tiles)
        self.opponent_bullet.draw(self.screen)
        self.bullet_pos = []

        if self.player.health <= 0:
            self.client.send(Protocol.Responce.Winner , None)
            print('opponent winner')
            self.client.close_()


if __name__ == "__main__":
    game = Game(Client())
    game.run()