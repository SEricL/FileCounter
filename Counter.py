import os
import os.path
import re

cont = True

#TODO: Change to non-cmd based (probably tkinter)

def getBytes(name: str) -> int:
    # Returns size of file in bytes. Divide by 1024 for each step up (MB, GB, etc.)
    if isinstance(name, str):
        return os.stat(path + '\\' + name).st_size
    return os.stat(path + '\\' + name[0]).st_size


def bytePrint(bytes: int, mag: str) -> str:
    mag = mag.upper()
    match mag:
        case "KB":
            return str(bytes / 1024) + " KB"
        case "MB":
            return str(bytes / pow(1024, 2)) + " MB"
        case "GB":
            return str(bytes / pow(1024, 3)) + " GB"
        case "TB":
            return str(bytes / pow(1024, 4)) + " TB"
        case _:
            return str(bytes) + " Bytes"


def getFiles(criteria: str, path):
    pattern = re.compile(criteria, re.IGNORECASE)
    # Gets all the files in directory
    fileNames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # Pick matching only
    fileNames = [f for f in fileNames if re.match(pattern, f)]
    # Converts initial list to 2d array with byte size in second slot.
    files = []
    for i in range(len(fileNames)):
        files.append([fileNames[i], getBytes(fileNames[i])])
    files.sort(key=lambda x: x[0])  # Sort by name. (To use index 1
    return files

allFiles = []
queries = []

while cont:
    print("Enter the path you want to search:(exit to end)")
    path = input()

    if len(path) < 3:
        # Default path is directory this file is in
        path = os.path.dirname(__file__)
    if path.lower() == "exit":
        cont = False
        break

    print("The following uses python's Re Library")
    print("Enter criteria:")
    criteria = input()
    files = getFiles(criteria, path)

    allFiles += files
    totalSize = 0  # Wil be kept in bytes, but converted when printed

    for file in files:
        totalSize += file[1]
        print(file[0], bytePrint(file[1], "KB"))

    # Store previous queries
    queries += [path, criteria]

print("Total size:", totalSize)  #TODO: Change to adapt to closest size (kb,mb, etc.)