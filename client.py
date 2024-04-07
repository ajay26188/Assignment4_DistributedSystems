#I used one youtube tutorial for this assigment.
#Source: https://www.youtube.com/watch?v=nmzzeAvQHp8

import threading
import socket

#This function is to handle receiving messages from the server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "nickname?":
                client.send(chosen_nickname.encode('utf-8'))
            else:
                print(message)
        
        except:
            print('Error!')
            client.close()
            break

#This function is to handle sending messages to the server
def client_send():
    while True:
        try:
            #Prompting user to input message
            message = input("")

            #To quit the chatroom
            if message == 'quit':
                client.send(message.encode('utf-8'))
                break
            #To send a private message to specific user
            elif message.startswith('private'):
                receiver, private_message = message.split(maxsplit=2)[1:]
                private_message = f'private {receiver} {private_message}'
                client.send(private_message.encode('utf-8'))

            else:
                message_with_nickname = f'{chosen_nickname}: {message}'
                client.send(message_with_nickname.encode('utf-8'))

        except:
            print('Error!')
            client.close()
            break

#Prompting the client to choose a nickname
chosen_nickname = input('Choose a nickname: ')

#Creating a socket for client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connecting client to server
client.connect(('127.0.0.1',3000))

#Creating a thread to handle receiving messages
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

#Creating a thread to handle sending messages
send_thread = threading.Thread(target=client_send)
send_thread.start()


