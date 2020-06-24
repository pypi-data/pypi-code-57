import time,os,pickle

FILENAME = "pacing_and_leading.save"

class LogItem:

    __slots__=("time","cursor","soft_target",
               "hard_target","similarity")
    
    def __init__(self,t,cursor,
                 soft_target,hard_target,
                 similarity):
        self.time = t
        self.cursor = cursor
        self.soft_target = soft_target
        self.hard_target = hard_target
        self.similarity = similarity

class Log:

    def __init__(self):
        self.data = []

    def set(self,t,cursor,soft_target,
            hard_target,similarity):
        self.data.append(LogItem(t,
                                 cursor,
                                 soft_target,
                                 hard_target,
                                 similarity))


    def save(self,file_path=None):
        if file_path is None:
            file_path = os.getcwd()+os.sep+FILENAME
        with open(file_path,"wb") as f:
            pickle.dump(self,f)
        return file_path
        
    @classmethod
    def load(cls,file_path=None):
        if file_path is None:
            file_path = os.getcwd()+os.sep+FILENAME
        with open(file_path,"rb") as f:
            instance = pickle.load(f)
        return instance
        
        
