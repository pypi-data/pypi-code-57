global translation
translation={'en_EN':{'Goat':'Goat','Wolf':'Wolf','Cabbage':'Cabbage','Full':'The boat is full, you have to unboard something first','strType':'name has to be a string', 'NotonBoard':' is not on board.'},
            'fr_FR':{'Goat':'Chèvre','Wolf':'Loup','Cabbage':'Chou','Full':"Le bateau est plein, il faut faire descendre quelque chose d'abord",'strType':'name doit être un string', 'NotonBoard':" n'est pas à bord."}}
__version__ = '0.1'
class Boat(object):
    """
        Models a boat with with two spare box 
    """
    def __init__(self, lang='en_EN'):
        """
            Initialize the Boat
            
            Parameter
            ----------
            lang : (default value='en_EN') (type=string) Game's language
            
            Tests
            ----------
            >>> boat=Boat()
            >>> boat.first
            >>> boat.second
            >>> boat.side
            True
            
        """
        self.__first=None
        self.__second=None
        self.__side=True #Gauche
        if lang in translation:
            self.__language=lang
        else:
            self.__language='en_EN'

    @property
    def first (self): return self.__first

    @property
    def second(self): return self.__second
    
    @property
    def side(self): return self.__side

    def board(self, name):
        """
            Returns two booleans : b1 and b2
            b1==True if there is a free box (name has been board)
            b2==True if name is in the first box, False otherwise
            
            Parameter
            -----------
            name : (type=string) name of the element to board
            
            Tests
            ----------
            >>> boat=Boat()
            >>> boat.board('Goat')
            (True, True)
            >>> boat.first
            'Goat'
            >>> boat.second
            >>> boat.board('Wolf')
            (True, False)
            >>> boat.first
            'Goat'
            >>> boat.second
            'Wolf'
            >>> boat.board('Cabbage')
            The boat is full, you have to unboard something first
            (False, False)
            
        """
        assert isinstance (name,str),translation[self.__language]['strType']
        if (name in ["Goat", "Wolf", "Cabbage"]):
            if (self.__first==None):
                self.__first=name
                return True,True #possible,first
            elif(self.__second==None):
                self.__second=name
                return True,False #possible, second
            else:
                print(translation[self.__language]['Full'])
                return False,False
        else:
            print(name+" does not exist in this game. \n Choose among those names : \n 'Goat' \n 'Wolf' \n 'Cabbage'")
            return False,False
            
            
    def unboard(self, name):
        """
            Returns two booleans : b1 and b2
            b1==True if name is on board and therefore can be unboard
            b2==True if name is in the first box, False otherwise
            
            Parameter
            -----------
            name : (type=string) name of the element to unboard
            
            Tests
            ----------
            >>> boat=Boat()
            >>> boat.board('Goat')
            (True, True)
            >>> boat.board('Wolf')
            (True, False)
            >>> boat.first
            'Goat'
            >>> boat.second
            'Wolf'
            >>> boat.unboard('Cabbage')
            Cabbage is not on board.
            (False, False)
            >>> boat.unboard('Goat')
            (True, True)
            >>> boat.unboard('Wolf')
            (True, False)
            
        """
        assert isinstance (name,str),translation[self.__language]['strType']
        if(self.__first!=None and self.__first==name):
            self.__first=None
            return True,True #possible, first
        elif(self.__second!=None and self.__second==name):
            self.__second=None
            return True,False #possible, second
        else:
            if (name in ["Goat", "Wolf", "Cabbage"]):
                print(name+translation[self.__language]['NotonBoard'])
            else:
                print(name+" does not exist in this game. \n Choose among those names : \n 'Goat' \n 'Wolf' \n 'Cabbage'")
            return False,False
    
    def cross(self):
        """
            Make the Boat change side (goes to the other coast)
            
            Test
            ----------
            >>> boat=Boat()
            >>> boat.side
            True
            >>> boat.cross()
            >>> boat.side
            False
            
        """
        self.__side= not self.__side