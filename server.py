#!/bin/python3

import socket
import threading

host = '192.168.56.101'
port = 55550

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nickname[index]
            broadcast('{} left!'.format(nickname).encode())
            nickname.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode())
        client.send("Connected to server!".encode())

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("Server is listening...")
receive()

