import os
import math
import socket
from Crypto.Hash import SHA256
import file_explorer as fe
import time

def chunks(list, chunk_size):
    chunks = []
    for i in range(0, len(list), chunk_size):
        chunks.append(list[i:i + chunk_size])
    return chunks

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    tcp, client_address = sock.accept()
    try:
        print('connection from', client_address)
        
        filepath = tcp.recv(32).decode("utf-8")

        print('received request for file ' + filepath)

        file_bytes = fe.getFileBytesFromPath(filepath)

        if file_bytes:

            block_size = 1024
            file_blocks = chunks(file_bytes, block_size)
            last_packet_hash = None

            packets = []

            for block in reversed(file_blocks):
                if last_packet_hash is None:
                    last_packet_hash = SHA256.new(block).digest()
                    packets.insert(0, last_packet_hash)
                else:
                    packet = block + last_packet_hash
                    packets.insert(0, packet)
                    last_packet_hash = SHA256.new(packet).digest()
            
            print(last_packet_hash.hex())
            print(packets[0].hex())

            for packet in packets:
                tcp.send(len(packet).to_bytes(2, "big"))
                tcp.send(packet)
                time.sleep(0.001)
            
            tcp.send((0).to_bytes(2, "big"))

    finally:
        print("done")

tcp.close()

