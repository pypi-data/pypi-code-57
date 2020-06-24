from ipywidgets_game_wolf_goat_cabbage.Grid import Grid
__version__ = '0.1'

def GAME(UI=True):
    """
        Launch and display the game Goat-Wolf-Cabbage
        
        Parameter
        ----------
        UI : (default value=True) (type=boolean) True to display the buttons
        
        Functions
        -----------
        board(name)
        unboard(name)
        reset()
        cross()
        
        Use Example
        -----------
        >> GAME(UI=False)
        
    """
    global game
    game=Grid(UI=UI, lang='en_EN')
    return game
    
def board(element):
    """
        Board element
        
        Parameter
        ----------
        element : (type=string) the element to board. It has to belong to : \n 'Goat' \n 'Wolf' \n 'Cabbage'
        
        Use Example
        -----------
        >> board('Cabbage')
        
    """
    game.board(element)
    
def unboard(element):
    """
        Unboard element
        
        Parameter
        ----------
        element : (type=string) the element to unboard. It has to belong to : \n 'Goat' \n 'Wolf' \n 'Cabbage'
        
        Use Example
        -----------
        >> unboard('Wolf')
        
    """
    game.unboard(element)
    
def reset():
    """
        Reset the game
        
        Use Example
        -----------
        >> reset()
        
    """
    game.reset()    
    
def cross():
    """
        Make the boat cross the river
        
        Use Example
        -----------
        >> cross()
        
    """
    game.cross()    
    