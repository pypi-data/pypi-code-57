'''
This Module includes rx7_object.
This object exists in rx7 module so I recommend to use  rx7.RX7_obj  
instead of  rx7.rx_obj.RX7_obj  to ease.
'''
############################################
#############  RX7 OBJECT  #################
############################################
class RX7_obj:
    '''
    This class creates an Iterable that can only contains string.  
    You Can Lock this object (with self.lock() method) 
    which means you can not add remove or set item to it 
    (Usually we use these things in game developing).  
    When Object is locked you can not delete it.  
    Using forbidden methods when object is locked cause LockError 
    and you need to use self.unlock() to unlock.  
    Also RX7_obj include other iterable features like __add__,__sub__,__getitem__,__setitem__,etc.  
    + Custom Representing.
    '''
#######################
#####  Existence  #####
#######################
    def __init__(self,*var):
        for item in var:
            if type(item)!=str:
                raise TypeError
        self.name= self
        self.__MAIN=list(var)
        self.ND= set(var)
        self.__LOCK= False
        self.lock_error= False
        #import sys
        #self.__size= sys.getsizeof(self)
    def __str__(self):
        return '<'+','.join(self.__MAIN)+'>'
    def __repr__ (self):
        #if not self.__LOCK:
            return '<'+','.join(self.__MAIN)+'>'
        #else:
        #    raise self.LockError('Object is Locked. Content Is Protected.')
########################
########  LOCK  ########
########################
    class LockError(Exception):
        def __init__(self, message='Object is Locked. Use Object.unlock() to unlock it.'):
            super().__init__(message)
    def lock(self):
        '''Lock the object.  
        In Locked mode you can not add,remove or delete object.'''
        self.__LOCK= True
    def unlock(self):
        '''Unlock the object so you can add or remove sth and delete the object'''
        self.__LOCK= False
######  LUCKABLE  ######
    def add(self,var):
        '''Add var to the object.  
        raise LockError if object is locked.'''
        if not self.__LOCK:
            self.__MAIN.append(var)
            self.ND= set(self.__MAIN)
        else:
            if self.lock_error:
                raise self.LockError
    def remove(self,*var,warning=False,Break=False):
        '''Removes var from the object.  
        raise LockError if object is locked.'''
        if not self.__LOCK:
            if Break:
                for th in [v for v in var]:
                    if th in self.__MAIN:
                        self.__MAIN.remove(th)
                    else:
                        raise ValueError
            elif warning:
                for th in [v for v in var]:
                    if th in self.__MAIN:
                        self.__MAIN.remove(th)
                    else:
                        print(f'WARNING:  {th} Not in {self}')
            else:
                for th in [v for v in var if v in self.__MAIN]:
                    self.__MAIN.remove(th)
            self.ND= set(self.__MAIN)
        else:
            if self.lock_error:
                raise self.LockError

    def __setitem__(self,index,value):
        if not self.__LOCK:
            if type(value)==str:
                self.__MAIN[index]=value
                self.ND= set(self.__MAIN)
            else:
                raise TypeError
        else:
            if self.lock_error:
                raise self.LockError
    
    def __del__(self):
        '''This will raise LockError if object is locked.
           EVEN IF lock_error IS FALSE'''
        if self.__LOCK:
            raise self.LockError        
######################
######################
    def __add__(self,other,duplicate=True):
        if not self.__LOCK:
            NEW= RX7_obj(self.__MAIN[0]) 
            for item in self.__MAIN[1:len(self.__MAIN)]:
                NEW.add(item)
            for item in other.__MAIN:
                NEW.add(item)
            if not duplicate:
                NEW.__MAIN=list(set(NEW.__MAIN))
            return NEW
        else:
            if self.lock_error:
                raise self.LockError            
    def __sub__(self,other):
        if not self.__LOCK:
            for item in self.__MAIN:
                if item not in other.__MAIN:
                    NEW= RX7_obj(item)
                    break
            for item in self.__MAIN:
                if item not in other.__MAIN:
                    NEW.add(item)
            NEW.remove(NEW[0])
            return NEW
        else:
            if self.lock_error:
                raise self.LockError
    def __len__(self):
        return len(self.__MAIN)
    def __getitem__(self,index):
        return self.__MAIN[index]
    def __bool__(self):
        bool(len(self.__MAIN))
    '''def __call__(self):
        if not self.__LOCK:'''
    def __sizeof__(self):
        return (self.__MAIN.__sizeof__(),self.ND.__sizeof__()) #self.__size,
