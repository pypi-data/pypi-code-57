from ipywidgets_game_maze.Maze import Maze
__version__ = '0.1'
def MAZE(level=0):
    levels={0:'lab/lab.json',1:'lab/laby3d.json'}
    if not(level in levels):
        level=0
    global maze
    maze=Maze(levels[level])
    return maze
    
def move():
    maze.move()

def look():
    return maze.look()

def right():
    maze.right()

def left():
    maze.left()
    
def up():
    maze.up()
    
def down():
    maze.down()
    
def horizontal():
    maze.horizontal()
    
def reset():
    maze.reset()
