import socket
import json
import threading
from protocols import Protocol

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostbyname(socket.gethostname()), 5555))
        self.started = False
        self.closed = False
        self.receive_ = False
        self.info = None
        self.opponent_moved = {
            'pos' : [0,0], 
            'bullet' : [],
            'center' : [0,0]
        }
        self.bullet = None
        self.winner = False
        self.opponent_leave = False

    def start(self):
        self.receive_ = True
        thread = threading.Thread(target=self.receive)
        thread.start()

    def send(self, r_type, data):
        if self.closed:
            print("Cannot send data, socket is closed")
            return

        message = {
            'type': r_type,
            'data': data
        }
        message_str = json.dumps(message)
        try:
            self.client.send(message_str.encode('ascii'))
        except ConnectionAbortedError as e:
            print(f"Error sending data: {e}")
        except OSError as e:
            print(f"OS error sending data: {e}")
        except Exception as e:
            print(f"Unexpected error sending data: {e}")

    def receive(self):
        while self.receive_:
            try:
                
                data = self.client.recv(2048 * 4).decode('ascii')
                if data:
                    message = json.loads(data)
                    self.info = data
                    self.handle_message(message)
                else:
                    print("Received empty data")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.receive_ = False

    def handle_message(self, message):
        r_type = message['type']
        data = message['data']

        if r_type == Protocol.Responce.Start:
            self.winner = False
            self.opponent_leave = False
            self.started = True
        elif r_type == Protocol.Responce.Opponent_moved:
            self.opponent_moved['pos'] = data['pos']
            self.opponent_moved['bullet'] = data['bullet']
            self.opponent_moved['center'] = data['center']
        elif r_type == Protocol.Responce.Opponent_left:
            self.started = False
            self.client.close()

        elif r_type == Protocol.Responce.loser:
            self.winner = True
            self.started = False
            self.opponent_leave = True
            self.client.close()


    def close(self):
        self.client.close()