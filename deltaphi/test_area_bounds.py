import unittest
import numpy
from deltaphi.area_bounds import CheckerBoard

__author__ = 'Emanuele Tamponi'


class TestAreaBounds(unittest.TestCase):

    def test_checker_board(self):
        area = CheckerBoard("up")
        numpy.testing.assert_array_equal(
            [1, 1, 1, 1, 0, 0],
            area.is_inside(
                phis=numpy.asarray([0.0, 0.5, 0.0, -0.5, 0.5, -0.5]),
                deltas=numpy.asarray([1.0, 0.5, 0.0, 0.5, 0.0, 0.0])
            )
        )
        area = CheckerBoard("left")
        numpy.testing.assert_array_equal(
            [1, 0],
            area.is_inside(
                phis=numpy.asarray([-0.5, 0.5]),
                deltas=numpy.asarray([0.0, 0.0])
            )
        )
