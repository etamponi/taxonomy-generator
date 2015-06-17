import unittest

import numpy

from deltaphi.soft_shapes import Gaussian

__author__ = 'Emanuele'


class TestSoftShapes(unittest.TestCase):

    def test_gaussian(self):
        g = Gaussian([1, 0], 1)
        points = numpy.asarray([[4.0, 4.0], [3, 0], [1, 3]])
        expected_values = numpy.exp(-0.5 * numpy.asarray([5.0, 2.0, 3.0])**2)
        numpy.testing.assert_array_equal(expected_values, g.contains(points))

    def test_shape_union(self):
        shape = Gaussian([1, 0], 1) | Gaussian([0, 1], 1)
        points = numpy.asarray([[4.0, 4.0], [3, 0], [1, 3]])
        expected_values = numpy.max([
            numpy.exp(-0.5 * numpy.asarray([5.0, 2.0, 3.0])**2),
            numpy.exp(-0.5 * numpy.asarray([25.0, 10.0, 5.0]))
        ], axis=0)
        numpy.testing.assert_array_equal(expected_values, shape.contains(points))
