import os
import os.path
import re
import time
from tkinter import ttk
from tkinter import *

cont = True


# TODO: Change to non-cmd based (probably tkinter)

def getBytes(name: str, path) -> int:
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
    try:
        pattern = re.compile(criteria, re.IGNORECASE)
        # Gets all the files in directory
        fileNames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        # Pick matching only
        fileNames = [f for f in fileNames if re.match(pattern, f)]
        # Converts initial list to 2d array with byte size in second slot.
        files = []
        for i in range(len(fileNames)):
            files.append([fileNames[i], getBytes(fileNames[i], path)])
        files.sort(key=lambda x: x[0])  # Sort by name. (To use index 1
        return files
    except FileNotFoundError as e:
        print(e)
        return None


class Window:

    def __init__(self, root):
        self.path = ''
        self.criteria = ''
        self.all_files = []
        self.query_history = []
        self.query_list = []
        self.root = root
        self.total_size = 0

        self.root.title("File Counter")

        self.main_frame = ttk.Frame(self.root, padding="12 12 12 12", borderwidth=5, relief='groove')
        self.main_frame.pack()

        result_frame = ttk.Frame(self.root, padding="12 12 12 12", borderwidth=5, relief='groove')
        result_frame.pack()

        self.listbox = Listbox(result_frame, width=50)
        self.listbox.pack()

        path_text = Label(self.main_frame, text="Path:")
        path_text.pack()

        self.path = StringVar()
        path_entry = ttk.Entry(self.main_frame, width=50, textvariable=self.path)
        path_entry.pack()

        crit_text = Label(self.main_frame, text="Criteria(Regex):")
        crit_text.pack()

        self.criteria = StringVar()
        crit_entry = ttk.Entry(self.main_frame, width=50, textvariable=self.criteria)
        crit_entry.pack()

        go_button = Button(self.main_frame, text="Search", command=self.search)
        go_button.pack()

        root.bind("<Return>", lambda e: self.search)

    def search(self):
        files = getFiles(str(self.criteria.get()), str(self.path.get()))
        if files == None:
            return
        elif len(files) <= 0:
            print("Nothing found")
            return
        self.all_files += files

        for file in files:
            self.total_size += file[1]
            self.listbox.insert(END, file[0] + " " + bytePrint(file[1], "KB"))

    def clear(self):
        self.listbox.delete(0, END)
        self.total_size = 0
        self.all_files = []
        self.query_list = []


root = Tk()

Window(root)

root.mainloop()
