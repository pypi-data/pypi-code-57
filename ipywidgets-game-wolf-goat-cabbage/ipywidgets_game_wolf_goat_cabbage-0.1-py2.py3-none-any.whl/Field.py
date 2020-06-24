from .Coast import *
from .Boat import *
__version__ = '0.1'
class Field(object):
    """
        Models the game without any visualisation
        
        Readable attributes
        -----------
        rows : (type=int) number of rows in the game
        columns : (type=int) number of columns in the game
        leftCoast : (type=Coast) the left coast
        rightCoast : (type=Coast) the right coast
        boat : (type=Boat) the boat 
        
    """
    def __init__(self):
        """
            Game initialization
            
            Tests
            -----------
            >>> field=Field()
            >>> field.rows
            5
            >>> field.columns
            10
            >>> field.leftCoast.goat
            True
            >>> field.rightCoast.goat
            False
            >>> field.boat.side
            True
            
        """
        self.__rows=5
        self.__columns=10
        self.__leftCoast= Coast(True)
        self.__rightCoast= Coast(False)
        self.__boat=Boat()


    @property
    def rows(self): return self.__rows

    @property
    def columns(self): return self.__columns

    @property
    def leftCoast(self): return self.__leftCoast
    
    @property
    def rightCoast(self): return self.__rightCoast
    
    @property
    def boat(self): return self.__boat
    

    def board(self, name):
        """
            Board the element name
            
            Parameter
            ----------
            name : (type=string) the element to board
            
            Tests
            ----------
            >>> field=Field()
            >>> field.board('Goat')
            (True, True, True)
            >>> field.boat.first
            'Goat'
            >>> field.leftCoast.goat
            False
            
        """
        assert isinstance (name,str),"name has to be a string"
        if self.__boat.side: #on the left coast
            c1=self.__leftCoast.board(name)
            if c1:  # the Element is on the coast
                c2,side=self.__boat.board(name)
                if not c2: #the boat is full
                    self.__leftCoast.unboard(name)
                    return False,True,side
                else:
                    return True,True,side #(possible,rive,first/second)
            else:
                return False, False, False
        else: # on the right coast
            c1=self.__rightCoast.board(name)
            if c1:  #the element is on the coast
                c2,side=self.__boat.board(name)
                if not c2: #the boat is full
                    self.__rightCoast.unboard(name)
                    return False,False,side
                else:
                    return True,False,side
            else:
                return False, False, False
    
    def unboard (self, name):
        """
            Unboard the element name
            
            Parameter
            ----------
            name : (type=string) the element to 
            
            Tests
            -----------
            >>> field=Field()
            >>> field.unboard('Goat')
            Goat is not on board.
            (False, False, False, False)
            >>> field.board('Cabbage')
            (True, True, True)
            >>> field.unboard('Cabbage')
            (True, True, True, False)
            
        """
        assert isinstance (name,str),"name has to be a string"
        c1,side=self.__boat.unboard(name)
        if c1: #The Element is on board
            if self.__boat.side: # the boat is on the left coast
                self.__leftCoast.unboard(name)
                return True,True,side, False #possible, gauche, first/second
            else: #the boast is on the right coast
                self.__rightCoast.unboard(name)
                if self.__rightCoast.win():
                    return True,False, side, True
                else:
                    return True,False, side, False
        else:
            return False,False,False, False
    
    def cross(self):
        """
            Make the boat cross the river
            
            Tests
            ----------
            >>> field=Field()
            >>> field.boat.side
            True
            >>> field.cross()
            True
            >>> field=Field()
            >>> field.board('Goat')
            (True, True, True)
            >>> field.cross()
            False
            
        """
        self.__boat.cross()
        is_ok=0
        if self.__boat.side:
            #the boast is now on the left coast so we check the right coats
            is_ok=self.__rightCoast.check()
        else:
            is_ok=self.leftCoast.check()
        if is_ok==-1:
            return True
        else:
            return False
