class SingleJug :
    """ Class modeling a single jug 
        
        Readable attributes
        ----------
        capacity : (type=int) maximum volume the jug may contain
        volume : (type=int) the actual volume of water the jug contains
    """
    def __init__(self, capacity):
        """ Initialization of the jug
            
            Parameter
            ----------
            capacity : (type=int) capacity of the jug
            
            Tests
            ----------
            >>> s=SingleJug(5)
            >>> s.capacity
            5
            >>> s.volume
            0
            
        """
        assert isinstance(capacity,int), "capacity has to be an int"
        self.__capacity= capacity
        self.__volume= 0
    
    @property
    def capacity (self): return self.__capacity
    
    @property
    def volume (self): return self.__volume
    
    def modify(self, newContent):
        """ Change the capacity of the jug
        
            Parameter
            ----------
            newContent : (type: int) new capacity of the jug
            
            Tests
            ----------
            >>> s=SingleJug(7)
            >>> s.modify(3)
            >>> s.capacity
            3
            
        """
        self.__capacity= int(newContent)
        self.__volume= 0
    
    def set_volume(self, vol):
        """ Set the volume contained : necessary for test
            
            Parameter
            ----------
            vol : (type=int) new volume of water contained in the jug
            
            Tests
            ----------
            >>> s=SingleJug(7)
            >>> s.volume
            0
            >>> s.set_volume(4)
            >>> s.volume
            4
            
        """
        self.__volume=vol
    
    
    def empty (self):
        """ Empty the jug 
            
            Tests
            ----------
            >>> s=SingleJug(7)
            >>> s.set_volume(5)
            >>> s.volume
            5
            >>> s.empty()
            >>> s.volume
            0
            
        """
        self.__volume=0
    
    
    def pour(self, secondJug):
        """ Pour the water of the jug into the given one
        
            Parameter
            ----------
            secondJug : (type=SingleJug) the jug we want to pour the water into
            
            Tests
            ----------
            >>> s=SingleJug(7)
            >>> s2=SingleJug(5)
            >>> s.set_volume(6)
            >>> s.pour(s2)
            >>> s.volume
            1
            >>> s2.volume
            5
            
        """
        toPour=min(secondJug.capacity - secondJug.volume, self.__volume)
        self.__volume-=toPour
        secondJug.fill(toPour)
    
    def fill(self, vol=None):
        """ Fill the jug to the top or had a given amount of water
            
            Parameter
            ----------
            vol : (default value =None) (type=int) the volume of water to add
            
            Tests
            ----------
            >>> s=SingleJug(7)
            >>> s.volume
            0
            >>> s.fill()
            >>> s.volume
            7
            >>> s.empty()
            >>> s.fill(3)
            >>> s.volume
            3
            
        """
        if vol==None:
            vol=self.__capacity - self.__volume
        if self.__volume+vol > self.__capacity :
            print("Over the capacity")
        else:
            self.__volume+=vol
