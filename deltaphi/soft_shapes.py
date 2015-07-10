import numpy
from scipy.spatial import distance

from deltaphi.shapes import Shape

__author__ = 'Emanuele'


class Gaussian(Shape):

    def __init__(self, center, precision):
        self.center = numpy.asarray(center)
        self.precision = precision

    def contains(self, points):
        distances = distance.cdist([self.center], points, metric="sqeuclidean")[0]
        return numpy.exp(-0.5 * self.precision * distances)


SOFT_COHESION_AREA = Gaussian([1, 0], 0.5)
SOFT_SEPARABILITY_AREA = (Gaussian([0, 1], 0.5) | Gaussian([0, -1], 0.5))
