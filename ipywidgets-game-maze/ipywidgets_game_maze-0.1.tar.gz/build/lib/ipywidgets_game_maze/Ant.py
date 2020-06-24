from pythreejs import *
import os
from .Object3D import Object3D
from ipywidgets import Image
__version__ = '0.1'
class Ant(Object3D):
    """
        This class models the ant inside the Maze.
        It inherits from the class Object3D
        
        Readable attributes
        ----------
        bodyMoves : (type=List(int)) List of coordonates of the ant's body. Let (X(k),Y(k),Z(k)) the coordonates of the ant on step k :
                    X(k)=bodyMoves[k*3] ; Y(k)=bodyMoves[k*3+1] ; Z(k)=bodyMoves[k*3+2]
        headMoves : (type=List(int)) List of coordonates of the ant's head
        tailMoves : (type=List(int)) List of coordonates of the ant's tail
        timing : (type=List(int)) List of time steps of each coordonates
        actionT : (type=AnimationAction) Head's animation
        actionC : (type=AnimationAction) Body's animation
        actionQ : (type=AnimationAction) Tail's animation
        orientation : (type=string) The direction the ant is facing
        authorizedMove : (type=boolean) False if moves are unabled
        
    """
    def __init__(self,x,y,z,w,h,d,orientation='W'):
        """
            Initialization of the ant
            
            Parameters
            ----------
            x : (type=int or float) x coordonate at start
            y : (type=int or float) y coordonate at start
            z : (type=int or float) z coordonate at start
            w : (type=int) theorical width as an Object3D (an Object3D is seen as a cube)
            h : (type=int) theorical height as an Object3D (an Object3D is seen as a cube)
            d : (type=int) theorical deepth as an Object3D (an Object3D is seen as a cube)
            orientation : (default value='W') (type=string) orientation of the ant at start
            
            Test
            ----------
            >>> ant=Ant(0,0,0,1,1,1,'S')
            >>> ant.bodyMoves
            [0, 0, 0]
            >>> ant.headMoves
            [0, 0, 0.26]
            >>> ant.tailMoves
            [0, 0, -0.25]
            >>> ant.timing
            [0]
            >>> ant.orientation
            'S'
            
        """
        assert (isinstance(x,float) or isinstance(x,int)), "x has to be a float or an int"
        assert (isinstance(y,float) or isinstance(y,int)), "y has to be a float or an int"
        assert (isinstance(z,float) or isinstance(z,int)), "z has to be a float or an int"
        assert (isinstance(w,int)), "w has to be an int"
        assert (isinstance(h,int)), "h has to be an int"
        assert (isinstance(d,int)), "d has to be an int"
        assert isinstance(orientation,str), "orientation has to be a string"
        assert (orientation in ['N','S','U','D','E','W']), "orientation has to belong to ['N','S','U','D','E','W']"
        # Initialization as an Object3D
        super().__init__ (x=x,y=y,z=z,w=w,h=h,d=d,colour='blue')
        # Relative position of the ant's head and tail to the body
        self.__relativePositions={'W':{'Head':(0.26,0,0),'Tail':(-0.25,0,0)},
                             'E':{'Head':(-0.26,0,0),'Tail':(0.25,0,0)},
                             'N':{'Head':(0,0,-0.26),'Tail':(0,0,0.25)},
                             'S':{'Head':(0,0,0.26),'Tail':(0,0,-0.25)},
                             'U':{'Head':(0,0.26,0),'Tail':(0,-0.25,0)},
                             'D':{'Head':(0,-0.26,0),'Tail':(0,0.25,0)}}
        # New orientation of the ant according to its previous orientation and the side it turns
        self.__orientationTurn={'D':{'W':'S','S':'E','E':'N','N':'W','U':'U','D':'D'},
                               'G':{'W':'N','N':'E','E':'S','S':'W','U':'U','D':'D'}
                               }
        self.__orientation=orientation
        self.__initialOrientation=orientation
        self.__lastHorizontalOrientation=orientation
        # How to modify the ant's coordonates according to its orientation
        self.__moveOriented={'W':(1,0,0),
                            'E':(-1,0,0),
                            'N':(0,0,-1),
                            'S':(0,0,1),
                            'U':(0,1,0),
                            'D':(0,-1,0)}
        # Moves : Body, Head and Tail
        self.__bodyMoves=[x,y,z]
        self.__headMoves=[x+self.__relativePositions[orientation]['Head'][0],y+self.__relativePositions[orientation]['Head'][1],z+self.__relativePositions[orientation]['Head'][2]]
        self.__tailMoves=[x+self.__relativePositions[orientation]['Tail'][0],y+self.__relativePositions[orientation]['Tail'][1],z+self.__relativePositions[orientation]['Tail'][2]]
        
        # textures
        link = '/nbextensions/ipywidgets_game_maze/tete3.jpg'
        #link = os.path.dirname(__file__)+'/images/tete3.jpg'
        head_tex = ImageTexture(imageUri=link)
        matHead=MeshPhysicalMaterial(map=head_tex)
        
        link2 = "/nbextensions/ipywidgets_game_maze/seville.jpg"
        #link2 = os.path.dirname(__file__)+"/images/seville.jpg"
        body_tex = ImageTexture(imageUri=link2)
        matbody=MeshPhysicalMaterial(map=body_tex)
        #head
        self.head=Mesh(
           geometry=SphereBufferGeometry(radius=0.1),
            material=matHead,
            position=self.__headMoves
        )
        #self.head=Mesh(
        #    geometry=SphereBufferGeometry(radius=0.1),
        #    material=MeshPhysicalMaterial(transparent=False, color='black'),
        #    position=self.__headMoves
        #)
        #body
        self.body=Mesh(
            geometry=SphereBufferGeometry(radius=0.18),
            material=matbody,
            position=self.__bodyMoves
        )
        #self.body=Mesh(
        #    geometry=SphereBufferGeometry(radius=0.18),
        #    material=MeshPhysicalMaterial(transparent=False, color='black'),
        #    position=self.__bodyMoves
        #)
        #tail
        self.tail=Mesh(
            geometry=SphereBufferGeometry(radius=0.15),
            material=matbody,
            position=self.__tailMoves
        )
        #self.tail=Mesh(
        #    geometry=SphereBufferGeometry(radius=0.15),
        #    material=MeshPhysicalMaterial(transparent=False, color='black'),
        #    position=self.__tailMoves
        #)
        #
        self.__timing=[0]
        self.__nbMoves= 0
        self.__actionT=None
        self.__actionC=None
        self.__actionQ=None
        self.__authorizedMove=True
    
    @property
    def bodyMoves(self): return self.__bodyMoves
    
    @property
    def headMoves(self): return self.__headMoves
    
    @property
    def tailMoves(self): return self.__tailMoves
    
    @property
    def timing(self): return self.__timing
    
    @property
    def actionT (self): return self.__actionT
    
    @property
    def actionC (self): return self.__actionC
    
    @property
    def actionQ (self): return self.__actionQ
    
    @property
    def orientation (self): return self.__orientation
    
    @property
    def authorizedMove(self): return self.__authorizedMove
    
    def block(self): 
        """
            Called when there was a collision, no move may be added 
            
            Test
            ----------
            >>> ant=Ant(0,0,0,1,1,1,'S')
            >>> ant.bodyMoves
            [0, 0, 0]
            >>> ant.move()
            True
            >>> ant.bodyMoves
            [0, 0, 0, 0, 0, 1]
            >>> ant.block()
            >>> ant.move()
            False
            >>> ant.bodyMoves
            [0, 0, 0, 0, 0, 1]
            
        """
        self.__authorizedMove=False
    
    def position_part(self, part, direction, x, y, z):
        """
            Position of head and tail according the the given position (x,y,z) of the body
            
            Parameters
            ----------
            part : (type=string) Designate which part of the ant we want the coordonates : 'Head' or 'Tail'
            direction : (type=string) Designate the orientation of the ant in this case
            x : (type=int) x coordonate of the ant's body
            y : (type=int) y coordonate of the ant's body
            z : (type=int) z coordonate of the ant's body
            
            Test
            ----------
            >>> ant=ant=Ant(4,5,7,1,1,1,'S')
            >>> ant.position_part('Head','N',0,0,0)
            [0, 0, -0.26]
            >>> ant.position_part('Tail','N',0,0,0)
            [0, 0, 0.25]
            
        """
        assert isinstance(part,str), "part has to be a string"
        assert (part=='Head' or part=='Tail'), "Part has to has one of the following values : ['Head', 'Tail'] "
        assert isinstance(direction,str), 'direction has to be a string'
        assert (direction in ['N','S','W','E','U','D']), "direction has to belong to ['N','S','W','E','U','D']"
        assert (isinstance(x,float) or isinstance(x,int)), "x has to be a float or an int"
        assert (isinstance(y,float) or isinstance(y,int)), "y has to be a float or an int"
        assert (isinstance(z,float) or isinstance(z,int)), "z has to be a float or an int"
        return [x+self.__relativePositions[direction][part][0], y+self.__relativePositions[direction][part][1], z+self.__relativePositions[direction][part][2]]
    
        
    def turn(self, direction):
        """
            Make the ant turn to a given direction
            
            Parameter
            ----------
            direction : (type=str) new orientation of the ant
            
            Tests
            ----------
            >>> ant=ant=Ant(0,0,0,1,1,1,'S')
            >>> ant.turn('E')
            >>> ant.headMoves
            [0, 0, 0.26, -0.26, 0, 0]
            >>> ant.bodyMoves
            [0, 0, 0, 0, 0, 0]
            >>> ant.tailMoves
            [0, 0, -0.25, 0.25, 0, 0]
            
            
        """
        assert isinstance(direction,str), "direction has to be a string"
        assert (direction in ['N','S','W','E','U','D']), "direction has to belong to ['N','S','W','E','U','D']"
        if direction!='U' and direction !='D' :
            self.__lastHorizontalOrientation=self.__orientation
        self.__orientation=direction
        #dist=sqrt((self.position[0]-x)**2+(self.position[1]-y)**2+(self.position[2]-z)**2)
        self.__timing.append(self.__timing[self.__nbMoves]+1)#self.__timing[self.__nbMoves]+int(dist))
        #body 
        self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3])
        self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3+1])
        self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3+2])
        self.__nbMoves+=1
        #Head
        self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3]+self.__relativePositions[direction]['Head'][0])
        self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3+1]+self.__relativePositions[direction]['Head'][1])
        self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3+2]+self.__relativePositions[direction]['Head'][2])
        #Tail
        self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3]+self.__relativePositions[direction]['Tail'][0])
        self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3+1]+self.__relativePositions[direction]['Tail'][1])
        self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3+2]+self.__relativePositions[direction]['Tail'][2])
        self.position=(self.__bodyMoves[self.__nbMoves*3],self.__bodyMoves[self.__nbMoves*3+1],self.__bodyMoves[self.__nbMoves*3+2])

    
    def right(self):
        """
            Makes the ant turn to the right
            
            Test
            ----------
            >>> ant=Ant(4,8,9,1,1,1,'E')
            >>> ant.right()
            >>> ant.bodyMoves
            [4, 8, 9, 4, 8, 9]
            >>> ant.headMoves
            [3.74, 8, 9, 4, 8, 8.74]
            >>> ant.tailMoves
            [4.25, 8, 9, 4, 8, 9.25]
            
        """
        self.turn(self.__orientationTurn['D'][self.__orientation])
    
    def left(self):
        """
            Makes the ant turns to the left
            
            Test
            ----------
            >>> ant=Ant(4,8,9,1,1,1,'E')
            >>> ant.left()
            >>> ant.bodyMoves
            [4, 8, 9, 4, 8, 9]
            >>> ant.headMoves
            [3.74, 8, 9, 4, 8, 9.26]
            >>> ant.tailMoves
            [4.25, 8, 9, 4, 8, 8.75]
        """
        self.turn(self.__orientationTurn['G'][self.__orientation])
    
    def up(self):
        """
            Makes the ant turn in a vertical position looking up
            
            Test
            ----------
            >>> ant=Ant(4,8,9,1,1,1,'E')
            >>> ant.up()
            >>> ant.bodyMoves
            [4, 8, 9, 4, 8, 9]
            >>> ant.headMoves
            [3.74, 8, 9, 4, 8.26, 9]
            >>> ant.tailMoves
            [4.25, 8, 9, 4, 7.75, 9]
            
        """
        self.turn('U')
    
    def down(self):
        """
            Makes the ant turn in a vertical position looking down
            
            Test
            ----------
            >>> ant=Ant(4,8,9,1,1,1,'E')
            >>> ant.down()
            >>> ant.bodyMoves
            [4, 8, 9, 4, 8, 9]
            >>> ant.headMoves
            [3.74, 8, 9, 4, 7.74, 9]
            >>> ant.tailMoves
            [4.25, 8, 9, 4, 8.25, 9]
            
        """
        self.turn('D')
    
    def horizontal(self):
        """
            Turn the ant to its last horizontal position
            
            Test
            ----------
            >>> ant=Ant(4,8,9,1,1,1,'E')
            >>> ant.down()
            >>> ant.horizontal()
            >>> ant.bodyMoves
            [4, 8, 9, 4, 8, 9, 4, 8, 9]
            >>> ant.headMoves
            [3.74, 8, 9, 4, 7.74, 9, 3.74, 8, 9]
            >>> ant.tailMoves
            [4.25, 8, 9, 4, 8.25, 9, 4.25, 8, 9]
            
        """
        self.turn(self.__lastHorizontalOrientation)
    
    def front_coordonates(self):
        """
            Returns the ant's coordonates if it moved forward
            
            Test
            ----------
            >>> ant=Ant(8,2,1,1,1,1,'E')
            >>> ant.front_coordonates()
            (7, 2, 1)
            
        """
        move=self.__moveOriented[self.__orientation]
        return (self.__bodyMoves[self.__nbMoves*3]+move[0], self.__bodyMoves[self.__nbMoves*3+1]+move[1], self.__bodyMoves[self.__nbMoves*3+2]+move[2])
    
    def move(self):
        """
            Makes the ant move forward
            
            Test
            ----------
            >>> ant=Ant(8,2,1,1,1,1,'E')
            >>> ant.move()
            True
            >>> ant.bodyMoves
            [8, 2, 1, 7, 2, 1]
            >>> ant.headMoves
            [7.74, 2, 1, 6.74, 2, 1]
            >>> ant.tailMoves
            [8.25, 2, 1, 7.25, 2, 1]
            
        """
        move=self.__moveOriented[self.__orientation]
        if self.__authorizedMove:
            #dist=sqrt((self.position[0]-x)**2+(self.position[1]-y)**2+(self.position[2]-z)**2)
            self.__timing.append(self.__timing[self.__nbMoves]+1)#self.__timing[self.__nbMoves]+int(dist))
            #body 
            self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3]+move[0])
            self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3+1]+move[1])
            self.__bodyMoves.append(self.__bodyMoves[self.__nbMoves*3+2]+move[2])
            self.__nbMoves+=1
            #Head
            self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3]+self.__relativePositions[self.__orientation]['Head'][0])
            self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3+1]+self.__relativePositions[self.__orientation]['Head'][1])
            self.__headMoves.append(self.__bodyMoves[self.__nbMoves*3+2]+self.__relativePositions[self.__orientation]['Head'][2])
            #Tail
            self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3]+self.__relativePositions[self.__orientation]['Tail'][0])
            self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3+1]+self.__relativePositions[self.__orientation]['Tail'][1])
            self.__tailMoves.append(self.__bodyMoves[self.__nbMoves*3+2]+self.__relativePositions[self.__orientation]['Tail'][2])
            self.position=(self.__bodyMoves[self.__nbMoves*3],self.__bodyMoves[self.__nbMoves*3+1],self.__bodyMoves[self.__nbMoves*3+2])
            return True
        else:
            return False
    
    def removeMove(self):
        """
            Pop the last move of the ant from its moves and position lists
            
            Test
            ----------
            >>> ant=Ant(8,2,1,1,1,1,'E')
            >>> ant.move()
            True
            >>> ant.move()
            True
            >>> ant.bodyMoves
            [8, 2, 1, 7, 2, 1, 6, 2, 1]
            >>> ant.headMoves
            [7.74, 2, 1, 6.74, 2, 1, 5.74, 2, 1]
            >>> ant.tailMoves
            [8.25, 2, 1, 7.25, 2, 1, 6.25, 2, 1]
            >>> ant.removeMove()
            >>> ant.bodyMoves
            [8, 2, 1, 7, 2, 1]
            >>> ant.headMoves
            [7.74, 2, 1, 6.74, 2, 1]
            >>> ant.tailMoves
            [8.25, 2, 1, 7.25, 2, 1]
            
        """
        for i in range (0,3):
            self.__tailMoves.pop()
            self.__bodyMoves.pop()
            self.__headMoves.pop()
        self.__timing.pop()
        self.__nbMoves-=1
        self.position=(self.__bodyMoves[self.__nbMoves*3],self.__bodyMoves[self.__nbMoves*3+1],self.__bodyMoves[self.__nbMoves*3+2])
    
    
    def resetMoves(self):
        """
            Erase all the moves and reset the ant
            
            Test
            ----------
            >>> ant=Ant(8,2,1,1,1,1,'E')
            >>> ant.move()
            True
            >>> ant.move()
            True
            >>> ant.bodyMoves
            [8, 2, 1, 7, 2, 1, 6, 2, 1]
            >>> ant.headMoves
            [7.74, 2, 1, 6.74, 2, 1, 5.74, 2, 1]
            >>> ant.tailMoves
            [8.25, 2, 1, 7.25, 2, 1, 6.25, 2, 1]
            >>> ant.timing
            [0, 1, 2]
            >>> ant.resetMoves()
            >>> ant.bodyMoves
            [8, 2, 1]
            >>> ant.headMoves
            [7.74, 2, 1]
            >>> ant.tailMoves
            [8.25, 2, 1]
            >>> ant.timing
            [0]
            
        """
        #Stop the old animation
        if self.__actionT!=None and self.__actionC!=None and self.__actionQ!=None:
            self.__actionT.stop()
            self.__actionC.stop()
            self.__actionQ.stop()
        #Set the position to the initial position
        self.position=(self.__bodyMoves[0],self.__bodyMoves[1],self.__bodyMoves[2])
        # orientation
        self.__orientation=self.__initialOrientation
        #self.object3D.position=self.__moves[:3]
        self.__timing=[0]
        self.__bodyMoves=self.__bodyMoves[:3]
        self.__headMoves=self.__headMoves[:3]
        self.__tailMoves=self.__tailMoves[:3]
        self.__nbMoves=0
        self.__authorizedMove=True
    
    def mkMove(self):
        """
            Make the animation for each part of the ant
        """
        #Head
        head_positon_track = VectorKeyframeTrack(name='.position',
        times=self.__timing,
        values=self.__headMoves)
        head_clip = AnimationClip(tracks=[head_positon_track])
        self.__actionT = AnimationAction(AnimationMixer(self.head), head_clip, self.head)
        #body
        body_positon_track = VectorKeyframeTrack(name='.position',
        times=self.__timing,
        values=self.__bodyMoves)
        body_clip = AnimationClip(tracks=[body_positon_track])
        self.__actionC = AnimationAction(AnimationMixer(self.body), body_clip, self.body)
        #Tail
        tail_positon_track = VectorKeyframeTrack(name='.position',
        times=self.__timing,
        values=self.__tailMoves)
        tail_clip = AnimationClip(tracks=[tail_positon_track])
        self.__actionQ = AnimationAction(AnimationMixer(self.tail), tail_clip, self.tail)
