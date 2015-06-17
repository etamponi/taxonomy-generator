import numpy
from scipy.spatial import distance

__author__ = 'Emanuele'


class Shape(object):

    def contains(self, points):
        pass

    def __or__(self, other):
        return ShapeUnion(self, other)

    def __and__(self, other):
        return ShapeIntersection(self, other)


class ShapeGroup(Shape):

    def __init__(self, a, b):
        """
        :type a: Shape | ShapeGroup
        :type b: Shape | ShapeGroup
        """
        self.shapes = a.shapes if isinstance(a, type(self)) else [a]
        self.shapes += b.shapes if isinstance(b, type(self)) else [b]


class ShapeUnion(ShapeGroup):

    def __init__(self, a, b):
        super(ShapeUnion, self).__init__(a, b)

    def contains(self, points):
        return numpy.max([shape.contains(points) for shape in self.shapes], axis=0)


class ShapeIntersection(ShapeGroup):

    def __init__(self, a, b):
        super(ShapeIntersection, self).__init__(a, b)

    def contains(self, points):
        return numpy.prod(numpy.asarray([shape.contains(points) for shape in self.shapes]), axis=0)


class PSphere(Shape):

    def __init__(self, center, radius, p):
        # Represent it as a single row matrix as it has to be used with cdist
        self.center = numpy.asarray([center])
        self.radius = radius
        self.p = p

    def contains(self, points):
        return numpy.asarray(
            distance.cdist(self.center, points, metric='minkowski', p=self.p) <= self.radius, dtype=float
        )[0]
