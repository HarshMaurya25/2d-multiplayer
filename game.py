import pygame
from client import Client
from protocols import Protocol
from player import Player
from tilemap import TileSheet
import time

class Game:
    def __init__(self , client):
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

        self.player = Player(self, (100 , 100 ) , (30 , 30) , (255 , 0 ,0))
        self.opponent = Player(self, (100 , 100 ) , (30 , 30) , (0 , 255  ,0))
        self.data = {
            'pos' : self.player.pos
        }
        self.movement = [False, False]
        self.tiles = TileSheet(self, 20)

    def run(self):
        time.sleep(2)
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
        
        if self.client.started:
            self.data = {
                        'pos' : self.player.pos
                    }
            
            self.client.send(Protocol.Request.Move, self.data)
            if 'pos' in self.client.opponent_moved:
                self.opponent.pos = tuple(self.client.opponent_moved['pos'])
        self.player.update((self.movement[0] - self.movement[1], 0), self.tiles)
        self.player.Render()
        self.opponent.Render()
        self.tiles.render()

if __name__ == "__main__":
    game = Game(Client())
    game.run()