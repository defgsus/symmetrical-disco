import math
from copy import copy
from typing import Sequence

from . import const
from .vec3_operators import Vec3Operators


class Vec3(Vec3Operators):

    def __init__(self, x=None, y=None, z=None):
        if x is None:
            self._v = [0., 0., 0.]
        else:
            if y is None:
                if isinstance(x, (int, float)):
                    self._v = [x, x, x]
                else:
                    self._v = [x[0], x[1], x[2]]
            else:
                self._v = [x, y, z or 0.]

    def __repr__(self):
        return "%s(%s, %s, %g)" % (self.__class__.__name__, self.x, self.y, self.z)

    def __str__(self):
        return "%s(%g, %g, %g)" % (self.__class__.__name__, self.x, self.y, self.z)

    @property
    def x(self):
        return self._v[0]

    @property
    def y(self):
        return self._v[1]

    @property
    def z(self):
        return self._v[2]

    @x.setter
    def x(self, x):
        self._v[0] = x

    @y.setter
    def y(self, x):
        self._v[1] = x

    @z.setter
    def z(self, x):
        self._v[2] = x

    def set(self, x=None, y=None, z=None):
        if x is None:
            self._v = [0., 0., 0.]
        else:
            if y is None:
                self._v = [x[0], x[1], x[2]]
            else:
                self._v = [x, y, z or 0.]

    # --- copy ---

    def __copy__(self):
        return self.__class__(self.x, self.y, self.z)

    def copy(self):
        return self.__copy__()

    # --- list-like ---

    def __len__(self):
        return 3

    def __getitem__(self, i):
        return self._v[i]

    def __setitem__(self, i):
        return self._v[i]

    def __iter__(self):
        return iter(self._v)

    def __contains__(self, item):
        return item in self._v

    # --- boolean equality ---

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._v == other._v
        try:
            if len(other) != len(self):
                return False

            return self._v[0] == other[0] \
                and self._v[1] == other[1] \
                and self._v[2] == other[2]
        except TypeError:
            return False

    # --- unary ---

    def __round__(self, n=None):
        if n is None:
            return self.__class__(
                round(self._v[0]),
                round(self._v[1]),
                round(self._v[2]),
            )
        else:
            return self.__class__(
                round(self._v[0], n),
                round(self._v[1], n),
                round(self._v[2], n),
            )

    # ----- getter -----

    def length(self):
        """
        Returns cartesian length of vector

        :return: float
        >>> Vec3(5,0,0).length()
        5.0
        >>> Vec3(1).length() == math.sqrt(3.)
        True
        """
        return math.sqrt(
            self._v[0] * self._v[0] + self._v[1] * self._v[1] + self._v[2] * self._v[2]
        )

    def length_squared(self):
        """
        Returns the square of the cartesian length of vector

        :return: float
        >>> Vec3(5,0,0).length_squared()
        25.0
        >>> Vec3(1).length_squared()
        3.0
        """
        return self._v[0] * self._v[0] + self._v[1] * self._v[1] + self._v[2] * self._v[2]

    def distance(self, vec3: Sequence):
        """
        Returns the cartesian distance between self and other vector

        :param vec3: float sequence of length 3
        :return: float
        >>> Vec3((5,0,0)).distance(Vec3(0))
        5.0
        >>> Vec3(1).distance(Vec3(2)) == math.sqrt(3)
        True
        """
        dx = self._v[0] - vec3[0]
        dy = self._v[1] - vec3[1]
        dz = self._v[2] - vec3[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def distance_squared(self, vec3: Sequence):
        """
        Returns the square of the cartesian distance between self and other vector

        :param vec3: float sequence of length 3
        :return: float

        >>> Vec3(5,0,0).distance_squared(Vec3(0))
        25.0
        >>> Vec3(1).distance_squared(Vec3(2))
        3.0
        """
        dx = self._v[0] - vec3[0]
        dy = self._v[1] - vec3[1]
        dz = self._v[2] - vec3[2]
        return dx * dx + dy * dy + dz * dz

    def dot(self, vec3: Sequence):
        """
        Returns the dot product of self and other vec3

        :param arg3: float sequence of length 3
        :return: float

        >>> Vec3(1,2,3).dot((4,5,6)) # (1*4)+(2*5)+(3*6)
        32.0
        """
        return self._v[0] * vec3[0] + self._v[1] * vec3[1] + self._v[2] * vec3[2]

    # ------ inplace methods -------

    def round(self, n=None):
        """
        Rounds the vector INPLACE

        :param n: optional, number of digits
        :return: self
        
        >>> Vec3(1.2, 1.5, 1.7).round()
        Vec3(1, 2, 2)
        """
        if n is None:
            self._v[0] = round(self._v[0])
            self._v[1] = round(self._v[1])
            self._v[2] = round(self._v[2])
        else:
            self._v[0] = round(self._v[0], n)
            self._v[1] = round(self._v[1], n)
            self._v[2] = round(self._v[2], n)

    def cross(self, vec3: Sequence):
        """
        Makes this vector the cross-product of this and arg3, INPLACE
        The cross product is always perpendicular to the plane described by the two vectors

        :param vec3: float sequence of length 3
        :return: self

        >>> Vec3(1,0,0).cross((0,1,0))
        Vec3(0, 0, 1)
        >>> Vec3(1,0,0).cross((0,0,1))
        Vec3(0, -1, 0)
        >>> Vec3(0,1,0).cross((0,0,1))
        Vec3(1, 0, 0)
        """
        self._v = [
            self.y * vec3[2] - self.z * vec3[1],
            self.z * vec3[0] - self.x * vec3[2],
            self.x * vec3[1] - self.y * vec3[0],
        ]
        return self

    def reflect(self, vec3: Sequence):
        """
        Reflects this vector on a plane with given normal, INPLACE

        :param vec3: float sequence of length 3
        :return: self

        Example: suppose ray coming from top-left, going down on a flat plane
        >>> Vec3(2, -1, 0).reflect((0,1,0)).round()
        Vec3(2, 1, 0)
        """
        self.set(self - Vec3(vec3) * self.dot(vec3) * 2.)
        return self

    def rotate_x(self, degree: float):
        """
        Rotates this vector around the x-axis, INPLACE

        :param degree: the degrees [0., 360.]
        :return: self

        >>> Vec3(1,2,3).rotate_x(90).round()
        Vec3(1, -3, 2)
        """
        degree *= const.DEG_TO_TWO_PI
        sa = math.sin(degree)
        ca = math.cos(degree)
        y = self.y * ca - self.z * sa
        self.z = self.y * sa + self.z * ca
        self.y = y
        return self

    def rotate_y(self, degree):
        """
        Rotates this vector around the y-axis, INPLACE
        
        :param degree: the degrees [0., 360.]
        :return: self
        
        >>> Vec3(1,2,3).rotate_y(90).round()
        Vec3(3, 2, -1)
        """
        degree *= const.DEG_TO_TWO_PI
        sa = math.sin(degree)
        ca = math.cos(degree)
        x = self.x * ca + self.z * sa
        self.z = -self.x * sa + self.z * ca
        self.x = x
        return self

    def rotate_z(self, degree):
        """
        Rotates this vector around the z-axis, INPLACE
        
        :param degree: the degrees [0., 360.]
        :return: self
        
        >>> Vec3(1,2,3).rotate_z(90).round()
        Vec3(-2, 1, 3)
        """
        degree *= const.DEG_TO_TWO_PI
        sa = math.sin(degree)
        ca = math.cos(degree)
        x = self.x * ca - self.y * sa
        self.y = self.x * sa + self.y * ca
        self.x = x
        return self

    def rotate_axis(self, axis: Sequence, degree: float):
        """
        Rotates this vector around an arbitrary axis, INPLACE
        
        :param axis: float sequence of length 3
        :param degree: the degrees [0., 360.]
        :return: self
        
        >>> Vec3(1,2,3).rotate_axis((1,0,0), 90) == Vec3(1,2,3).rotate_x(90)
        True
        """
        degree *= const.DEG_TO_TWO_PI
        si = math.sin(degree)
        co = math.cos(degree)

        m = axis[0] * axis[0]+ axis[1] * axis[1] + axis[2] * axis[2]
        ms = math.sqrt(m)

        x = (axis[0] * (axis[0] * self.x + axis[1] * self.y + axis[2] * self.z)
             + co * (self.x * (axis[1] * axis[1] + axis[2] * axis[2]) + axis[0] * (-axis[1] * self.y - axis[2] * self.z))
             + si * ms * (-axis[2] * self.y + axis[1] * self.z)) / m
        y = (axis[1] * (axis[0] * self.x + axis[1] * self.y + axis[2] * self.z)
             + co * (self.y * (axis[0] * axis[0] + axis[2] * axis[2]) + axis[1] * (-axis[0] * self.x - axis[2] * self.z))
             + si * ms * (axis[2] * self.x - axis[0] * self.z)) / m
        self.z = (axis[2] * (axis[0] * self.x + axis[1] * self.y + axis[2] * self.z)
                  + co * (self.z * (axis[0] * axis[0] + axis[1] * axis[1]) + axis[2] * (-axis[0] * self.x - axis[1] * self.y))
                  + si * ms * (-axis[1] * self.x + axis[0] * self.y)) / m
        self.x = x
        self.y = y
        return self

    # --- value-copying methods ---

    def crossed(self, vec3: Sequence):
        """
        Returns the cross-product of this vector and arg3
        The cross product is always perpendicular to the plane described by the two vectors
        
        :param vec3: float sequence of length 3
        :return: self
        
        >>> Vec3(1,0,0).crossed((0,1,0))
        Vec3(0, 0, 1)
        >>> Vec3(1,0,0).crossed((0,0,1))
        Vec3(0, -1, 0)
        >>> Vec3(0,1,0).crossed((0,0,1))
        Vec3(1, 0, 0)
        """
        return self.copy().cross(vec3)

    def reflected(self, norm: Sequence):
        """
        Returns the this vector reflected on a plane with given normal

        :param norm: float sequence of length 3
        :return: self

        Example: suppose ray coming from top-left, going down on a flat plane
        >>> Vec3(2,-1,0).reflected((0,1,0)).rounded()
        Vec3(2, 1, 0)
        """
        return self.copy().reflect(norm)

    def rotated_x(self, degree: float):
        """
        Returns this vector rotated around the x-axis

        :param degree: the degrees [0., 360.]
        :return: vec3

        >>> Vec3(1,2,3).rotated_x(90).rounded()
        Vec3(1, -3, 2)
        """
        return self.copy().rotate_x(degree)

    def rotated_y(self, degree: float):
        """
        Returns this vector rotated around the y-axis

        :param degree: the degrees [0., 360.]
        :return: vec3

        >>> Vec3(1,2,3).rotated_y(90).rounded()
        Vec3(3, 2, -1)
        """
        return self.copy().rotate_y(degree)

    def rotated_z(self, degree: float):
        """
        Returns this vector rotated around the z-axis

        :param degree: the degrees [0., 360.]
        :return: vec3

        >>> Vec3(1,2,3).rotated_z(90).rounded()
        Vec3(-2, 1, 3)
        """
        return self.copy().rotate_z(degree)

    def rotated_axis(self, axis: Sequence, degree: float):
        """
        Returns this vector rotated around an arbitrary axis

        :param axis: float sequence of length 3
        :param degree: the degrees [0., 360.]
        :return: vec3

        >>> Vec3(1,2,3).rotated_axis((1,0,0), 90) == Vec3(1,2,3).rotated_x(90)
        True
        """
        return self.copy().rotate_axis(axis, degree)
