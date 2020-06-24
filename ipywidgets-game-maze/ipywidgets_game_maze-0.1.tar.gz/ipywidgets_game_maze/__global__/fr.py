from ipywidgets_game_maze.Maze import Maze
__version__ = '0.1'
def LABY3D(niveau=0):
    niveaux={0:'lab/lab.json',1:'lab/laby3d.json'}
    if not(niveau in niveaux):
        niveau=0
    global lab
    lab=Maze(niveaux[niveau],'fr_FR')
    return lab
    
def avancer():
    lab.move()

def regarder():
    return lab.look()

def droite():
    lab.right()

def gauche():
    lab.left()
    
def haut():
    lab.up()
    
def bas():
    lab.down()
    
def horizontale():
    lab.horizontal()
    
def restart():
    lab.reset()