from ..Jugs import Jugs

def JUGS(capacity1=None, capacity2=None, UI=False):
    """
        Create and display the jugs game
        
        Parameters
        ----------
        capacity1 : (default value=None) (type=int) Capacity of the first jug
        capacity2 : (default value=None) (type=int) Capacity of the second jug
        UI : (default value=False) (type=boolean) Display the user interface
        
        Functions
        ----------
        fill (c)
        pour(c)
        empty(c)
        obtained()
        
        Use example
        ----------
        >> JUGS(5,7,False)
        
    """
    global jugs
    jugs = Jugs(capacity1=capacity1, capacity2=capacity2, UI=UI, lang='en_EN')
    return jugs
    
def fill(c):
    """
        Fill the jug number c
        
        Parameter
        ----------
        c : (value = 0 or 1) number of the jug
        
        Use example
        ----------
        >> fill(0)
        
    """
    jugs.fill(c)

def pour(c):
    """
        Pour the water of the first jug into the second one
        
        Parameter
        ----------
        c : (value = 0 or 1) number of the jug
        
        Use example
        ----------
        >> pour(1)
        
    """
    jugs.pour(c)

def empty(c):
    """
       Empties the jug number c
       
       Parameter
        ----------
        c : (value = 0 or 1) number of the jug
        
        Use example
        ----------
        >> empty(0)
        
    """
    jugs.empty(c)

def set_volumes(c1,c2):
    """
        Set new capacities to both jugs
        
        Parameters
        ----------
        c1 : (type=int) capacity of the left jug
        c2 : (type=int) capacity of the right jug
        
        Use example
        ----------
        >> set_volumes(5,8)
      
    """
    jugs.set_volumes(c1,c2)

def obtained():
    """
        Returns a list of boolean. The box number i is set to True if the player already got i liters
        
        Use example
        ----------
        >> obtained()
    """
    return jugs.obtained
