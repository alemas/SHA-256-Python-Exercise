import socket
import sys
from Crypto.Hash import SHA256
import file_explorer as fe


HOST = 'localhost'
PORT = 10000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
tcp.connect(server_address)

filepath = fe.selectFileFromBasepath()
tcp.send(filepath.encode("utf-8"))

packet_size = -1
packet = None
first = True

while True:
    packet_size = int.from_bytes(tcp.recv(sys.getsizeof(0)), "big")
    if packet_size == 0:
        break
    
    packet = tcp.recv(packet_size)

    if first:
        first = False
        print(packet.hex())
    # if packet:
    #     print(packet)

print(packet.hex())
tcp.close()