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

        print('received ' + filepath)

        file_bytes = fe.getFileBytesFromPath(filepath)

        if file_bytes:

            block_size = 1024
            file_blocks = chunks(file_bytes, block_size)
            last_packet_hash = None
            buffer = None

            for block in reversed(file_blocks):

                if last_packet_hash is None:
                    last_packet_hash = SHA256.new(block).digest()
                    buffer = last_packet_hash
                else:
                    buffer = block + last_packet_hash
                    last_packet_hash = SHA256.new(buffer).digest()

                    tcp.send(len(block).to_bytes(2, "big"))
                    tcp.send(buffer)

                time.sleep(0.01)
            
            tcp.send(len(last_packet_hash).to_bytes(2, "big"))
            tcp.send(last_packet_hash)
            tcp.send((0).to_bytes(2, "big"))
        
        break

    finally:
        tcp.close()
        break

tcp.close()

# file_bytes = selectFileFromBasepath().read()
# block_size = 1024
# file_blocks = chunks(file_bytes, block_size)

# last_packet_hash = None

# for block in reversed(file_blocks):
#     if last_packet_hash is None:
#         last_packet_hash = SHA256.new(block).digest()
#     else:
#         last_packet_hash = SHA256.new(block+last_packet_hash).digest()

# print(last_packet_hash.hex())

