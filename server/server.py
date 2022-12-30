import socket
import threading
import signal
import sys
import psutil
import json

from conn_handle import get_data, send_data

def signal_handler(sig, frame):
    print('\nDone')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

OPTIONS = ["All Data", "CPU Usage", "Battery Level"]

def get_battery_data():
    battery_data = psutil.sensors_battery()
    return {
        "percentage": battery_data.percent,
        "time_left": battery_data.secsleft,
        "plugged": battery_data.power_plugged
    } 

def data_manager(option):
    data = {}
    if option in [1,2]:
        data["cpu_usage"] = str(psutil.cpu_percent(1))

    if option in [1,3]:
        data["battery"] = get_battery_data()

    return data 

def handle_client_connection(client_socket, address):
    print(f"Accepted connection from {address[0]}:{address[1]}")
    headerformat='!BLL'
    try:
        result = get_data(client_socket, headerformat)
        option = int(result["message"])

        if option > 0:
            print(f"Client ({address[0]}:{address[1]}) chose [{option}] {OPTIONS[option-1]}")

        while True:
            result['message'] = json.dumps(data_manager(option))
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
