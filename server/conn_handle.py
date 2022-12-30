import struct

def get_data(sock, header_format):
    # fetch packet header
    req = sock.recv(struct.calcsize(header_format))
    packet_header = struct.unpack(header_format, req)
    version,size,order = packet_header

    # fetch packet data
    req = sock.recv(size)
    packet_data = struct.unpack(f"{size}s", req)
    data = packet_data[0].decode()

    return {
            'version': int(version),
            'size': int(size),
            'order':int(order),
            'message': data
        }

def send_data(sock, header_format, data):
    message = data['message'].encode()
    size = len(message)
    packet = struct.pack(f"{header_format}{size}s", data['version'], size, data['order'], message)
    sock.send(packet)
