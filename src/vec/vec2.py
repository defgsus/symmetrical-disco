import math
from copy import copy

from . import const
from .types import *
from .vec2_operators import Vec2Operators


class Vec2(Vec2Operators):

    def __init__(
            self,
            x: Union[Vector2, Number] = None,
            y: Optional[Number] = None,
    ):
        """
        Creates a new Vec2.

        Examples:

        >>> Vec2()
        Vec2(0.0, 0.0)
        >>> Vec2(3)
        Vec2(3.0, 3.0)
        >>> Vec2(1, 2)
        Vec2(1.0, 2.0)
        >>> Vec2([1, 2])
        Vec2(1.0, 2.0)

        :param x:
            Can be a ``number`` or a ``sequence of numbers``.

        :param y:
            A ``number``
        """
        if x is None:
            self._v = [0., 0.]
        else:
            if y is None:
                if isinstance(x, (int, float)):
                    x = float(x)
                    self._v = [x, x]
                else:
                    self._v = [float(x[0]), float(x[1])]
            else:
                self._v = [float(x), float(y)]

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.x, self.y)

    def __str__(self):
        return "%s(%g, %g)" % (self.__class__.__name__, self.x, self.y)

    @property
    def x(self):
        return self._v[0]

    @property
    def y(self):
        return self._v[1]

    @x.setter
    def x(self, x):
        self._v[0] = x

    @y.setter
    def y(self, x):
        self._v[1] = x

    def set(
            self,
            x: Union[Vector2, Number] = None,
            y: Optional[Number] = None,
    ):
        if x is None:
            self._v = [0., 0.]
        else:
            if y is None:
                if isinstance(x, (int, float)):
                    self._v = [x, x]
                else:
                    self._v = [x[0], x[1]]
            else:
                self._v = [x, y]

    # --- copy ---

    def __copy__(self):
        return self.__class__(self._v[0], self._v[1])

    def copy(self):
        return self.__copy__()

    # --- list-like ---

    def __len__(self):
        return 2

    def __getitem__(self, i: int):
        return self._v[i]

    def __setitem__(self, i: int):
        return self._v[i]

    def __iter__(self):
        return iter(self._v)

    def __contains__(self, item: Number):
        return item in self._v

    # --- boolean equality ---

    def __eq__(self, other: Vector2):
        if isinstance(other, self.__class__):
            return self._v == other._v
        try:
            if len(other) != len(self):
                return False

            return self._v[0] == other[0] \
                and self._v[1] == other[1]
        except TypeError:
            return False

    # --- unary ---

    def __round__(self, n: Optional[int] = None):
        if n is None:
            return self.__class__(
                round(self._v[0]),
                round(self._v[1]),
            )
        else:
            return self.__class__(
                round(self._v[0], n),
                round(self._v[1], n),
            )

    # ----- getter -----

    def length(self):
        """
        Returns cartesian length of vector

        :return: float
        >>> Vec2(5,0).length()
        5.0
        >>> Vec2(1).length() == math.sqrt(2.)
        True
        """
        return math.sqrt(
            self._v[0] * self._v[0] + self._v[1] * self._v[1]
        )

    def length_squared(self):
        """
        Returns the square of the cartesian length of vector

        :return: float
        >>> Vec2(5,0).length_squared()
        25.0
        >>> Vec2(1).length_squared()
        2.0
        """
        return self._v[0] * self._v[0] + self._v[1] * self._v[1]

    def distance(self, vec2: Vector2):
        """
        Returns the cartesian distance between self and other vector

        :param vec2: float sequence of length 2
        :return: float
        >>> Vec2(5,0).distance(Vec2())
        5.0
        >>> Vec2(1).distance(Vec2(2)) == math.sqrt(2)
        True
        """
        dx = self._v[0] - vec2[0]
        dy = self._v[1] - vec2[1]
        return math.sqrt(dx * dx + dy * dy)

    def distance_squared(self, vec2: Vector2):
        """
        Returns the square of the cartesian distance between self and other vector

        :param vec2: float sequence of length 3
        :return: float

        >>> Vec2(5,0).distance_squared(Vec2(0))
        25.0
        >>> Vec2(1).distance_squared(Vec2(2))
        2.0
        """
        dx = self._v[0] - vec2[0]
        dy = self._v[1] - vec2[1]
        return dx * dx + dy * dy

    def dot(self, vec2: Vector2):
        """
        Returns the dot product of self and other vec2

        :param vec2: float sequence of length 2
        :return: float

        >>> Vec2(1,2).dot((4,5)) # (1*4)+(2*5)
        14.0
        """
        return self._v[0] * vec2[0] + self._v[1] * vec2[1]

    # ------ inplace methods -------

    def round(self, n: Optional[int] = None):
        """
        Rounds the vector INPLACE

        :param n: optional, number of digits
        :return: self
        
        >>> Vec2(1.2, 1.5).round()
        Vec2(1, 2)
        """
        if n is None:
            self._v[0] = round(self._v[0])
            self._v[1] = round(self._v[1])
        else:
            self._v[0] = round(self._v[0], n)
            self._v[1] = round(self._v[1], n)
        return self

    def normalize(self):
        """
        Normalizes the vector, e.g. makes it length 1, INPLACE

        :return: self

        >>> Vec2(1,1).normalize().round(6)
        Vec2(0.707107, 0.707107)
        >>> round(Vec2(1,2).normalize().length(), 6) == 1
        True
        """
        l = self.length()
        self._v[0] /= l
        self._v[1] /= l
        return self

    def normalize_safe(self):
        """
        Normalizes the vector, e.g. makes it length 1, INPLACE
        If the length is zero, this call does nothing

        :return: self

        >>> Vec2(1,1).normalize_safe().round(6)
        Vec2(0.707107, 0.707107)
        >>> Vec2(0).normalize_safe()
        Vec2(0.0, 0.0)
        """
        l = self.length()
        if not l == 0.:
            self._v[0] /= l
            self._v[1] /= l
        return self

    # --- value-copying methods ---

    def rounded(self, n: Optional[int] = None):
        """
        Returns rounded vector

        :param n: optional, number of digits
        :return: Vec2

        >>> Vec2(1.2, 1.5).rounded()
        Vec2(1, 2)
        """
        return self.copy().round(n)
