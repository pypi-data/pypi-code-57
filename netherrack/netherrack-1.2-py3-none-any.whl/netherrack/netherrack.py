import pprint
import requests
import base64
import json
import gzip

res = requests.get("https://raw.githubusercontent.com/EnjoyYourBan/enjoyyourban.github.io/master/actions.json")
actions = res.json()

class Target:
    def __init__(self, line):
        self.line = line
    
    def target(self, playerTarget):
        self.line.code['blocks'][-1]['target'] = playerTarget

class Not:
    def __init__(self, line):
        self.line = line
    
    def _not(self):
        self.line.code['blocks'][-1]['inverted'] = "NOT"

class Close:
    def __init__(self, line):
        self.line = line
    
    def _else(self):
        self.line.code['blocks'].append({"id":"block","block":"else"})
        self.line.code['blocks'].append({"id":"bracket","direct":"open","type":"norm"})

class Variable:
    def __init__(self, name, varType="unsaved"):
        self.name = name
        self.varType = varType
        self.value = 0
    
    def compile(self):
        return {"item":{"id":"var","data":{"name":self.name,"scope": self.varType}}, "slot":0}

class Text:
    def __init__(self, value):
        self.value = value
    
    def compile(self):
        return {"item": {"id": "txt", "data": {"name": self.value}}, "slot": 0}

class Num:
    def __init__(self, value):
        self.value = value
    
    def compile(self):
        return {"item": {"id": "num", "data": {"name": self.value}}, "slot": 0}

class Location:
    def __init__(self, x, y=0, z=0, pitch=0, yaw=0):
        self.x, self.y, self.z, self.pitch, self.yaw = x, y, z, pitch, yaw
    
    def compile(self):
        return {"item": {"id": "loc", "data": {"loc": {
            "x": self.x, "y": self.y, "z": self.z, "pitch": self.pitch, "yaw": self.yaw
        }, "isBlock": False}}, "slot": 0}

class GameValue:
    def __init__(self, value, valTarget="Default"):
        self.value = value
        self._target = valTarget
    
    def target(self, valTarget="Default"):
        self._target = valTarget
    
    def compile(self):
        return {"item":{"id":"g_val","data":{"type": self.value,"target": self._target}},"slot":0}

class Particle:
    def __init__(self, particle):
        self.particle = particle
    
    def compile(self):
        return {"item":{"id":"part","data":{"particle":self.particle,"count":1,"speed":0,"dx":0,"dy":0,"dz":0}},"slot":0}

class Potion:
    def __init__(self, effect, length, amplifier=1):
        self.effect, self.length, self.amplifier = effect, length, amplifier
    
    def compile(self):
        return {"item":{"id":"pot","data":{"pot":self.effect,"dur":self.length,"amp":self.amplifier}},"slot":0}

class Sound:
    def __init__(self, noise, pitch=1, vol=1):
        self.noise, self.pitch, self.vol = noise, pitch, vol
    
    def compile(self):
        return {"item":{"id":"snd","data":{"sound": self.noise,"pitch": self.pitch,"vol": self.vol}},"slot":0}

