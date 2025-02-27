import socket
import threading
import json
from protocols import Protocol

class Client:
    def __init__(self , host  = socket.gethostbyname(socket.gethostname()), port = 5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.nickname = None

        self.closed = False
        self.started = False
        self.opponent = None
        self.player_move = {}
        self.opponent_moved = {}
        
        self.info = ''
        self.receive_ = False

    def start(self):
        receive_thread = threading.Thread(target=self.receive)  # Change self.start to self.receive
        receive_thread.start()

    def send(self , request , data):
        data = {
            'type': request,
            'data': data
        }
        try:
            self.server.send(json.dumps(data).encode('ascii'))
        except:
            pass

    def receive(self):
        while not self.closed:
            self.receive_ = True
            try:
                data = self.server.recv(2048).decode('ascii')
                message = json.loads(data)
                self.handle_response(message)
            except:
                pass

    def close(self):
        self.closed = True
        self.server.close()

    def handle_response(self, response):
        r_type = response['type']
        data = response['data']
        self.info = r_type
        if r_type == Protocol.Responce.Opponent:
            self.opponent = data
        
        elif r_type == Protocol.Responce.Start:
            self.started = True  
            
        elif r_type == Protocol.Responce.Opponent_left:
            self.close()

        elif r_type == Protocol.Responce.Opponent_moved:
            self.opponent_moved = data

    def opponent_move(self):
        pass