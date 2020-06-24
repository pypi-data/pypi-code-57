import os
import json
import time
from .Ant import Ant
from .StaticObject import StaticObject
from .Visualisation import Visualisation
from .value_player_widget import ValuePlayerWidget
import traitlets
import ipywidgets as widgets
from .Object3D import Object3D
from pythreejs import PerspectiveCamera, DirectionalLight,AmbientLight, Scene, OrbitControls, Renderer
__version__ = '0.1'
global translation
translation={'en_EN':{'right':'Right','left':'Left','up':'Up','down':'Down','horizontal':'Horizontal','move':'Move','win':'images/win.jpg'},
            'fr_FR':{'right':'Droite','left':'Gauche','up':'Haut','down':'Bas','horizontal':'Horizontal','move':'Avancer','win':'images/gagne.jpg'}}

def mkImageWidget(file_name, im_format,w=50,h=50):
    """ Return an object widget.Image displaying the image titled file_name
        
        Parameters
        ----------
        file_name : (type=string) image file name
        im_format : (type=string) format of the file
        w : (default value=50) (type=int) image width
        h : (default value=50) (type=int) image height
        
    """
    assert isinstance(file_name, str), "file_name doit être un string"
    assert isinstance(im_format, str), "im_format doit être un string"
    assert isinstance(w,int), "w has to be an int"
    assert isinstance(h, int), "h has to be an int"
    file=open(os.path.dirname(__file__)+"/"+file_name,"rb")
    image=file.read()
    return widgets.Image(
            value=image,
            format=im_format,
            width=w,
            height=h,
            layout=widgets.Layout(border="none", margin="0px", padding="0 px")
        )


