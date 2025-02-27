class Room:
    def __init__(self , player , opponent):
        self.player = player
        self.opponent = opponent

        self.finished = False
        self.data = {
            player : {},
            opponent : {}
        }

    
    def moves(self, client):
        if not self.finished:
            return False
        
        return self.data[self.opponent]
    