import os

def selectFileFromBasepath(basepath = "data") :
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

    return open(basepath + "/" + files[option])

file = selectFileFromBasepath()