class Maze(widgets.VBox):
    """
        Models a 3 dimentional maze created from a JSON file
        
        Readable attributes
        ----------
        value : (type=list) value linked to ValuePlayerWidget
        children : (type=list) all the children given to the 3D scene
        renderer : (type=Renderer) 3D visualisation
        player : (type=ValuePlayerWidget) the ValuePlayerWidget containing the visualisation
        ant : (type=Ant) the ant inside the maze
    """
    value=traitlets.List()
    def __init__(self,file, language='en_EN'):
        """
            Maze's initialization
            
            Parameter
            ----------
            file : (type=string) path to the JSON file describing the file
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.ant.position
            (-4, 0.5, -4)
            >>> maze.ant.timing
            [0]
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.player.player.pause()
            
        """
        assert isinstance(file,str), "file has to be a string"
        
        if language in translation:
            self.__language=language
        else:
            self.__langugage='en_EN'
        with open(os.path.dirname(__file__)+"/"+file, 'r') as myfile:
            data=myfile.read()
            # parse file
            obj = json.loads(data)
            
        # View
        view_width = obj['view']['w']
        view_height = obj['view']['h']
        camera = PerspectiveCamera( position=[obj['camera']['x'], obj['camera']['y'], obj['camera']['z']], aspect=view_width/view_height)
        key_light = DirectionalLight(position=[obj['key_light']['x'], obj['key_light']['y'], obj['key_light']['z']])
        ambient_light = AmbientLight()
        
        # The ant
        self.__ant=Ant(obj['ant']['x'],obj['ant']['y'],obj['ant']['z'],obj['ant']['w'],obj['ant']['h'],obj['ant']['d'],obj['ant']['orientation'])
        
        # Static objects inside the maze
        self.__contenu=[StaticObject(obj['ground']['x'],obj['ground']['y'],obj['ground']['z'],obj['ground']['w'],obj['ground']['h'],obj['ground']['d'])]
        
        # Maze dimensions
        dimensions=[obj['ant']['x'],obj['ant']['x'],obj['ground']['y'],obj['ground']['y'],obj['ground']['z'],obj['ground']['z'],0,0,0] # [xmin,xmax,ymin,ymax,zmin,zmax,width,height,deepth]
        
        for b in obj['bloc']:
            self.__contenu.append(StaticObject(b['x'],b['y'],b['z'],b['w'],b['h'],b['d'],"red"))
            dimensions[0]=min(dimensions[0],b['x'])
            dimensions[1]=max(dimensions[1],b['x'])
            dimensions[2]=min(dimensions[2],b['y'])
            dimensions[3]=max(dimensions[3],b['y'])
            dimensions[4]=min(dimensions[4],b['z'])
            dimensions[5]=max(dimensions[5],b['z'])
        
        # Make the cube containing all the maze
        dimensions[6]= dimensions[1]-dimensions[0]
        dimensions[7]= dimensions[3]-dimensions[2]
        dimensions[8]= dimensions[5]-dimensions[4]
        
        x=(dimensions[1]+dimensions[0])/2
        y=(dimensions[3]+dimensions[2])/2
        z=(dimensions[5]+dimensions[4])/2
        self.__contouringCube= Object3D(x=x,y=y,z=z,w=dimensions[6],h=dimensions[7],d=dimensions[8])
        
        # light 2
        dlight=DirectionalLight(position=[10,10 ,10 ])
        
        # Every object inside the scene
        children=[camera, key_light,dlight, ambient_light,self.__ant.head,self.__ant.body,self.__ant.tail]
        for i in self.__contenu:
            children.append(i.object3D)
            
        # The visualisation
        self.__scene = Scene(children=children)
        self.__controller = OrbitControls(controlling=camera)
        self.__renderer = Renderer(camera=camera, scene=self.__scene, controls=[self.__controller],
                            width=view_width, height=view_height)
        self.__message=mkImageWidget('images/blanc.jpg', 'jpg' ,250,125)
        self.__action=widgets.Label(value='')
        self.update_action()
        
        #ValuePlayerWidget
        self.__value=self.mk_value()
        messageBox=widgets.VBox([self.__action,self.__message],layout=widgets.Layout(justify_content="center"))
        #widgets.VBox([mkImageWidget('images/blanc.jpg', 'jpg' ,200,100),self.__message,mkImageWidget('images/blanc.jpg', 'jpg' ,50,20)])]
        self.__view=Visualisation([self.__renderer,messageBox],self.__value)
        traitlets.link([self,"value"],[self.__view,"value"])
        self.__player=ValuePlayerWidget(self.__view,language)
        self.__player.player.reset(self.__value)
        
        #widgets.HBox.__init__(self,[self.__player])
        widgets.VBox.__init__(self,[self.__player])
    
    @traitlets.observe('value')
    def _observe_value(self, change):
    # when self.__value is modified, the visualisation has to change
        self.valuePlayer_move(change['new'])
    
    @property
    def renderer(self): return self.__renderer
    
    @property
    def player(self): return self.__player
    
    @property
    def message(self): return self.__message
    
    @property
    def ant(self): return self.__ant

    @property
    def history(self): return (self.__ant.headMoves, self.__ant.bodyMoves, self.__ant.tailMoves)

    def mk_value(self, action=None):
        """
            Returns the new value for self.__value
        """
        return [self.__ant.orientation, self.__ant.position[0], self.__ant.position[1], self.__ant.position[2],action]
    
    def update_action(self, value=None):
        """
            Update the label on which the action is displayed
        """
        if isinstance(value,str) and value!=None:
            self.__action.value="Action : "+value
        else:
            self.__action.value=""
    
    def valuePlayer_move(self,change):
        """
            Modifies the visualisation when ValuePlayerWidget change self.__value
            
            Parameter
            ----------
            change : (type=list) new orientation and coordonates 
        """
        assert isinstance(change[0],str),"change[0] has to be a string"
        assert (change[0] in ['N','S','U','D','E','W']), "change[0] has to belong to ['N','S','U','D','E','W']"
        assert (isinstance(change[1],int) or isinstance(change[1],float)), "change[1] has to be an int or a float"
        assert (isinstance(change[2],int) or isinstance(change[2],float)), "change[2] has to be an int or a float"
        assert (isinstance(change[3],int) or isinstance(change[3],float)), "change[3] has to be an int or a float"
        direction=change[0]
        x=change[1]
        y=change[2]
        z=change[3]
        self.update_action(change[4])
        head_coordonates=self.__ant.position_part('Head', direction, x, y, z)
        tail_coordonates=self.__ant.position_part('Tail', direction, x, y, z)
        self.__ant.head.position=head_coordonates
        self.__ant.body.position=[x,y,z]
        self.__ant.tail.position=tail_coordonates
        if self.__ant.future_collision([x,y,z],self.__contouringCube)==False:
            file=open(os.path.dirname(__file__)+"/"+translation[self.__language]['win'],"rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
        else:
            file=open(os.path.dirname(__file__)+"/"+"images/blanc.jpg","rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
        for ob in self.__contenu:
            if self.__ant.future_collision([x,y,z],ob)==True:
                file=open(os.path.dirname(__file__)+"/"+"images/perdu.png","rb")
                image=file.read()
                self.__message.format="png"
                self.__message.value=image
        #time.sleep(0.5)
    
    def majMove(self, action=None):
        """
            Update the position of each part of the ant
        """
        self.__ant.head.position=self.__ant.headMoves[len(self.__ant.headMoves)-3:len(self.__ant.headMoves)]
        self.__ant.body.position=self.__ant.bodyMoves[len(self.__ant.bodyMoves)-3:len(self.__ant.bodyMoves)]
        self.__ant.tail.position=self.__ant.tailMoves[len(self.__ant.tailMoves)-3:len(self.__ant.tailMoves)]
        self.__player.set_value(self.mk_value(action))
        if self.__ant.collision(self.__contouringCube)==False:
            file=open(os.path.dirname(__file__)+"/"+translation[self.__language]['win'],"rb")
            image=file.read()
            self.__message.format="jpg"
            self.__message.value=image
            self.__ant.block()
        elif self.__ant.authorizedMove==False:
            file=open(os.path.dirname(__file__)+"/"+"images/perdu.png","rb")
            image=file.read()
            self.__message.format="png"
            self.__message.value=image
        time.sleep(0.2)
    
    def collision(self):
        """
            Check if there is a collision. If there is a collision, the last move is poped from the moves list
            No move may be added
        """
        #c=0
        for ob in self.__contenu:
            if self.__ant.collision(ob)==True:
                #c+=1
                #self.__ant.removeMove()
                self.__ant.block()
    
    def look(self):
        """
            Returns False if the ant is in front of an obstacle and therefore cannot move forward
            Returns True otherwise
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.look()
            True
            >>> maze.right()
            >>> maze.look()
            False
            >>> maze.player.player.pause()
            
        """
        if self.__ant.authorizedMove:
            next_coordonates=self.__ant.front_coordonates()
            for ob in self.__contenu:
                if self.__ant.future_collision(next_coordonates, ob)==True:
                    return False
            return True
        else:
            return False
    
    def right(self):
        """
            Turns the ant to the right
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.right()
            >>> maze.history
            ([-4, 0.5, -3.74, -4.26, 0.5, -4], [-4, 0.5, -4, -4, 0.5, -4], [-4, 0.5, -4.25, -3.75, 0.5, -4])
            >>> maze.player.player.pause()
        """
        if self.__ant.authorizedMove:
            self.__ant.right()
            self.majMove(translation[self.__language]['right'])
    
    def left(self):
        """
            Turns the ant to the left
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.left()
            >>> maze.history
            ([-4, 0.5, -3.74, -3.74, 0.5, -4], [-4, 0.5, -4, -4, 0.5, -4], [-4, 0.5, -4.25, -4.25, 0.5, -4])
            >>> maze.player.player.pause()
            
        """
        if self.__ant.authorizedMove:
            self.__ant.left()
            self.majMove(translation[self.__language]['left'])
    
    def move(self):
        """
            Make the ant move forward if there is no obstacle
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.move()
            >>> maze.history
            ([-4, 0.5, -3.74, -4, 0.5, -2.74], [-4, 0.5, -4, -4, 0.5, -3], [-4, 0.5, -4.25, -4, 0.5, -3.25])
            >>> maze.player.player.pause()
            
        """
        if self.__ant.move():
            self.collision()
            self.majMove(translation[self.__language]['move'])
    
    def up(self):
        """
            Turns the ant to the up
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.up()
            >>> maze.history
            ([-4, 0.5, -3.74, -4, 0.76, -4], [-4, 0.5, -4, -4, 0.5, -4], [-4, 0.5, -4.25, -4, 0.25, -4])
            >>> maze.player.player.pause()
            
        """
        if self.__ant.authorizedMove:
            self.__ant.up()
            self.majMove(translation[self.__language]['up'])
    
    def down(self):
        """
            Turns the ant to the down
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.down()
            >>> maze.history
            ([-4, 0.5, -3.74, -4, 0.24, -4], [-4, 0.5, -4, -4, 0.5, -4], [-4, 0.5, -4.25, -4, 0.75, -4])
            >>> maze.player.player.pause()
            
        """
        if self.__ant.authorizedMove:
            self.__ant.down()
            self.majMove(translation[self.__language]['down'])
    
    def horizontal(self):
        """
            Turns the ant to its last horizontal orientation
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.down()
            >>> maze.horizontal()
            >>> maze.history
            ([-4, 0.5, -3.74, -4, 0.24, -4, -4, 0.5, -3.74], [-4, 0.5, -4, -4, 0.5, -4, -4, 0.5, -4], [-4, 0.5, -4.25, -4, 0.75, -4, -4, 0.5, -4.25])
            >>> maze.player.player.pause()
            
        """
        if self.__ant.authorizedMove:
            self.__ant.horizontal()
            self.majMove(translation[self.__language]['horizontal'])
    
    def reset(self):
        """
            Reset the game
            
            Tests
            ----------
            >>> maze=Maze('lab/lab.json')
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.move()
            >>> maze.move()
            >>> maze.move()
            >>> maze.left()
            >>> maze.history
            ([-4, 0.5, -3.74, -4, 0.5, -2.74, -4, 0.5, -1.74, -4, 0.5, -0.74, -3.74, 0.5, -1], [-4, 0.5, -4, -4, 0.5, -3, -4, 0.5, -2, -4, 0.5, -1, -4, 0.5, -1], [-4, 0.5, -4.25, -4, 0.5, -3.25, -4, 0.5, -2.25, -4, 0.5, -1.25, -4.25, 0.5, -1])
            >>> maze.reset()
            >>> maze.history
            ([-4, 0.5, -3.74], [-4, 0.5, -4], [-4, 0.5, -4.25])
            >>> maze.player.player.pause()
            
        """
        self.__ant.resetMoves()
        file=open(os.path.dirname(__file__)+"/"+"images/blanc.jpg","rb")
        image=file.read()
        self.__message.format="jpg"
        self.__message.value=image
        self.majMove()
        self.__value=self.mk_value()
        self.__player.player.reset(self.__value)
