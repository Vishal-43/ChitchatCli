# client.py
import socket
import threading
from discover import discover_servers

def receive(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Disconnected from server.")
            sock.close()
            break

def main():
    try:
        servers = discover_servers()
        if servers:
            print("Discovered servers:")
            for i, (ip, port) in enumerate(servers.items(), 1):
                print(f"{i}. {ip}:{port}")
            choice = input("Select server number or press Enter to connect manually: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(servers):
                host = list(servers.keys())[int(choice) - 1]
                port = servers[host]
            else:
                host = input("Server IP (default 127.0.0.1): ").strip() or "127.0.0.1"
                port = int(input("Server Port (default 9999): ").strip()) or 9999
        

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
    except Exception as e:
        print("")


