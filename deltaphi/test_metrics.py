import unittest

import numpy

from deltaphi.metrics import Discriminant, Characteristic, Separability, Cohesion
from deltaphi.category_info import CategoryInfoFactory, CategoryGroup, RawCategoryInfo


__author__ = 'Emanuele Tamponi'


class TestMetrics(unittest.TestCase):

    def setUp(self):
        builder = CategoryInfoFactory({"a", "b", "c", "d"})
        self.ci1 = builder.build(RawCategoryInfo("A", 10, {"a": 9, "b": 1, "c": 2, "d": 9}))
        self.ci2 = builder.build(RawCategoryInfo("A", 10, {"a": 1, "b": 8, "c": 1, "d": 8}))
        self.ci3 = builder.build(RawCategoryInfo("A", 10, {"a": 2, "b": 3, "c": 9, "d": 7}))

    def test_discriminant(self):
        d = Discriminant()
        expected_discriminant = 0.1 * numpy.asarray([8, -7, 1, 1])
        numpy.testing.assert_array_almost_equal(expected_discriminant, d.pairwise_evaluate(self.ci1, self.ci2))

    def test_characteristic(self):
        c = Characteristic()
        expected_characteristic = 0.1 * numpy.asarray([0, -1, -7, 7])
        numpy.testing.assert_array_almost_equal(expected_characteristic, c.pairwise_evaluate(self.ci1, self.ci2))

    def test_pairwise_separability(self):
        s = Separability()
        expected_separability = 0.7
        self.assertAlmostEqual(expected_separability, s.evaluate(CategoryGroup([self.ci1, self.ci2])))
        self.assertAlmostEqual(expected_separability, s.evaluate(CategoryGroup([self.ci2, self.ci1])))

    def test_separability(self):
        sep = Separability()
        expected_cohesion = 0.60
        self.assertAlmostEqual(expected_cohesion, sep.evaluate(CategoryGroup([self.ci1, self.ci2, self.ci3])), 2)

    def test_pairwise_cohesion(self):
        coh = Cohesion()
        expected_cohesion = 0.71
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci1, self.ci2])), 2)
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci2, self.ci1])), 2)

    def test_cohesion(self):
        coh = Cohesion()
        expected_cohesion = 0.51
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci1, self.ci2, self.ci3])), 2)
