import socket
import threading
import getpass
from datetime import datetime


clients = {} 
nicknames = set()
LOCK = threading.Lock()
SERVER_SOCKET = None
PASSWORD = None
SERVER_PORT = None


def start():
    global SERVER_SOCKET, PASSWORD, SERVER_PORT

   
    while True:
        try:
            SERVER_PORT = int(input("Enter server port (1024–65535): "))
            if 1024 <= SERVER_PORT <= 65535:
                break
            print("Port must be in range 1024–65535.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    
    PASSWORD = getpass.getpass("Set a password: ").strip()
    if not PASSWORD:
        print("Password cannot be empty.")
        return

    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", SERVER_PORT))
        s.listen()
        SERVER_SOCKET = s
        print(f"✅ Server started on port {SERVER_PORT}")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return

    
    import chat
    chat.accept_clients()


