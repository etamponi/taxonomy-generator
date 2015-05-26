import unittest

import numpy

from deltaphi import shapes

__author__ = 'Emanuele'


class TestShapes(unittest.TestCase):

    def setUp(self):
        self.shape_checks = [
            {
                'shape': shapes.PSphere(center=numpy.asarray([0.0, 0.0]), radius=1, p=1),
                'points_inside': numpy.asarray((
                    (1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0), (0.5, 0.5), (-0.5, -0.5)
                )),
                'points_outside': numpy.asarray((
                    (1.0, 1.0), (-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0)
                ))
            },
            {
                'shape': shapes.PSphere(
                    center=numpy.asarray([1.0, 0.0]), radius=0.5, p=1
                ) | shapes.PSphere(
                    center=numpy.asarray([-1.0, 0.0]), radius=0.5, p=1
                ),
                'points_inside': numpy.asarray((
                    (1.0, 0.0), (0.5, 0.0), (-1.0, 0.0), (-0.5, 0.0)
                )),
                'points_outside': numpy.asarray((
                    (0.0, 1.0), (0.0, -1.0), (0.0, 0.5), (0.0, -0.5)
                ))
            },
            {
                'shape': shapes.PSphere(
                    center=numpy.asarray([0.5, 0.0]), radius=1, p=1
                ) & shapes.PSphere(
                    center=numpy.asarray([-0.5, 0.0]), radius=1, p=1
                ),
                'points_inside': numpy.asarray((
                    (0.0, 0.0), (0.5, 0.0), (-0.5, 0.0), (0.0, 0.5)
                )),
                'points_outside': numpy.asarray((
                    (1.0, 0.0), (-1.0, 0.0)
                ))
            }
        ]

    def test_is_inside(self):
        for shape_check in self.shape_checks:
            shape = shape_check['shape']
            inside = shape_check['points_inside']
            outside = shape_check['points_outside']
            numpy.testing.assert_array_equal(numpy.ones(len(inside)), shape.contains(inside))
            numpy.testing.assert_array_equal(numpy.zeros(len(outside)), shape.contains(outside))
