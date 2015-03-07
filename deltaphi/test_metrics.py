import unittest
import math

from mock import MagicMock
import numpy

from deltaphi.metrics import Discriminant, Characteristic, Separability, Cohesion
from deltaphi.category_info import CategoryInfoBuilder


__author__ = 'Emanuele Tamponi'


class TestMetrics(unittest.TestCase):

    def setUp(self):
        builder = CategoryInfoBuilder(["a", "b", "c"])
        self.ci1 = builder.build_leaf("A", 100, {"a": 60, "c": 80})
        self.ci2 = builder.build_leaf("B", 80, {"b": 30, "c": 50})

    def test_binary_discriminant(self):
        d = Discriminant()
        expected_discriminant = numpy.asarray([60. / 100., -30. / 80., (80. / 100.) - (50. / 80.)])
        numpy.testing.assert_array_equal(expected_discriminant, d.evaluate(self.ci1, self.ci2))

    def test_binary_characteristic(self):
        c = Characteristic()
        expected_characteristic = numpy.asarray([(60. / 100.) - (80. / 80.), -50. / 80., (80. / 100.) - (30. / 80.)])
        numpy.testing.assert_array_equal(expected_characteristic, c.evaluate(self.ci1, self.ci2))

    def test_pairwise_separability(self):
        c = Characteristic()
        c.evaluate = MagicMock(return_value=numpy.asarray([-0.6, -0.1, 0.2, 0.5]))
        d = Discriminant()
        d.evaluate = MagicMock(return_value=numpy.asarray([-0.1, 0.7, -0.6, 0.1]))
        s = Separability(c, d)
        expected_separability = 1. / 2. * ((0.7 - 0.1) + (0.6 - 0.2))
        self.assertEqual(expected_separability, s.evaluate(self.ci1, self.ci2))
        self.assertEqual(expected_separability, s.evaluate(self.ci2, self.ci1))

    def test_pairwise_cohesion(self):
        c = Characteristic()
        c.evaluate = MagicMock(return_value=numpy.asarray([-0.6, -0.1, 0.2, 0.5]))
        d = Discriminant()
        d.evaluate = MagicMock(return_value=numpy.asarray([-0.1, 0.7, -0.1, 0.1]))
        coh = Cohesion(c, d)
        expected_cohesion = 1. / 2. * (math.sqrt(0.2**2 + 0.1**2) + math.sqrt(0.5**2 + 0.1**2))
        self.assertEqual(expected_cohesion, coh.evaluate(self.ci1, self.ci2))
        self.assertEqual(expected_cohesion, coh.evaluate(self.ci2, self.ci1))
