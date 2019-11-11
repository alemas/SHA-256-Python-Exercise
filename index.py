import os
import math
import numpy as np
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

file_bytes = selectFileFromBasepath().read()
block_size = 1024
file_blocks = np.array_split(file_bytes, block_size)

print(file_blocks[3:5])

last_block_hash = None

for block in reversed(file_blocks):
    if len(block) < block_size:
        last_block_hash = sha256.new(block)


# last_block_size = len(file_bytes) % block_size
# total_blocks = math.ceil(len(file_bytes) / block_size)

# current_block = None

# for i in range(total_blocks, 0, -1):
#     if current_block == None:
#         print(i)
#         block_range = slice(i * block_size, (i * block_size) + last_block_size)
#         print("range = " + str(block_range))
#         current_block = file_bytes[block_range]

# print(len(current_block))