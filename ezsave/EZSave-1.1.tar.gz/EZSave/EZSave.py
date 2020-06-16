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
    
    def IntSaveExsists(name : str):
        if path.exists(f'{name}_i.txt'):
            return True
        else:
            return False
    
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
            save.SetFloat(name, 0.0)
            return 0.0
    
    def FloatSaveExsists(name : str):
        if path.exists(f'{name}_f.txt'):
            return True
        else:
            return False

    def SetStr(name : str, tosave : str):
        output = open(f'{name}_s.txt', 'w')
        output.write(tosave)
        output.close()
    
    def GetStr(name : str):
        if path.exists(f'{name}_s.txt'):
            inp = open(f'{name}_s.txt', 'r')
            get = inp.read()
            inp.close()
            return get
        else:
            save.SetStr(name, '')
            return ''

    def StrSaveExsists(name : str):
        if path.exists(f'{name}_s.txt'):
            return True
        else:
            return False

    def SetStrArr(name : str, tosave : list):
        output = open(f'{name}_a.txt', 'w')
        output.write('\n'.join(tosave))
        output.close()
    
    def GetStrArr(name : str):
        if path.exists(f'{name}_a.txt'):
            inp = open(f'{name}_a.txt', 'r')
            get = inp.read().split('\n')
            inp.close()
            return get
        else:
            save.SetStrArr(name, [''])
            return []

    def ArrSaveExsists(name : str):
        if path.exists(f'{name}_a.txt'):
            return True
        else:
            return False
class level:
    def CreateSystem(system_name : str):
        save.SetStrArr(system_name, [''])
    
    def CheckSystemExsists(system : str):
        if path.exists(f'{system}_a.txt'):
            return True
        else: return False
    
    def AddUser(system : str, user : str):
        sys = save.GetStrArr(system)
        if user in sys:
            return
        else:
            sys.append(user)
            save.SetStrArr(system, sys)
    
    def CalcLevelXP(lvl : int):
        xp = 25
        if lvl > 0:
            for x in range(lvl):
                xp += xp // 2 + round(xp * 0.25)
        return xp

    def AddXP(system : str, user : str, amount : int):
        xp = save.GetInt(f'{user}_{system}_xp') + amount
        save.SetInt(f'{user}_{system}_xp', xp)
        lvl = save.GetInt(f'{user}_{system}_lvl')
        lvlup = False
        while True:
            if level.CalcLevelXP(lvl) <= xp:
                lvl += 1
                lvlup = True
            else: break
        save.SetInt(f'{user}_{system}_lvl', lvl)
        return lvlup
    
    def Level(system : str, user : str):
        sys = save.GetStrArr(system)
        exsists = False
        for x in sys:
            if x == user:
                exsists = True
                break
        if exsists:
            xplvlarr = [save.GetInt(f'{user}_{system}_lvl'), save.GetInt(f'{user}_{system}_xp'), level.CalcLevelXP(save.GetInt(f'{user}_{system}_lvl'))]
            return xplvlarr
        else:
            level.AddUser(system, user)
            return [0, 0, level.CalcLevelXP(save.GetInt(f'{user}_{system}_lvl'))]
    
    def BestLevel(system : str):
        bestlvl = 0
        user = ''
        for x in save.GetStrArr(system):
            if save.GetInt(f'{x}_{system}_lvl') > bestlvl:
                bestlvl = save.GetInt(f'{x}_{system}_lvl')
                user = x
        return [user, bestlvl]
