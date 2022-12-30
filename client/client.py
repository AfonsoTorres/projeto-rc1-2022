import socket
import signal
import sys
import os
import json

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

OPTIONS = ["All Data", "CPU Usage", "Battery Level"]

def menu():
    return f"Server Data. Choose an option:\n{''.join([f'[{i+1}] {OPTIONS[i]}{chr(10)}' for i in range(len(OPTIONS))])}"

def print_bar(title, percentage, bar_end=""):
    offset = 30
    bar = int(percentage*offset/100)
    blank = offset-bar

    print(f"{title}: [ ", end="")
    print("|"*(bar), f'{" "*blank}] ', end="")
    print(f'{percentage:4d}', "%", end=bar_end)


headerformat='!BLL'
order = 0
while True:
    try:
        option = input(f"{menu()}[0] Exit\nOption: ")
        order += 1
        send_data(sock, headerformat, {"message": option, "version": 1, "order": order})
        while True:
            result = get_data(sock, headerformat)
            values = json.loads(result["message"])

            if not values:
                sys.exit(0)

            os.system('clear')

            print("Server Data:")

            if option in ['1','2']:
                cpu_percentage = int(float(values['cpu_usage']))
                print_bar("CPU", cpu_percentage, '\n')

            if option in ['1','3']:
                battery_percentage = int(float(values['battery']['percentage']))
                print_bar("BAT", battery_percentage)

                print(" [✓]" if values['battery']['plugged'] else " [x]", "Plugged", end='\n')

    except (socket.timeout, socket.error):
        print("Server error. Done!")
        sys.exit(0)
