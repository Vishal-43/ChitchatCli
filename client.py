# client.py
import socket
import threading

def receive(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("⚠️ Disconnected from server.")
            sock.close()
            break

def main():
    host = input("Server IP (default 127.0.0.1): ").strip() or "127.0.0.1"
    port = int(input("Server Port: ").strip())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Connected to the server!")

    threading.Thread(target=receive, args=(s,), daemon=True).start()

    while True:
        msg = input()
        if msg.strip().lower() == "/quit":
            s.send(msg.encode("utf-8"))
            break
        s.send(msg.encode("utf-8"))

    s.close()


