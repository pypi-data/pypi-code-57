__version__ = '0.1'
class Coast(object):
    """
        Models a coast capable of hosting a goat, a wolf and a cabbage
    """
    def __init__(self, occupied):
        """
            Initialize the coast
            
            Parameter
            -----------
            occupied : (type=Boolean) whether the coast is initialized full or empty
            
            Tests
            ----------
            >>> coast=Coast(True)
            >>> coast.goat
            True
            >>> coast.wolf
            True
            >>> coast.cabbage
            True
            >>> coast=Coast(False)
            >>> coast.goat
            False
            >>> coast.wolf
            False
            >>> coast.cabbage
            False
            
        """
        self.__goat=occupied
        self.__wolf=occupied
        self.__cabbage=occupied

    @property
    def goat(self): return self.__goat

    @property
    def cabbage(self): return self.__cabbage

    @property
    def wolf(self): return self.__wolf

    def check(self):
        """
            Returns -1 if the goat is left alone with the cabbage or the wolf, returns 1 otherwise
            
            Tests
            ----------
            >>> coast=Coast(True)
            >>> coast.check()
            -1
            >>> coast=Coast(False)
            >>> coast.check()
            1
            
        """
        if ((self.__goat and self.__cabbage) or (self.__goat and self.__wolf)):
            return -1
        else:
            return 1
    
    def win(self):
        """
            Returns True if all elements (goat, cabbage and wolf) are on the coast
            Tests
            ----------
            >>> coast=Coast(True)
            >>> coast.win()
            True
            >>> coast=Coast(False)
            >>> coast.win()
            False
            
        """
        if self.__goat and self.__wolf and self.__cabbage:
            return True
        else:
            return False

    def board(self, name):
        """
            Remove the element name of the coast if it is on it and returns True, it returns False otherwise
            
            Parameter
            -----------
            name : (type=string) name of the element to remove
            
            Tests
            ----------
            >>> coast=Coast(True)
            >>> coast.goat
            True
            >>> coast.wolf
            True
            >>> coast.cabbage
            True
            >>> coast.board('Goat')
            True
            >>> coast.goat
            False
            >>> coast=Coast(False)
            >>> coast.board('Wolf')
            There isn't any wolf on this coast
            False
            
        """
        assert isinstance (name,str),"name has to be a string"
        if name=="Goat":
            if self.__goat:
                self.__goat= False
                return True
            else:
                print("There isn't any goat on this coast")
                return False
        elif name=="Wolf":
            if self.__wolf:
                self.__wolf= False
                return True
            else:
                print("There isn't any wolf on this coast")
                return False
        elif name=="Cabbage":
            if self.__cabbage:
                self.__cabbage= False
                return True
            else:
                print("There isn't any cabbage on this coast")
                return False
        else:
            print(name+" does not exist in this game. \n Choose among those names : \n Goat \n Wolf \n Cabbage")

    def unboard(self, name):
        """
            Set the element name to True
            
            Parameter
            ----------
            name : (type=string) name of the element to add
            
            Tests
            ----------
            >>> coast=Coast(False)
            >>> coast.wolf
            False
            >>> coast.unboard('Wolf')
            >>> coast.wolf
            True
            
        """
        assert isinstance (name,str),"name has to be a string"
        if name=="Goat":
            self.__goat= True
        elif name=="Wolf":
            self.__wolf= True
        elif name=="Cabbage":
            self.__cabbage= True
        else:
            print(name+" does not exist in this game. \n Choose among those names : \n Goat \n Wolf \n Cabbage")
