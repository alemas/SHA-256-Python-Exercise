import os
import math
from Crypto.Hash import SHA256

def selectFileFromBasepath(basepath = "data"):
    files = []
    index = 0
    print("Escolha o arquivo a ser usado:")
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            print(str(index) + " - " + entry)
            files.append(entry)
            index += 1

    option = int(input("\n"))
    while (option < 0 or option >= index):
        option = int(input("Escolha uma opção válida\n"))

    return open(basepath + "/" + files[option], "rb")

def chunks(list, chunk_size):
    chunks = []
    for i in range(0, len(list), chunk_size):
        chunks.append(list[i:i + chunk_size])
    return chunks

file_bytes = selectFileFromBasepath().read()
block_size = 1024
file_blocks = chunks(file_bytes, block_size)

last_packet_hash = None

for block in reversed(file_blocks):
    if last_packet_hash is None:
        last_packet_hash = SHA256.new(block).digest()
    else:
        last_packet_hash = SHA256.new(block+last_packet_hash).digest()

print(last_packet_hash.hex())