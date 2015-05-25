import unittest

import numpy

from deltaphi import shapes

__author__ = 'Emanuele'


class TestShapes(unittest.TestCase):

    def setUp(self):
        self.shape_checks = [
            {
                'shape': shapes.Diamond(),
                'points_inside': [
                    (1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0), (0.5, 0.5), (-0.5, -0.5)
                ],
                'points_outside': [
                    (1.0, 1.0), (-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0)
                ]
            }
        ]

    def test_is_inside(self):
        for shape_check in self.shape_checks:
            shape = shape_check['shape']
            inside = shape_check['points_inside']
            outside = shape_check['points_outside']
            numpy.testing.assert_array_equal(numpy.ones(len(inside)), shape.contains(inside))
            numpy.testing.assert_array_equal(numpy.zeros(len(outside)), shape.contains(outside))
