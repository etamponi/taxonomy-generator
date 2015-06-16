import numpy
from scipy.spatial import distance

from deltaphi.metrics import PhiDelta, IntegralMetric

__author__ = 'Emanuele'


class SoftShape(object):

    def contains(self, points):
        pass

    def __or__(self, other):
        return SoftShapeUnion(self, other)


class SoftShapeUnion(SoftShape):

    def __init__(self, a, b):
        """
        :type a: SoftShape | SoftShapeUnion
        :type b: SoftShape | SoftShapeUnion
        """
        self.shapes = a.shapes if isinstance(a, SoftShapeUnion) else [a]
        self.shapes += b.shapes if isinstance(b, SoftShapeUnion) else [b]

    def contains(self, points):
        return numpy.mean([shape.contains(points) for shape in self.shapes], axis=0)


class Gaussian(SoftShape):

    def __init__(self, center, precision):
        self.center = numpy.asarray(center)
        self.precision = precision

    def contains(self, points):
        distances = distance.cdist([self.center], points, metric="sqeuclidean")[0]
        return numpy.exp(-0.5 * self.precision * distances)


class SoftIntegralMetric(IntegralMetric):

    COHESION_AREA = Gaussian([1, 0], 1)
    SEPARABILITY_AREA = Gaussian([0, 1], 1) | Gaussian([1, 0], 1)

    def __init__(self, area, phi_delta=PhiDelta()):
        super(SoftIntegralMetric, self).__init__(area, phi_delta)

    def integrate(self, points, inside):
        return numpy.mean(inside)
