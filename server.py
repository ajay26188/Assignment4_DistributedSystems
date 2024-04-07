#I used one youtube tutorial for this assigment.
#Source: https://www.youtube.com/watch?v=nmzzeAvQHp8

import threading 
import socket

#Creating server configuration
host = '127.0.0.1'
port = 3000

#Creating two lists to store clients and their nicknames
clients = []
nicknames = []

#This function is to broadcast messages to all the clients
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(message)

#This function is to handle each client's connection
def handle_client(client):
    while True:
        try:
            #Receiving message from client
            message = client.recv(1024)
            if message:
                #Private messaging
                if message.decode('utf-8').startswith('private'):
                    receiver, private_message = message.decode('utf-8').split(maxsplit=2)[1:]
                    receiver_client = clients[nicknames.index(receiver)]
                    receiver_client.send(f'(Private) {nicknames[clients.index(client)]}: {private_message}'.encode('utf-8'))

                #Quitting the chat and closing the connection
                elif message.decode('utf-8') == 'quit':
                    index = clients.index(client)
                    nickname = nicknames[index]
                    broadcast(f'{nickname} has left the chat room!'.encode('utf-8'))
                    nicknames.remove(nickname)
                    clients.remove(client)
                    client.close()
                    break

                else:
                    #Broadcasting message to all clinets
                    broadcast(message,client)

        except:
            #If there is an error, the program will remove client from the list and the connection is lost
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            broadcast(f'{nickname} has left the chat room!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

#This is the main function to accept client connections
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f'Server is running and listening on {host}:{port}...')

    while True:
        client, address = server.accept()
        print(f'Connection established with {address}')

        client.send('nickname?'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        #Adding client and its nickname to the lists
        nicknames.append(nickname)
        clients.append(client)
        print(f'{nickname} has connected to the chat room')

        broadcast(f'{nickname} has joined the chat room!'.encode('utf-8'),client)
        client.send('Welcome to the chat room!'.encode('utf-8'))

        #Creating a new thread for handling client's connection
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()

            