import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 5550
        self.addr = (self.server, self.port)
        self.connections = 0
        self.p = self.connect()

    def get_cons(self):
        return self.connections

    def getP(self):
        return self.p

    def connect(self):
        self.connections += 1
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
