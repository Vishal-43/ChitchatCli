import socket
import threading
import time

broadcast_port=9999
DISCOVERY_MSG = b"CHITCHAT_DISCOVERY_REQUEST"
RESPONSE_PREFIX = b"CHITCHAT_SERVER|"

def broadcast_discovery(tcp_port):
    udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = f"CHITCHAT_SERVER|{tcp_port}"
    while True:
        udp.sendto(msg.encode('utf-8'), ('<broadcast>', broadcast_port))
        time.sleep(1)
    
def discover_servers(timeout=5):
    udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.bind(("0.0.0.0",broadcast_port))
    udp.settimeout(timeout)
    start_time = time.time()
    found = {}
    print("Searching for servers...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            data,addr = udp.recvfrom(1024)  
            if data.startswith(RESPONSE_PREFIX):
                _,port = data.decode('utf-8').split("|")
                found[addr[0]] = int(port)
        except socket.timeout:
            break
    return found