class Line:
    def __init__(self, eventType, eventName):
        if eventType not in ("func", "process"):
            self.code = {"blocks": [
                {"block": eventType, "id": "block", "args": {"items": []}, "action": eventName}
            ]}
        else:
            self.code = {"blocks":[{"id":"block","block":eventType,"args":{"items":[{"item":{"id":"bl_tag","data":{"option":"False","tag":"Is Hidden","action":"dynamic","block":eventType}},"slot":26}]},"data":eventName}]}
        
        self.target = "None"
        self.brackets = []
    
    def callFunc(self, function):
        self.code['blocks'].append({"id":"block","block":"call_func","args":{"items":[]},"data":function})
    
    def callProc(self, process):
        self.code['blocks'].append({"id":"block","block":"start_process","args":{"items":[{"item":{"id":"bl_tag","data":{"option":"Create new storage","tag":"Local Variables","action":"dynamic","block":"start_process"}},"slot":25},{"item":{"id":"bl_tag","data":{"option":"With current targets","tag":"Target Mode","action":"dynamic","block":"start_process"}},"slot":26}]},"data":process})

    def control(self, action, *items):
        try:
            tags = actions[action]['tags']
        except:
            pass

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26
        
        for tag in tags:
            formatted.append({"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "block": "control"}},
                "slot": index
            })

            index -= 1
        
        self.code['blocks'].append({"block": "control", "id": "block", "args": {
            "items": formatted
        }, "action": action})

        return Target(self)
    
    def selectObj(self, action, subaction="abc", *items):
        try:
            tags = actions[action]['tags']
        except:
            pass

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26
        
        for tag in tags:
            formatted.append({"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "subAction": subaction, "block": "select_obj"}},
                "slot": index
            })

            index -= 1
        
        self.code['blocks'].append({"block": "select_obj", "id": "block", "args": {
            "items": formatted
        }, "action": action, "subaction": subaction})

        return Target(self)

    def entityAction(self, action, *items):
        try:
            tags = actions[action]['tags']
        except:
            tags = []

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26
        
        for tag in tags:
            formatted.append({"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "block": "entity_action"}},
                "slot": index
            })

            index -= 1
        
        self.code['blocks'].append({"block": "entity_action", "id": "block", "args": {
            "items": formatted
        }, "action": action})

        return Target(self)

    def gameAction(self, action, *items):
        try:
            tags = actions[action]['tags']
        except:
            tags = []

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26
        
        for tag in tags:
            formatted.append({"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "block": "game_action"}},
                "slot": index
            })

            index -= 1
        
        self.code['blocks'].append({"block": "game_action", "id": "block", "args": {
            "items": formatted
        }, "action": action})

        return Target(self)
    
    def playerAction(self, action, *items):
        tags = actions[action]['tags']

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26
        
        for tag in tags:
            formatted.append({"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "block": "player_action"}},
                "slot": index
            })

            index -= 1
        
        self.code['blocks'].append({"block": "player_action", "id": "block", "args": {
            "items": formatted
        }, "action": action})

        return Target(self)
    
    def setVar(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "set_var", "id": "block", "args": {
            "items": formatted
        }, "action": action})

        return Target(self)
    
    ## IFs
    def close(self):
        if self.brackets != []:
            if self.brackets[-1] == 'normal':
                bType = 'norm'
            else:
                bType = 'repeat'

            self.code['blocks'].append({"id":"bracket","type":bType,"direct":"close"})
            self.brackets.pop(-1)
        else:
            raise Exception("no bracket to close")

        return Close(self)
    
    def ifEntity(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "if_entity", "id": "block", "args": {
            "items": formatted
        }, "action": action})
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)
    
    def ifGame(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "if_game", "id": "block", "args": {
            "items": formatted
        }, "action": action})
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)

    def ifPlayer(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "if_player", "id": "block", "args": {
            "items": formatted
        }, "action": action})
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)

    def ifVar(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "if_var", "id": "block", "args": {
            "items": formatted
        }, "action": action})
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)
    
    def repeat(self, action, *items):
        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        self.code['blocks'].append({"block": "repeat", "id": "block", "args": {
            "items": formatted
        }, "action": action})
        self.code['blocks'].append({"id":"bracket","type":"repeat","direct":"open"})
        self.brackets.append("special")

        return Target(self)
    
    def build(self):
        if self.brackets != []:
            raise Exception("grr u didnt close the brackets")

        jsonCode = json.dumps(self.code)

        g = gzip.compress(bytes(jsonCode, 'utf-8'))

        encryptCode = base64.b64encode(g)
        encryptCode = str(encryptCode, 'utf-8')
        
        commandCode = '''
        /give @p minecraft:ender_chest{PublicBukkitValues:{"hypercube:codetemplatedata":'{"author":"Netherrack","name":"Netherrack Template","version":1,"code":"'''+encryptCode+'''"}'},display:{Name:'{"text":"Netherrack Template"}'}}
        '''

        return commandCode, jsonCode, encryptCode