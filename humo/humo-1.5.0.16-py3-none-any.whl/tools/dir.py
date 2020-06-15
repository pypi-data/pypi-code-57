import pathlib
import pprint
import os, tkinter, tkinter.filedialog, tkinter.messagebox

class plib:
    def __init__(self,path):
        self.path = path
        self.p = pathlib.Path(path)

    def isdirctory(self):
        pprint.pprint(self.p.iterdir())
    

def findfile():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp)
    return file