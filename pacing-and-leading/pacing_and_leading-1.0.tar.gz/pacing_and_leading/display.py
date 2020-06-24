import copy

class _Circle:

    def __init__(self,name,position,size,color,x_shift=0):
        self.name = name
        self.position = copy.deepcopy(position)
        self.size = copy.deepcopy(size)
        self.color = copy.deepcopy(color)
        self.x_shift = x_shift

    def __str__(self):
        return str(self.name)+"\t"+str(self.position)
        

class _VerticalLine(_Circle):

    def __init__(self,name,position,size,color):

        _Circle.__init__(name,position,size,color)


class _Arrow:

    def __init__(self,
                 name,
                 position,
                 delta,
                 color,
                 length,
                 width,
                 tip_size):

        self.name = name
        self.position = position
        self.delta = delta
        self.color = color
        self.width = width
        self.tip_size = tip_size
        self.length = length
        
class Circle :

    """ generic class for all moving circles in the world
        
    Args:      
    update_function : compute the position, size and color
    of the circle depending of the current state of the world,
    e.g. position of the user's cursor
    """
    
    def __init__(self,
                 name,
                 update_function,
                 init_position=[0,0]):

        self._name = name
        self._position = init_position
        self._size = None 
        self._color = None # None means transparent
        self._update_function = update_function
        self._x_shift=0
        
    def __str__(self):
        return str(self._name)+":\t"+str(self._position)
        
    def get_position(self):
        
        return copy.deepcopy(self._position)

    def get(self):

        return _Circle(self._name,
                       self._position,
                       self._size,
                       self._color,
                       x_shift=self._x_shift)
    
    def update(self,world):

        values = self._update_function(world)
        try:
            self._position,self._size,self._color,self._x_shift = values
        except:
            self._position,self._size,self._color = values
    

class VerticalLine(Circle) :

    """ generic class for all moving circles in the world
        
    Args:      
    update_function : compute the position, size and color
    of the circle depending of the current state of the world,
    e.g. position of the user's cursor
    """
    
    def __init__(self,
                 name,
                 vertical_target,
                 init_position=[0,0]):

        Circle.__init__(self,
                        name,
                        vertical_target,
                        vertical_target.get_position())
        self._vertical_target = vertical_target
        
    def get_source(self):
        
        return self._vertical_target
        
    def update(self,world):

        self._position,self._size,self._color = self._update_function(world)


class Arrow:

    def __init__(self,
                 name,
                 length,
                 width,
                 tip_size,
                 update_function):

        self._name = name
        self._update_function = update_function
        self._position = (0,0)
        self._delta = (0,0)
        self._color = None
        self._width = width
        self._tip_size = tip_size
        self._length = length
        
    def get(self):

        return _Arrow(self._name,
                      self._position,
                      self._delta,
                      self._color,
                      self._length,
                      self._width,
                      self._tip_size)
        
    def update(self,world):

        self._position,self._delta,self._color = self._update_function(world)

    
