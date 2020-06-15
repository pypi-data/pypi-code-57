class save:
    def SaveInt(name : str, tosave : int):
        output = open(f'{name}.txt', 'w')
        output.write(str(tosave))
        output.close()
    
    def GetInt(name : str):
        inp = open(f'{name}.txt', 'r')
        get = int(inp.read())
        inp.close()
        return get
    
    def SetFloat(name : str, tosave : float):
        output = open(f'{name}.txt', 'w')
        output.write(str(tosave))
        output.close()
    
    def GetFloat(name : str):
        inp = open(f'{name}.txt', 'r')
        get = float(inp.read())
        inp.close()
        return get
    
    def SetStr(name : str, tosave : str):
        output = open(f'{name}.txt', 'w')
        output.write(tosave)
        output.close()
    
    def GetStr(name : str):
        inp = open(f'{name}.txt', 'r')
        get = inp.read()
        inp.close()
        return get