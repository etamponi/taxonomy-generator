import numpy

__author__ = 'Emanuele'


class Shape(object):

    def contains_single(self, point):
        pass

    def contains(self, points):
        return numpy.asarray([self.contains_single(point) for point in points], dtype=int)


class Diamond(Shape):

    def contains_single(self, point):
        return abs(point[0]) + abs(point[1]) <= 1.0
