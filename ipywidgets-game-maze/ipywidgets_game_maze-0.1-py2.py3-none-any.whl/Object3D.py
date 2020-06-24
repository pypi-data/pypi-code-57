__version__ = '0.1'
class Object3D():
    """
        Any 3 dimentionnal object
        
        Readable attributes
        ----------
        position : (type=tupple) coordonates (x,y,z)
        width : (type=int or float) object's width
        height : (type=int or float) object's height
        deepth : (type=int or float) object's deepth
        colour : (type=string) object's colour
        
    """
    def __init__(self,x,y,z,w,h,d,colour='blue',op=0.5, trsp=True):
        """
            Initialization of the 3 dimentional object
            
            Parameters
            -----------
            x : (type=int or float) x coordonates of the object's center
            y : (type=int or float) y coordonates of the object's center
            z : (type=int or float) z coordonates of the object's center
            w : (type=int or float) width
            h : (type=int or float) height
            d : (type=int or float) deepth
            coulour : (default value='green') (type=string) the object's colour
            op : (default value=0.5) (type=float) opacity
            trsp : (default value=True) (type=boolean) transparancy of the object
            
            Test
            ----------
            >>> obj=Object3D(3,1,2,1,1,1,'red',0.4,True)
            >>> obj.position
            (3, 1, 2)
            >>> obj.width
            1
            >>> obj.height
            1
            >>> obj.deepth
            1
            >>> obj.colour
            'red'
            
        """
        assert (isinstance(x,int) or isinstance(x,float)), "x has to be an int or a float"
        assert (isinstance(y,int) or isinstance(y,float)), "y has to be an int or a float"
        assert (isinstance(z,int) or isinstance(z,float)), "z has to be an int or a float"
        assert (isinstance(w,int) or isinstance(w,float)), "w has to be an int or a float"
        assert (isinstance(h,int) or isinstance(h,float)), "h has to be an int or a float"
        assert (isinstance(d,int) or isinstance(d,float)), "d has to be an int or a float"
        assert isinstance(colour,str), "colour has to be a string"
        assert (isinstance(op,float) or isinstance(op,int)),"op has to be an int or a float"
        assert isinstance(trsp,bool), "trsp has to be a boolean"
        self.position=(x,y,z)
        self.width=w
        self.height=h
        self.deepth=d
        self.colour=colour
    
    def collision(self,obstacle):
        """
            Check if there is a collision with an Object3D object given as a parameter.
            Returns True if there is a collision, False otherwise
            
            Parameter
            -----------
            obstacle : (type=Object3D) the obstacle there may be a collision with
            
            Test
            ----------
            >>> obj=Object3D(3,1,2,1,1,1)
            >>> obj2=Object3D(1,1,1,1,1,1)
            >>> obj.collision(obj2)
            False
            >>> obj3=Object3D(3,2,2,1,2,1)
            >>> obj.collision(obj3)
            True
            
        """
        assert isinstance(obstacle,Object3D), "obstacle has to be an Object3D"
        # coordonate of self
        x=self.position[0]-(self.width/2)
        y=self.position[1]-(self.height/2)
        z=self.position[2]-(self.deepth/2)
        #coordonate of the stranger object
        x2=obstacle.position[0]-(obstacle.width/2)
        y2=obstacle.position[1]-(obstacle.height/2)
        z2=obstacle.position[2]-(obstacle.deepth/2)
        #check for a collision
        #print("x: "+str(((xmin<=x2min)and(x2min<=xmax)) or ((xmin<=x2max) and(x2max<=xmax))))
        #print("y: "+str(((ymin<=y2min)and(y2min<=ymax)) or ((ymin<=y2max)and(y2max<=ymax))))
        #print("z: "+str(((zmin<=z2min)and(z2min<=zmax)) or ((zmin<=z2max)and(z2max<=z2max))))
        if((x2 >= x + self.width)      
            or (x2 + obstacle.width <= x) 
            or (y2 >= y + self.height) 
            or (y2 + obstacle.height <= y)    
            or (z2 >= z + self.deepth)   
            or (z2 + obstacle.deepth <= z)):
            return False
        else:
            return True
    
    def future_collision(self, coordonates, obstacle):
        """
            Check if there would be a collision with an Object3D given as a parameter if the object was in some given coordonates
            
            Parameters
            ----------
            coordonates : (type=list(int or float)) the hypothetic parameters
            obstacle : (type=Object3D) the obstacle
            
            Test
            ----------
            >>> obj=Object3D(3,1,9,1,1,1)
            >>> obj2=Object3D(3,1,2,1,5,1)
            >>> obj.future_collision([3,2,2],obj2)
            True
            >>> obj.future_collision([3,2,4],obj2)
            False
            
        """
        assert (isinstance(coordonates,list) or isinstance(coordonates,tuple)), "coordonates has to be a list"
        assert isinstance(obstacle,Object3D), "obstacle has to be an Object3D"
        # coordonate of self
        x=coordonates[0]-(self.width/2)
        y=coordonates[1]-(self.height/2)
        z=coordonates[2]-(self.deepth/2)
        #coordonate of the stranger object
        x2=obstacle.position[0]-(obstacle.width/2)
        y2=obstacle.position[1]-(obstacle.height/2)
        z2=obstacle.position[2]-(obstacle.deepth/2)
        #check for a collision
        if((x2 >= x + self.width)      
            or (x2 + obstacle.width <= x) 
            or (y2 >= y + self.height) 
            or (y2 + obstacle.height <= y)    
            or (z2 >= z + self.deepth)   
            or (z2 + obstacle.deepth <= z)):
            return False
        else:
            return True
        
