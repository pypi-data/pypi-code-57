from vectorObjects.VectorMaster import VectorMaster
import operator
import math
import numpy


class Vector2D(VectorMaster):
    """
    A vector object for working with 2D coordinates or uv values.

    """
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        """
        Return for debugging
        """
        return f"{self.x, self.y}"

    def __str__(self):
        """
        Print return for code readability
        """
        return f"X: {self.x}, Y: {self.y}"

    def __getitem__(self, item):
        """
        Allows for index calling returns in order of x, y.
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Index out of range: Vector 3D has x[0] and y[1] items. Item calls greater than 1 "
                             "not permitted")

    def __iter__(self):
        """
        Allows for iteration in order x, y.
        """
        yield self.x
        yield self.y

    def __add__(self, other):
        """
        Add ether another instance of vector 2D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.add)

    def __sub__(self, other):
        """
        Subtract ether another instance of vector 2D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.sub)

    def __mul__(self, other):
        """
        Multiply ether another instance of vector 2D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.mul)

    def __truediv__(self, other):
        """
        Divide ether another instance of vector 2D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.truediv)

    def __neg__(self):
        """
        Invert the sign of all elements
        """
        return self._negative(self)

    def __eq__(self, other):
        """
        See if two vectors are equal
        """
        return self._equality(self, other)

    def __ne__(self, other):
        """
        Opposite of equality
        """
        return not self.__eq__(other)

    def to_tuple(self):
        """
        Returns a tuple representation of type (x, y)
        """
        return self._return_tuple(self)

    def to_list(self):
        """
        Returns a list representation of type [x, y]
        """
        return self._return_list(self)

    def dot_product(self, other):
        """
        Calculate the dot product of two instances of the same class object
        """
        return self._return_dot_product(self, other)

    def cross_product(self, other):
        """
        Calculate the cross product of two instances of the same class object
        """
        return self._return_cross_product(self, other)

    def normalise(self):
        """
        Normalise attributes
        """
        return self._normalise_attributes(self)


class Vector3D(VectorMaster):
    """
    A vector object for working with 3D coordinates such as vertex positions in 3D space or a normal direction.
    """
    __slots__ = ["x", "y", "z"]

    def __init__(self, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """
        Return for debugging
        """
        return f"{self.x, self.y, self.z}"

    def __str__(self):
        """
        Print return for code readability
        """
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}"

    def __getitem__(self, item):
        """
        Allows for index calling returns in order of x, y, z.
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError("Index out of range: Vector 3D has x[0], y[1] and z[2] items. Item calls greater than 2 "
                             "not permitted")

    def __iter__(self):
        """
        Allows for iteration in order x, y, z
        """
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        """
        Add ether another instance of vector 3D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.add)

    def __sub__(self, other):
        """
        Subtract ether another instance of vector 3D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.sub)

    def __mul__(self, other):
        """
        Multiply ether another instance of vector 3D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.mul)

    def __truediv__(self, other):
        """
        Divide ether another instance of vector 3D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.truediv)

    def __neg__(self):
        """
        Invert the sign of all elements
        """
        return self._negative(self)

    def __eq__(self, other):
        """
        See if two vectors are equal
        """
        return self._equality(self, other)

    def __ne__(self, other):
        """
        Opposite of equality
        """
        return not self.__eq__(other)

    def to_tuple(self):
        """
        Returns a tuple representation of type (x, y, z)
        """
        return self._return_tuple(self)

    def to_list(self):
        """
        Returns a list representation of type [x, y ,z]
        """
        return self._return_list(self)

    def dot_product(self, other):
        """
        Calculate the dot product of two instances of the same class object
        """
        return self._return_dot_product(self, other)

    def cross_product(self, other):
        """
        Calculate the cross product of two instances of the same class object
        """
        return self._return_cross_product(self, other)

    def normalise(self):
        """
        Normalise attributes
        """
        return self._normalise_attributes(self)


