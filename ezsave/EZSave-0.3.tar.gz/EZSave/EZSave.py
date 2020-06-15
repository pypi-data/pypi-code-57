from os import path
class save:
    def SetInt(name : str, tosave : int):
        output = open(f'{name}_i.txt', 'w')
        output.write(str(tosave))
        output.close()
    
    def GetInt(name : str):
        if path.exists(f'{name}_i.txt'):
            inp = open(f'{name}_i.txt', 'r')
            get = int(inp.read())
            inp.close()
            return get
        else:
            save.SetInt(name, 0)
            return 0
    
    def SetFloat(name : str, tosave : float):
        output = open(f'{name}_f.txt', 'w')
        output.write(tosave)
        output.close()
    
    def GetFloat(name : str):
        if path.exists(f'{name}_f.txt'):
            inp = open(f'{name}_f.txt', 'r')
            get = float(inp.read())
            inp.close()
            return get
        else:
            save.SetInt(name, 0)
            return 0
    
    def SetStr(name : str, tosave : str):
        output = open(f'{name}_s.txt', 'w')
        output.write(tosave)
        output.close()
    
    def GetStr(name : str):
        if path.exists(f'{name}_s.txt'):
            inp = open(f'{name}_s.txt', 'r')
            get = float(inp.read())
            inp.close()
            return get
        else:
            save.SetInt(name, 0)
            return 0