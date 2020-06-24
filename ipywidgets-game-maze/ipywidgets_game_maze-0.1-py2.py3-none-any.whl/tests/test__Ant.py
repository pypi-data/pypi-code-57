from ipywidgets_game_maze.Ant  import Ant
from random import *

def test__init():
    orientations=['N','S','U','D','E','W']
    relative={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
    for i in range(0,20):
        x=randint(0,100)
        y=randint(0,100)
        z=randint(0,100)
        o=randint(0,len(orientations)-1)
        ant=Ant(x,y,z,1,1,1,orientations[o])
        assert (ant.bodyMoves==[x,y,z]),"Initialization problem 1"
        assert(ant.headMoves==[x+relative[orientations[o]]['Head'][0],y+relative[orientations[o]]['Head'][1],z+relative[orientations[o]]['Head'][2]]), "Initialization problem 2"
        assert(ant.tailMoves==[x+relative[orientations[o]]['Tail'][0],y+relative[orientations[o]]['Tail'][1],z+relative[orientations[o]]['Tail'][2]]), "Initialization problem 3"
        assert (ant.orientation==orientations[o]),"Initialization problem 4"
        assert (ant.timing==[0]),"Initialization problem 5"
        
def test__move():
    orientations=['N','S','U','D','E','W']
    moveOriented={'W':(1,0,0),'E':(-1,0,0),'N':(0,0,-1),'S':(0,0,1),'U':(0,1,0),'D':(0,-1,0)}
    for i in range(0,20):
        x=randint(0,100)
        y=randint(0,100)
        z=randint(0,100)
        orient=randint(0,len(orientations)-1)
        ant=Ant(x,y,z,1,1,1,orientations[orient])
        oldBody=ant.bodyMoves
        oldHead=ant.headMoves
        oldTail=ant.tailMoves
        ant.move()
        dxyz=[moveOriented[orientations[orient]][0],moveOriented[orientations[orient]][1],moveOriented[orientations[orient]][2]]
        
        assert len(ant.bodyMoves)==6,"Problem Move 1"
        assert len(ant.headMoves)==6,"Problem Move 2"
        assert len(ant.tailMoves)==6,"Problem Move 3"
        for i in range(0,3):
            assert (round(ant.bodyMoves[3+i],2)==round(oldBody[i]+dxyz[i],2)),"Problem Move 4"
            assert (round(ant.headMoves[3+i],2)==round(oldHead[i]+dxyz[i],2)),"Problem Move 5"
            assert (round(ant.tailMoves[3+i],2)==round(oldTail[i]+dxyz[i],2)),"Problem Move 6"
        
def test__up():
    orientations=['N','S','U','D','E','W']
    o=randint(0,len(orientations)-1)
    ant=Ant(0,0,0,1,1,1,orientations[o])
    ant.up()
    assert ant.bodyMoves[3:6]==[0,0,0],"Problem up 0"
    assert ant.headMoves[3:6]==[0,0.26,0],"Problem up 1"
    assert ant.tailMoves[3:6]==[0,-0.25,0],"Problem up 2"
    assert ant.orientation=="U","Problem up 3"
    
    
def test__down():
    orientations=['N','S','U','D','E','W']
    o=randint(0,len(orientations)-1)
    ant=Ant(0,0,0,1,1,1,orientations[o])
    ant.down()
    assert ant.bodyMoves[3:6]==[0,0,0],"Problem down 0"
    assert ant.headMoves[3:6]==[0,-0.26,0],"Problem down 1"
    assert ant.tailMoves[3:6]==[0,0.25,0],"Problem down 2"
    assert ant.orientation=="D","Problem down 3"
        
        
def test__block():
    orientations=['N','S','U','D','E','W']
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    o=randint(0,len(orientations)-1)
    ant=Ant(x,y,z,1,1,1,orientations[o])
    ant.move()
    oldBody=ant.bodyMoves
    oldHead=ant.headMoves
    oldTail=ant.tailMoves
    ant.block()
    ant.move()
    assert (len(ant.bodyMoves)==6),"Problem block 1"
    assert (len(ant.headMoves)==6), "Problem block 2"
    assert (len(ant.bodyMoves)==6), "Problem block 3"
    assert (oldBody==ant.bodyMoves), "Problem block 4"
    assert (oldHead==ant.headMoves),"Problem block 5"
    assert (oldTail==ant.tailMoves), "Problem block 6"
    
        
def test__position_part():
    orientations=['N','S','U','D','E','W']
    relative={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
    for i in range(0,20):
        orient=orientations[randint(0,len(orientations)-1)]
        x=randint(0,100)
        y=randint(0,100)
        z=randint(0,100)
        ant=Ant(0,0,0,1,1,1,'S')
        dh=[x+relative[orient]['Head'][0],y+relative[orient]['Head'][1],z+relative[orient]['Head'][2]]
        dt=[x+relative[orient]['Tail'][0],y+relative[orient]['Tail'][1],z+relative[orient]['Tail'][2]]
        assert (ant.position_part('Head',orient,x,y,z)==dh),"Problem position_part 1"
        assert (ant.position_part('Tail',orient,x,y,z)==dt),"Problem position_part 2"
        
        
        
def test__turn():
    orientations=['N','S','U','D','E','W']
    relative={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    ant=Ant(x,y,z,1,1,1,'S')
    for i in range(0,20):
        orient=orientations[randint(0,len(orientations)-1)]
        ant.turn(orient)
        lenMoves=len(ant.bodyMoves)
        assert (ant.bodyMoves[lenMoves-3:lenMoves]==[x,y,z]),"Problem turn 1"
        assert (ant.headMoves[lenMoves-3:lenMoves]==[x+relative[orient]['Head'][0],y+relative[orient]['Head'][1],z+relative[orient]['Head'][2]]),"Problem turn 2"
        assert (ant.tailMoves[lenMoves-3:lenMoves]==[x+relative[orient]['Tail'][0],y+relative[orient]['Tail'][1],z+relative[orient]['Tail'][2]]),"Problem turn 3"
        
        
def test__right():
    orientations=['N','S','E','W','U','D']
    relative={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
    newDir={'W':'S','S':'E','E':'N','N':'W','U':'U','D':'D'}
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    orient=orientations[randint(0,len(orientations)-1)]
    ant=Ant(x,y,z,1,1,1,orient)
    ant.right()
    assert (ant.bodyMoves[3:6]==[x,y,z]),"Problem right 1"
    assert (ant.headMoves[3:6]==[x+relative[newDir[orient]]['Head'][0],y+relative[newDir[orient]]['Head'][1],z+relative[newDir[orient]]['Head'][2]]),"Problem right 2"
    assert (ant.tailMoves[3:6]==[x+relative[newDir[orient]]['Tail'][0],y+relative[newDir[orient]]['Tail'][1],z+relative[newDir[orient]]['Tail'][2]]),"Problem right 3"  

    
def test__left():
    orientations=['N','S','E','W','U','D']
    relative={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
    newDir={'W':'N','N':'E','E':'S','S':'W','U':'U','D':'D'}
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    orient=orientations[randint(0,len(orientations)-1)]
    ant=Ant(x,y,z,1,1,1,orient)
    ant.left()
    assert (ant.bodyMoves[3:6]==[x,y,z]),"Problem left 1"
    assert (ant.headMoves[3:6]==[x+relative[newDir[orient]]['Head'][0],y+relative[newDir[orient]]['Head'][1],z+relative[newDir[orient]]['Head'][2]]),"Problem left 2"
    assert (ant.tailMoves[3:6]==[x+relative[newDir[orient]]['Tail'][0],y+relative[newDir[orient]]['Tail'][1],z+relative[newDir[orient]]['Tail'][2]]),"Problem left 3"  
              
        
        
def test_horizontal():
    orientations=['N','S','E','W','U','D']
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    orient=orientations[randint(0,len(orientations)-1)]
    ant=Ant(x,y,z,1,1,1,orient)
    oldBody=ant.bodyMoves
    oldHead=ant.headMoves
    oldTail=ant.tailMoves
    ant.up()
    ant.down()
    ant.horizontal()
    lenMoves=len(ant.bodyMoves)
    assert(ant.bodyMoves[lenMoves-3:lenMoves]==oldBody[0:3]), "Problem horizontal 1"
    assert(ant.headMoves[lenMoves-3:lenMoves]==oldHead[0:3]), "Problem horizontal 2"
    assert(ant.tailMoves[lenMoves-3:lenMoves]==oldTail[0:3]), "Problem horizontal 3"
    
        
def test__removeMove():
    orientations=['N','S','E','W','U','D']
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    orient=orientations[randint(0,len(orientations)-1)]
    ant=Ant(x,y,z,1,1,1,orient)
    oldBody=ant.bodyMoves
    oldHead=ant.headMoves
    oldTail=ant.tailMoves
    ant.move()
    ant.removeMove()
    lenMoves=len(ant.bodyMoves)
    assert (len(ant.bodyMoves)==3), "Problem removeMove 1"
    assert (len(ant.bodyMoves)==3), "Problem removeMove 2"
    assert (len(ant.bodyMoves)==3), "Problem removeMove 3"
    assert (len(ant.timing)==1), "Problem removeMove 4"
    assert(ant.bodyMoves[lenMoves-3:lenMoves]==oldBody[0:3]), "Problem removeMove 5"
    assert(ant.headMoves[lenMoves-3:lenMoves]==oldHead[0:3]), "Problem removeMove 6"
    assert(ant.tailMoves[lenMoves-3:lenMoves]==oldTail[0:3]), "Problem removeMove 7"
    assert (ant.timing==[0]), "Problem removeMove 8"
        
        
        
def test_resetMoves():
    orientations=['N','S','E','W','U','D']
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    orient=orientations[randint(0,len(orientations)-1)]
    ant=Ant(x,y,z,1,1,1,orient)
    oldBody=ant.bodyMoves[0:3]
    oldHead=ant.headMoves[0:3]
    oldTail=ant.tailMoves[0:3]
    ant.move()
    ant.right()
    ant.move()
    ant.right()
    ant.resetMoves()
    assert (len(ant.bodyMoves)==3),"Problem resetMoves 1"
    assert (len(ant.headMoves)==3),"Problem resetMoves 2"
    assert (len(ant.tailMoves)==3),"Problem resetMoves 3"
    assert (len(ant.timing)==1),"Problem resetMoves 4"
    assert (ant.bodyMoves==oldBody),"Problem resetMoves 5"
    assert (ant.headMoves==oldHead),"Problem resetMoves 6"
    assert (ant.tailMoves==oldTail),"Problem resetMoves 7"
    assert (ant.timing==[0]),"Problem resetMoves 8"
    assert (ant.orientation==orient), "Problem resetMoves 9"


        
        
        
        
        
        