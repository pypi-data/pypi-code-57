from pythreejs import *
from .Object3D import Object3D
__version__ = '0.1'
class StaticObject(Object3D):
    """
        A 3 dimentional object unable to move : used to add walls to the maze
        Inherits from Object3D
    """
    def __init__(self,x,y,z,w,h,d,colour='green',op=0.5, trsp=True):
        """
            Initialization of the static object
            
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
            -----------
            >>> obj=StaticObject(3,1,2,1,1,1)
            >>> obj.position
            (3, 1, 2)
            >>> obj.width
            1
            >>> obj.height
            1
            >>> obj.deepth
            1
            >>> obj.colour
            'green'
            
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
        super().__init__ (x,y,z,w,h,d,colour)
        self.object3D=Mesh(
                        BoxBufferGeometry(w, h, d),
                        MeshPhysicalMaterial(opacity=op, transparent=trsp, color=colour),
                        position=[x, y, z]
                      )
