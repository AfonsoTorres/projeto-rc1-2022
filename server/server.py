import socket
import threading
import signal
import sys
import struct
import psutil

from conn_handle import get_data, send_data

def signal_handler(sig, frame):
    print('\nDone')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

def handle_client_connection(client_socket, address):
    print(f"Accepted connection from {address[0]}:{address[1]}")
    headerformat='!BLL'
    try:
        result = get_data(client_socket, headerformat)

        print(f"Received ver: {result['version']}, size: {result['size']}, order: {result['order']} -> {result['message']}")

        while True:
            result['message'] = str(psutil.cpu_percent(1))
            send_data(client_socket, headerformat, result)

    except (socket.timeout, socket.error):
        print(f"Client {address} error. Done!")
    finally:
        client_socket.close()

ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))
server.listen(5)

print(f"Listening on {ip_addr}:{tcp_port}")

while True:
    client_sock, address = server.accept()
    client_handler = threading.Thread(target=handle_client_connection, args=(client_sock, address), daemon=True)
    client_handler.start()
