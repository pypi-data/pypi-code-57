import numpy as np
from .tools_processor import *
from sympy import symbols, sin, cos,init_printing, Matrix


class Axis:
    def __init__(self):
        self.x = 0
        self.y = 1
        self.z = 2
        self.xy = [0,1]
        self.xz = [0,2]
        self.yx = [1,0]
        self.yz = [1,2]
        self.zx = [2,0]
        self.zy = [2,1]
        self.xyz = [0,1,2]
        self.xzy = [0,2,1]
        self.yxz = [1,0,2]
        self.yzx = [1,2,0]
        self.zxy = [2,0,1]
        self.zyx = [2,1,0]
        self.x_ = np.array([1,0,0])
        self.y_ = np.array([0,1,0])
        self.z_ = np.array([0,0,1])
        self.absCorrd = np.array([[1,0,0],
                                  [0,1,0],
                                  [0,0,1]])





class Rmatrix:
    def __init__(self):
        self.x = symbols("x")
        self.y = symbols("y")
        self.z = symbols("z")
        self.φ = symbols("φ")
        self.θ = symbols("θ")
        self.ψ = symbols("ψ")

    def RMx(self,anlge):
        m = Matrix([
            [1.0,            0,            0],
            [  0,   cos(anlge),  -sin(anlge)],
            [  0,   sin(anlge),   cos(anlge)]
        ])
        return m

    def RMy(self,angle):
        m = Matrix([
            [ cos(angle),    0,  sin(angle)],
            [          0,  1.0,           0],
            [-sin(angle),    0,  cos(angle)]
        ])
        return m
    
    def RMz(self,angle):
        m = Matrix([
            [cos(angle), -sin(angle),   0],
            [sin(angle),  cos(angle),   0],
            [         0,           0, 1.0]
        ])
        return m

    def Rxyz(self):
        Rx, Ry, Rz = self.RMx(self.x), self.RMy(self.y), self.RMz(self.z)
        return Rz*Ry*Rx

    def Rxyz2(self):
        Rx, Ry, Rz = self.RMx(self.φ), self.RMy(self.θ), self.RMz(self.ψ)
        return Rz*Ry*Rx







class Vector:
    def __init__(self,base, ep1, ep2=None):
        self.sp = base
        self.ep1 = ep1
        self.ep2 = ep2

    @calc_vector
    def vector1(self):
        return self.ep1, self.sp

    @calc_vector
    def vector2(self):
        return self.ep2, self.sp

    @calc_cross
    def vector3(self):
        return self.vector1(), self.vector2()

    @calc_vecLength
    def Lvector1(self):
        return self.vector1()

    @calc_vecLength
    def Lvector2(self):
        return self.vector2()

    @calc_vecLength
    def Lvector3(self):
        return self.vector3()

    @calc_NormedVecotor
    def Nvector1(self):
        return self.vector1(), self.Lvector1()

    @calc_NormedVecotor
    def Nvector2(self):
        return self.vector2(), self.Lvector2()

    @calc_NormedVecotor
    def Nvector3(self):
        return self.vector3(), self.Lvector3()

    @calc_angle
    def VectorAngle(self):
        return self.vector1(), self.vector2(), self.Lvector1(), self.Lvector2()

    @calc_basis_vector
    def BasisVector(self):
        return self.Nvector1(), self.Nvector2(), self.Nvector3()


