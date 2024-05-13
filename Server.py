import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER = 2048
PORT = 32973
SERVER = socket.gethostname()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server.bind(ADDR)

clients = []
usernames = []
lock = threading.Lock()


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except socket.error as e:
            print(f"Error sending message to client: {e}")


def handle_client(client, address):
    username = client.recv(HEADER).decode(FORMAT)
    if username in usernames:
        client.send("Username taken".encode(FORMAT))
        client.close()
        return
    else:
        client.send("Username accepted".encode(FORMAT))
        with lock:
            usernames.append(username)
            clients.append(client)
        message = f"{username} has joined the chat."
        broadcast(message.encode(FORMAT))

    try:
        while True:
            msg = client.recv(HEADER).decode(FORMAT)
            if msg != DISCONNECT_MSG:
                message = f"{username}: {msg}"
                print(message)  # Print message to server console
                broadcast(message.encode(FORMAT))
            else:
                message = f"{username} has left the chat."
                print(message)  # Print message to server console
                broadcast(message.encode(FORMAT))
                with lock:
                    clients.remove(client)
                    usernames.remove(username)
                client.close()
                break
    except ConnectionResetError:
        print(f"Connection with {username} forcibly closed by the remote host.")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {address} connected.")
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
