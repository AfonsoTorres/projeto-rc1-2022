import socket
import signal
import sys
import struct
import os

from conn_handle import get_data, send_data

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

ip_addr = "198.173.173.227"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))


headerformat='!BLL'
order = 0
while True:
    try:
        message = input("Message to send? ")
        order += 1
        send_data(sock, headerformat, {"message": message, "version": 1, "order": order})
        while True:
            result = get_data(sock, headerformat)
            percentage = int(float(result['message']))
            offset = 30
            bar = int(percentage*offset/100)
            blank = offset-bar

            os.system('clear')

            print("CPU: [", end="")
            print("|"*(bar), " "*blank, "] ", end="")
            print(percentage, "%", " "*5)

    except (socket.timeout, socket.error):
        print("Server error. Done!")
        sys.exit(0)
