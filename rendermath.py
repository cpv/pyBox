from collections import namedtuple
from math import tan, pi
from typing import List


# provides a base named vector for a point in cartesian space (x,y,z)
# we use these to build up our triangles.


class Vec3D(object):

    def __str__(self):
        return 'x:' + str(self.x) + ' y:' + str(self.y) + ' z:' + str(self.z)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# triangles made up of 3 points in space.
# (each with a Vec3D for x,y,z)


class Tri(object):

    def __str__(self):
        return 'p1:' + self.p1.__str__() + ' p2:' + self.p2.__str__() + ' p3:' + self.p3.__str__()

    def __init__(self, p1=Vec3D(0, 0, 0), p2=Vec3D(0, 0, 0), p3=Vec3D(0, 0, 0), colour="#fb0"):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.colour = colour

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, value):
        if not isinstance(value, Vec3D):
            raise TypeError('Tri.p1 must be instance of Vec3D')
        self._p1 = value

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, value):
        if not isinstance(value, Vec3D):
            raise TypeError('Tri.p2 must be instance of Vec3D')
        self._p2 = value

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, value):
        if not isinstance(value, Vec3D):
            raise TypeError('Tri.p3 must be instance of Vec3D')
        self._p3 = value

# Multiple triangles to make up a mesh


class Mesh(object):
    def __init__(self, vector):
        self.vector = vector

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        if not isinstance(value, List):
            raise TypeError('Mesh.Vector must be instance of List[Tri]')
        self._vector = value


class RenderMath(object):

    fnear = 0.1
    ffar = 1000.0
    ffov = 90.0

    fScreenWidth = 500.0
    fScreenHeight = 500.0
    faspectRatio = fScreenHeight/fScreenWidth
    ffovRad = 1.0 / tan(ffov * 0.5/180 * pi)
    matrix = []

    def __init__(self):
        # black boxy projection matrix to do with projecting out 3d points
        # to a space on a 2d plane. We use this primarily for our matrix multiplication.

        w, h = 4, 4
        self.matrix = [[0 for x in range(w)] for y in range(h)]

        self.matrix[0][0] = self.faspectRatio * self.ffovRad
        self.matrix[1][1] = self.ffovRad
        self.matrix[2][2] = self.ffar / (self.ffar - self.fnear)
        self.matrix[3][2] = (-self.ffar * self.fnear)/(self.ffar - self.fnear)
        self.matrix[2][3] = 1
        self.matrix[3][3] = 0

    # m: matrix vector
    # k: 3d vec 1
    # o: 3d vec 2
    @staticmethod
    def multiplyMatrixVector(k: Vec3D, o: Vec3D, m: List[List]):

        o.x = k.x * m[0][0] + k.y * m[1][0] + k.z * m[2][0] + m[3][0]
        o.y = k.x * m[0][1] + k.y * m[1][1] + k.z * m[2][1] + m[3][1]
        o.z = k.x * m[0][2] + k.y * m[1][2] + k.z * m[2][2] + m[3][2]
        w = float(k.x * m[0][3] + k.y * m[1][3] + k.z * m[2][3] + m[3][3])
        # need to normalise back to cartesian space.

        # print(o.x, o.y, o.z, sep=' ')
        if(w != 0.0):
            o.x /= w
            o.y /= w
            o.z /= w

    @staticmethod
    def box_mesh():

        vlist = [
            # front facing tri
            Tri(
                Vec3D(0.0, 0.0, 0.0),
                Vec3D(0.0, 1.0, 0.0),
                Vec3D(1.0, 1.0, 0.0),
                colour="#de4c28"
            ),
            Tri(
                Vec3D(1.0, 0.0, 0.0),
                Vec3D(1.0, 1.0, 0.0),
                Vec3D(1.0, 0.0, 0.0),
                colour="#de4c28"
            ),

            # east facing tri
            Tri(
                Vec3D(1.0, 0.0, 0.0),
                Vec3D(1.0, 1.0, 0.0),
                Vec3D(1.0, 1.0, 1.0),
                colour="#3498eb"

            ),
            Tri(
                Vec3D(1.0, 0.0, 0.0),
                Vec3D(1.0, 1.0, 1.0),
                Vec3D(1.0, 0.0, 1.0),
                colour="#3498eb"

            ),
            # north facing tri
            Tri(
                Vec3D(1.0, 0.0, 1.0),
                Vec3D(1.0, 1.0, 1.0),
                Vec3D(0.0, 1.0, 1.0),
            ),
            Tri(
                Vec3D(1.0, 0.0, 1.0),
                Vec3D(0.0, 1.0, 1.0),
                Vec3D(0.0, 0.0, 1.0)
            ),

            # west facing tri
            Tri(
                Vec3D(0.0, 0.0, 1.0),
                Vec3D(0.0, 1.0, 1.0),
                Vec3D(0.0, 1.0, 0.0)
            ),
            Tri(
                Vec3D(0.0, 0.0, 1.0),
                Vec3D(0.0, 1.0, 0.0),
                Vec3D(0.0, 0.0, 0.0)
            ),

            # top facing tri
            Tri(
                Vec3D(0.0, 1.0, 0.0),
                Vec3D(0.0, 1.0, 1.0),
                Vec3D(1.0, 1.0, 1.0)
            ),
            Tri(
                Vec3D(0.0, 1.0, 0.0),
                Vec3D(1.0, 1.0, 1.0),
                Vec3D(1.0, 1.0, 0.0)
            ),
            # bottom facing tri
            Tri(
                Vec3D(1.0, 0.0, 1.0),
                Vec3D(0.0, 0.0, 1.0),
                Vec3D(0.0, 0.0, 0.0),
                colour="#2cfc03"

            ),
            Tri(
                Vec3D(1.0, 0.0, 1.0),
                Vec3D(0.0, 0.0, 0.0),
                Vec3D(1.0, 0.0, 0.0),
                colour="#2cfc03"

            ),

        ]

        mesh = Mesh(vlist)

        return mesh
