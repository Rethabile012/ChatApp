import socket
import threading

HEADER = 2048
PORT = 32973
SERVER = "35.208.151.24"
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


def receive():
    while True:
        message = client.recv(HEADER).decode(FORMAT)
        print(message)


def start_chat():
    while True:
        username = input("Enter your username: ")
        client.send(username.encode(FORMAT))
        response = client.recv(HEADER).decode(FORMAT)
        if response == "Username taken":
            print("Username already exists. Please choose a different username.")
        else:
            print(response)
            break

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    while True:
        msg = input("Enter message: ")
        send(msg)
        if msg == DISCONNECT_MSG:
            break

    receive_thread.join()


print("[STARTING] Client is starting...")
start_chat()

client.close()
