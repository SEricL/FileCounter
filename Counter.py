import os
import os.path
import re


print("Enter the path you want to search:")
path = input()

if len(path) < 3:
    # Default path is directory this file is in
    path = os.path.dirname(__file__)

def getBytes(name: str) -> int:
    # Returns size of file in bytes. Divide by 1024 for each step up (MB, GB, etc.)
    if isinstance(name, str):
        return os.stat(path + '\\' + name).st_size
    return os.stat(path + '\\' + name[0]).st_size

def bytePrint(bytes: int, mag: str) -> str:
    mag = mag.upper()
    match mag:
        case "MB":
            return bytes / pow(1024,2)
        case "GB":
            return bytes / pow(1024,3)
        case "TB":
            return bytes / pow(1024,4)
        case _:
            return bytes

def getFiles(criteria: str, path):
    pattern = re.compile(criteria, re.IGNORECASE)
    # Gets all the files in directory
    fileNames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    fileNames = [f for f in fileNames if re.match(pattern, f)]
    # Converts initial list to 2d array with byte size in second slot.
    files = []
    for i in range(len(fileNames)):
        files.append([fileNames[i], getBytes(fileNames[i])])
    files.sort(key=lambda x: x[0])
    return files

print("The following uses python's Re Library")
print("Enter criteria:")
criteria = input()
files = getFiles(criteria, path)

filesCopy = files.copy()
sizes = []
totalSize = 0  # Wil be kept in bytes, but converted when printed

while len(filesCopy) > 0:
    # File group criteria
    current = filesCopy[0][0]
    currentSize = 0
    while len(filesCopy) > 0 and current in filesCopy[0][0]:
        if current in filesCopy[0][0]:
            currentSize += filesCopy[0][1]
            filesCopy.pop(0)
    totalSize += currentSize
    currentSize /= (1024 * 1024)  # Outputs MB. (If less than 1, puts 0)
    sizes.append([current, int(currentSize)])


# print(sizes)
sizes.sort(key=lambda x: x[1])
sizes.reverse()
for a, s in sizes:
    print(a, s, 'MB')