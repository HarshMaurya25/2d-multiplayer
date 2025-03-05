import pygame
import json

surround = [(-1 , 0) , (-1 , 1) , (1, 0 ) , (1, -1) , (0,-1) , (0 , 1) ,(1 , 1) , (-1  , -1) , (0,0)]
class TileSheet:
    def __init__(self,gamw , tilesize = 30):
        self.game = gamw
        self.tilesize = tilesize
        self.tile_map= {}

    def render(self ):
        for tile in self.tile_map:
            tiles = self.tile_map[tile]
            rect = pygame.Rect(tiles['pos'][0] * self.tilesize, tiles['pos'][1] * self.tilesize, self.tilesize , self.tilesize)
            pygame.draw.rect(self.game.screen , (0,0,0) , rect)
    
    def playeraround(self , pos , size):
        tilearound = []
        loc = (int((pos[0] + size[0]) // self.tilesize) , int((pos[1] + size[1]) // self.tilesize))
        for position in surround:
            check = str(loc[0] + position[0]) + ';' + str(loc[1] + position[1])
            if check in self.tile_map:
                tilearound.append(self.tile_map[check])
        
        return tilearound

    def physcicsaround(self , pos , size):

        rect = []
        for tile in self.playeraround(pos  , size):
            rect.append(pygame.Rect((tile['pos'][0]) * self.tilesize, tile['pos'][1] * self.tilesize , self.tilesize , self.tilesize))


        return rect

    def Bulletaround(self , pos ):
        tilearound = []
        loc = (int((pos[0]) // self.tilesize) , int((pos[1]) // self.tilesize))
        for position in surround:
            check = str(loc[0] + position[0]) + ';' + str(loc[1] + position[1])
            if check in self.tile_map:
                tilearound.append(self.tile_map[check])
        
        return tilearound
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tile_map = map_data['tilemap']
        self.offgrid_tiles = map_data['offgrid']
    def Bullet_physcicsaround(self , pos):

        rect = []
        for tile in self.Bulletaround(pos ):
            rect.append(pygame.Rect((tile['pos'][0]) * self.tilesize, tile['pos'][1] * self.tilesize , self.tilesize , self.tilesize))


        return rect

"""
        for tile in range(0, 100):
            self.tile_map[str(tile) + ';' + "20"] = {
                'colour' : (0,0,0), 
                'pos' : (tile , 20)
            }
        for tile in range(0, 10):
            self.tile_map[str(tile + 23)  + ';' + "13"] = {
                'colour' : (0,0,0), 
                'pos' : (tile + 23 , 13)
            }
        for tile in range(0, 10):
            self.tile_map[str(tile + 34)  + ';' + "17"] = {
                'colour' : (0,0,0), 
                'pos' : (tile + 34 , 17)
            }
        for tile in range(0, 3):
            self.tile_map[str(tile + 15)  + ';' + "17"] = {
                'colour' : (0,0,0), 
                'pos' : (tile + 15 , 17)
            }
        for tile in range(0, 4):
            self.tile_map['10'+ ';' + str(tile + 17) ] = {
                'colour' : (0,0,0), 
                'pos' : (10, tile+ 17)
            }
        for tile in range(0, 7):
            self.tile_map['18'+ ';' + str(tile + 14) ] = {
                'colour' : (0,0,0), 
                'pos' : (18 , tile+ 14)
            }

            """