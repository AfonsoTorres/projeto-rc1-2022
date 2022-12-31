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
HOSTNAME = socket.gethostname()

# https://stackoverflow.com/a/57355707/11488921
print("\nResolving IP Address... ")
IP = socket.gethostbyname(HOSTNAME+".local")
print("Done! IP:", IP)
print("")

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

clients = {}
active_clients = 0

def handle_client_connection(client_socket, address):
    global active_clients

    client_id = f"{address[0]}:{address[1]}"

    print(f"Accepted connection from {client_id}")
    headerformat='!BLL'
    try:
        result = get_data(client_socket, headerformat)
        option = int(result["message"])

        if option > 0:
            print(f"Client ({client_id}) chose [{option}] {OPTIONS[option-1]}")

        clients[client_id] = 0
        active_clients += 1

        while True:
            # machine info
            data = data_manager(option)

            # server info
            data["hostname"] = HOSTNAME
            data["ip_addr"] = IP

            data["n_active_clients"] = active_clients
            data["n_clients"] = len(clients)

            # init so that it counts in the total size
            data["bytes"] = 0
            data["total_bytes"] = clients[client_id]
            data["total_bytes_all"] = sum(clients.values())

            # update values with updated size
            data["bytes"] = len(json.dumps(data).encode())
            clients[client_id] += data["bytes"]
            data["total_bytes"] = clients[client_id]
            data["total_bytes_all"] = sum(clients.values())

            result['message'] = json.dumps(data)
            send_data(client_socket, headerformat, result)

    except (socket.timeout, socket.error):
        # remove active client
        active_clients-=1

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