class Vector4D(VectorMaster):
    """
    Vector for 4D vertex coordinates and normal directions
    """

    __slots__ = ['x', 'y', 'z', 'w']

    def __init__(self, x=0, y=0, z=0, w=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        """
        Return for debugging
        """
        return f"{self.x, self.y, self.z, self.w}"

    def __str__(self):
        """
        Print return for code readability
        """
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}, W: {self.w}"

    def __getitem__(self, item):
        """
        Allows for index calling returns in order of x, y, z, w.
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.w
        else:
            raise IndexError("Index out of range: Vector 4D has x[0], y[1], z[2], and w[3] items. Item calls greater"
                             " than 3 not permitted")

    def __iter__(self):
        """
        Allows for iteration in order x, y, z, w
        """
        yield self.x
        yield self.y
        yield self.z
        yield self.w

    def __add__(self, other):
        """
        Add ether another instance of vector 4D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.add)

    def __sub__(self, other):
        """
        Subtract ether another instance of vector 4D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.sub)

    def __mul__(self, other):
        """
        Multiply ether another instance of vector 4D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.mul)

    def __truediv__(self, other):
        """
        Divide ether another instance of vector 4D, an int/float as a constant to all attributes, or a list/tuple of
        values of equal length to the number of attributes

        :type other: Vector3D | int | float | list | tuple
        :rtype: tuple
        """
        return self._mathematical_operator(self, other, operator.truediv)

    def __neg__(self):
        """
        Invert the sign of all elements
        """
        return self._negative(self)

    def __eq__(self, other):
        """
        See if two vectors are equal
        """
        return self._equality(self, other)

    def __ne__(self, other):
        """
        Opposite of equality
        """
        return not self.__eq__(other)

    def to_tuple(self):
        """
        Returns a tuple representation of type (x, y, z, w)
        """
        return self._return_tuple(self)

    def to_list(self):
        """
        Returns a list representation of type [x, y ,z, w]
        """
        return self._return_list(self)

    def dot_product(self, other):
        """
        Calculate the dot product of two instances of the same class object
        """
        return self._return_dot_product(self, other)

    def cross_product(self, other):
        """
        Calculate the cross product of two instances of the same class object
        """
        return self._return_cross_product(self, other)

    def normalise(self):
        """
        Normalise attributes
        """
        return self._normalise_attributes(self)


class PymeshioQuaternion(VectorMaster):
    """
    Rotation representation in vmd motion

    Unlike the other classes this is mostly kept as it was. Original source: https://github.com/ousttrue/pymeshio

    Warning
    ---------
    This is highly likely to change

    """
    __slots__ = ['x', 'y', 'z', 'w']

    def __init__(self, x=0, y=0, z=0, w=1):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        """
        Return for debugging
        """
        return f"{self.x, self.y, self.z, self.w}"

    def __str__(self):
        """
        Print return for code readability
        """
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}, W: {self.w}"

    def __getitem__(self, item):
        """
        Allows for index calling returns in order of x, y, z, w.
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.w
        else:
            raise IndexError("Index out of range: Vector 4D has x[0], y[1], z[2], and w[3] items. Item calls greater"
                             " than 3 not permitted")

    def __mul__(self, rhs):
        u=numpy.array([self.x, self.y, self.z], 'f')
        v=numpy.array([rhs.x, rhs.y, rhs.z], 'f')
        xyz=self.w*v+rhs.w*u+numpy.cross(u, v)
        return PymeshioQuaternion(xyz[0], xyz[1], xyz[2], self.w*rhs.w-numpy.dot(u, v))

    def dot(self, rhs):
        return self.x*rhs.x+self.y*rhs.y+self.z*rhs.z+self.w*rhs.w

    @staticmethod
    def _mmd_quaternion_array(sqY, sqZ, xy, wz, xz, wy, sqX, yz, wx):
        return numpy.array([
            # 1
            [1 - 2 * sqY - 2 * sqZ, 2 * xy + 2 * wz, 2 * xz - 2 * wy, 0],
            # 2
            [2 * xy - 2 * wz, 1 - 2 * sqX - 2 * sqZ, 2 * yz + 2 * wx, 0],
            # 3
            [2 * xz + 2 * wy, 2 * yz - 2 * wx, 1 - 2 * sqX - 2 * sqY, 0],
            # 4
            [0, 0, 0, 1]],
            'f')

    def getMatrix(self):
        sqX = self.x*self.x
        sqY = self.y*self.y
        sqZ = self.z*self.z
        xy = self.x*self.y
        xz = self.x*self.z
        yz = self.y*self.z
        wx = self.w*self.x
        wy = self.w*self.y
        wz = self.w*self.z
        return self._mmd_quaternion_array(sqY, sqZ, xy, wz, xz, wy, sqX, yz, wx)

    def getRHMatrix(self):
        x = -self.x
        y = -self.y
        z = self.z
        w = self.w
        sqX = x*x
        sqY = y*y
        sqZ = z*z
        xy = x*y
        xz = x*z
        yz = y*z
        wx = w*x
        wy = w*y
        wz = w*z
        return self._mmd_quaternion_array(sqY, sqZ, xy, wz, xz, wy, sqX, yz, wx)

    def getRollPitchYaw(self):
        m=self.getMatrix()

        roll = math.atan2(m[0, 1], m[1, 1])
        pitch = math.asin(-m[2, 1])
        yaw = math.atan2(m[2, 0], m[2, 2])

        if math.fabs(math.cos(pitch)) < 1.0e-6:
            roll += m[0, 1] > math.pi if 0.0 else -math.pi
            yaw += m[2, 0] > math.pi if 0.0 else -math.pi

        return roll, pitch, yaw

    def getNormalized(self):
        return self._normalise_attributes(self)

    def getRightHanded(self):
        "swap y and z axis"
        return PymeshioQuaternion(-self.x, -self.z, -self.y, self.w)

    @staticmethod
    def createFromAxisAngle(axis, rad):
        half_rad=rad/2.0
        s=math.sin(half_rad)
        return PymeshioQuaternion(axis[0]*s, axis[1]*s, axis[2]*s, math.cos(half_rad))
