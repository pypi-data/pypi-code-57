class save:
    def SaveInt(self, name : str, tosave : int):
        output = open(f'{name}.txt', 'w')
        output.write(str(tosave))
        output.close()
    
    def GetInt(self, name : str):
        inp = open(f'{name}.txt', 'r')
        get = int(inp.read())
        inp.close()
        return get
    
    def SetFloat(self, name : str, tosave : float):
        output = open(f'{name}.txt', 'w')
        output.write(str(tosave))
        output.close()
    
    def GetFloat(self, name : str):
        inp = open(f'{name}.txt', 'r')
        get = float(inp.read())
        inp.close()
        return get
    
    def SetStr(self, name : str, tosave : str):
        output = open(f'{name}.txt', 'w')
        output.write(tosave)
        output.close()
    
    def GetStr(self, name : str):
        inp = open(f'{name}.txt', 'r')
        get = inp.read()
        inp.close()
        return get