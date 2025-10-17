import socket 
import threading
import time 
from datetime import datetime 
import getpass

while True:
    try:
        server_id = int(input("enter a server id (1024-65535): "))
        if 1024 <= server_id <= 65535:
            break
        else:
            print("please enter a valid port number between 1024 and 65535")
    except ValueError:
        print("please enter a valid integer port number")


password = getpass.getpass("set a password for the server:")
if not password:
    print("password cannot be empty. exiting...")
    exit()
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0',server_id))
    server.listen()
    print(f"server started on port {server_id}")
except Exception as e:
    print(f"failed to start server: {e}")
    exit()


    