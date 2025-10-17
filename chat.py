from datetime import datetime, timedelta
import time
import threading
import server
IDLE_TIMEOUT = 300
last_activity = datetime.now()
running = True

def broadcast(message, sender=None):
    with server.LOCK:
        for client in list(server.clients.keys()):
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    client.close()
                    del server.clients[client]


def remove_client(client, username, notify=False):
    with server.LOCK:
        if client in server.clients:
            del server.clients[client]
        if username in server.nicknames:
            server.nicknames.remove(username)
    client.close()
    if notify:
        broadcast(f"{username} has left the chat.")


def handle_client(client):
    username = server.clients.get(client, "Unknown")
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if not msg:
                break

            if msg.strip().lower() == "/quit":
                client.send("Bye!".encode("utf-8"))
                remove_client(client, username, notify=True)
                break

            broadcast(f"{username}: {msg}", sender=client)

        except Exception as e:
            print(f"Error handling client {username}: {e}")
            remove_client(client, username, notify=True)
            break


def accept_clients():
    """Main loop that accepts clients and authenticates them."""
    if server.SERVER_SOCKET is None:
        print("SERVER_SOCKET is None. Start the server first.")
        return
    global running
    print("Waiting for clients...")
    while running:
        if datetime.now() - last_activity > timedelta(seconds=IDLE_TIMEOUT):
            print("Server idle for 5 minutes. Shutting down...")
            break
        try:
            
            client, address = server.SERVER_SOCKET.accept()
            print(f"Connection from {address}")

            
            client.send("Enter server password: ".encode("utf-8"))
            entered = client.recv(1024).decode("utf-8").strip()
            if entered != server.PASSWORD:
                client.send("Wrong password. Disconnecting.".encode("utf-8"))
                client.close()
                continue

            
            client.send("Enter your nickname: ".encode("utf-8"))
            while True:
                username = client.recv(1024).decode("utf-8").strip()
                if username in server.nicknames or not username:
                    client.send("Nickname taken. Enter another: ".encode("utf-8"))
                else:
                    break

            
            with server.LOCK:
                server.clients[client] = username
                server.nicknames.add(username)

            print(f"{username} joined from {address}")
            broadcast(f"{username} joined the chat!", sender=client)
            client.send("Connected! Type /quit to leave.".encode("utf-8"))

           
            thread = server.threading.Thread(target=handle_client, args=(client,))
            thread.start()

        except Exception as e:
            print(f" {e}")


def stop():
    while True:
        cmd = input()
        if cmd.strip().lower() == "/stop":
            print("Shutting down server...")
            global running
            running = False
            print("Closing all client connections...")
            with server.LOCK:
                for c in list(server.clients.keys()):
                    try:
                        c.send("Server is shutting down.".encode("utf-8"))
                        c.close()
                    except:
                        pass
                server.clients.clear()

            server.SERVER_SOCKET.close()
            print("Server terminated.")
threading.Thread(target=stop, daemon=True).start()