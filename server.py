import socket
from _thread import *
from player import Player
from enemy import *
import pickle
import sys



print("here!")
server_ip = socket.gethostname()  
port = 5550  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("after socket()")
try:
    print("before bind3")
    s.bind((server_ip, port))
    print("after bind()")
    s.listen(2)
    print("Waiting for connection, server started")
except socket.error as e:
    str(e)

#  pos = [(0, 0), (100, 100)]  #list of positions from p1 and p2
players = [Player(20, 20, 50, 50, (255, 0, 0), None, 0), Player(1350, 20, 50, 50, (0, 0, 255), None, 1)] #(1400, 20)


def threaded_client(conn, player_num):
    conn.send(pickle.dumps(players[player_num]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2))
            players[player_num] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player_num == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                #print("Received: ", data)
                #print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()
    # sys.exit()

currentPlayer = 0

while True:
    client_sock, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (client_sock, currentPlayer))
    currentPlayer += 1
