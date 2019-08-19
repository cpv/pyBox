from collections import namedtuple
from typing import List

# provides a base named vector for a point in cartesian space (x,y,z)
# we use these to build up our triangles.
class Vec3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# triangles made up of 3 points in space.
# (each with a Vec3D for x,y,z)
class Tri(object):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

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

#Multiple triangles to make up a mesh
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

    @staticmethod
    def props():
        #defining the window properties.

    @staticmethod
    def projection_matrix():
        w, h = 4, 4
        matrix = [[0 for x in range(w)] for y in range(h)]
        return matrix
        #row + column = 0'd out.

    @staticmethod
    def box_mesh():

        vlist = [
            #front facing tri
            Tri(
                Vec3D(0.0, 0.0, 0.0),
                Vec3D(0.0, 1.0, 0.0),
                Vec3D(1.0, 1.0, 0.0)
            )
            Tri(
                Vec3D(0.0, 0.0, 0.0),
                Vec3D(1.0, 1.0, 0.0),
                Vec3D(1.0, 0.0, 0.0)
            )
        ]

        mesh = Mesh(vlist)

        return mesh
