import socket 
import threading
import json
from protocols import Protocol
from room import Room

class Server:
    def __init__(self, host = socket.gethostbyname(socket.gethostname()), port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("Server Ready")

        self.player = {}
        self.opponent = {}
        self.rooms = {}
        self.waiting_for_player = None

    def receive(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {addr}")
            thread = threading.Thread(target=self.handle , args=(client, ))
            thread.start()

    def handle(self,client):
        self.handle_connect(client)
        self.wait_for_room(client)

        while True:
            try:
                data = client.recv(2048).decode('ascii')

                if not data:
                    break

                else:
                    message = json.loads(data)
                    self.handle_message(message , client)
            
            except Exception as e:
                print(f"Error receiving data: {e}")  # Add this line for debugging
                break

        self.send_to_opponent(Protocol.Responce.Opponent_left, None, client)
        self.disconnect(client)


    def handle_connect(self , client):
        while True:
            self.send(Protocol.Request.Nickname , None , client)
            try:
                message_ = client.recv(2048).decode('ascii')
                print(message_)
                message = json.loads(message_)
            except socket.error as e:
                print('break ' , e)
                break

            r_type = message['type']
            data = message['data']

            if r_type == Protocol.Request.Nickname:
                self.player[client] = data
                print(f'{client}\nThe Name Is {data}')

            else:
                continue

            if not self.waiting_for_player:
                self.waiting_for_player = client
                print(f"Waiting for Pair : {client}")
            
            else:
                self.join_room(client)
            
            break

    def join_room(self , client):
        room = Room(client , opponent = self.waiting_for_player)
        self.opponent[client] = self.waiting_for_player
        self.opponent[self.waiting_for_player] = client

        self.send(Protocol.Responce.Opponent , self.player[client] , self.waiting_for_player)
        self.send(Protocol.Responce.Opponent , self.player[self.waiting_for_player] , client)

        print("Sending start message to both players") 
        self.send(Protocol.Responce.Start , self.player[client] , self.waiting_for_player)
        self.send(Protocol.Responce.Start , self.player[self.waiting_for_player] , client)

        print(f"Room created: {room}, Players: {self.player[client]}, {self.player[self.waiting_for_player]}") 

        self.rooms[client] = room
        self.rooms[self.waiting_for_player] = room
        self.waiting_for_player = None

    def wait_for_room(self , client):
        while True:
            room = self.rooms.get(client)
            opponent = self.opponent.get(client)

            if room and opponent:
                self.send(Protocol.Responce.Start, None , client)
                print(f"Joined {room} room")
                break
    
    def handle_message(self , message , client):
        r_type = message['type']
        data = message['data']
        room = self.rooms[client]

        if r_type != Protocol.Request.Move:
            return
        
        self.send_to_opponent(Protocol.Responce.Opponent_moved , data , client )

    def send(self ,r_type , data ,  client):
        message = {
            'type': r_type,
            'data': data
        }

        try:
            client.send(json.dumps(message).encode('ascii'))
        
        except ConnectionError:
            print(f"Connection with {client} was reset.")
            self.disconnect(client)

    def send_to_opponent(self ,r_type ,data ,  client):
        opponent = self.opponent.get(client)
        if not opponent:
            return
        self.send(r_type, data, opponent)

    def disconnect(self , client):
        opponent = self.opponent.get(client)

        print(f"Disconnecting {client} ")

        if opponent in self.opponent:
            del self.opponent[opponent]
        if client in self.player:
            del self.player[client]
        if opponent in self.player:
            del self.player[opponent]
        if client in self.opponent:
            del self.opponent[client]
        if client in self.rooms:
            del self.rooms[client]
        if opponent in self.rooms:
            del self.rooms[opponent]

        client.close()