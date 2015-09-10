import unittest

import numpy

from deltaphi.fake_entities import FakePhiDelta, FakeCategoryInfo
from deltaphi.metrics import Discriminant, Characteristic, Separability, Cohesion, CharacteristicTerms, \
    DiscriminantTerms, LookAhead
from deltaphi.category_info import CategoryInfoFactory, CategoryGroup, RawCategoryInfo, CategoryLayer

__author__ = 'Emanuele Tamponi'


DISC = [0.0, 1.0]
CHAR = [1.0, 0.0]


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
        numpy.testing.assert_array_almost_equal(-expected_discriminant, d.pairwise_evaluate(self.ci2, self.ci1))

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
        expected_separability = 0.60
        self.assertAlmostEqual(expected_separability, sep.evaluate(CategoryGroup([self.ci1, self.ci2, self.ci3])), 2)

    def test_pairwise_cohesion(self):
        coh = Cohesion()
        expected_cohesion = 0.71
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci1, self.ci2])), 2)
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci2, self.ci1])), 2)

    def test_cohesion(self):
        coh = Cohesion()
        expected_cohesion = 0.51
        self.assertAlmostEqual(expected_cohesion, coh.evaluate(CategoryGroup([self.ci1, self.ci2, self.ci3])), 2)

    def test_fake_phi_delta(self):
        ci1 = FakeCategoryInfo("A", 3)
        ci2 = FakeCategoryInfo("B", 3)
        phi_delta_map = {
            (ci1, ci2): numpy.asarray([
                [0.7, 0.2],
                [0.1, 0.5],
                [0.6, 0.2]
            ])
        }
        fpd = FakePhiDelta()
        fpd.add_phi_delta_mapping(phi_delta_map)
        numpy.testing.assert_array_equal(phi_delta_map[(ci1, ci2)], fpd.pairwise_evaluate(ci1, ci2))
        # Automatic inversion of delta
        numpy.testing.assert_array_equal(
            numpy.asarray([
                [0.7, -0.2],
                [0.1, -0.5],
                [0.6, -0.2]
            ]), fpd.pairwise_evaluate(ci2, ci1)
        )

    def test_characteristic_terms(self):
        ci1 = FakeCategoryInfo("A", 3)
        ci2 = FakeCategoryInfo("B", 3)
        ci3 = FakeCategoryInfo("C", 3)
        ci12 = CategoryGroup([ci1, ci2]).build_parent_info()
        ci13 = CategoryGroup([ci1, ci3]).build_parent_info()
        ci23 = CategoryGroup([ci2, ci3]).build_parent_info()
        phi_delta_map = {
            (ci1, ci23): [
                [1.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0]
            ],
            (ci2, ci13): [
                [0.0, 1.0],
                [1.0, 0.0],
                [1.0, 0.0]
            ],
            (ci3, ci12): [
                [0.0, 1.0],
                [1.0, 0.0],
                [1.0, 0.0]
            ]
        }
        fpd = FakePhiDelta()
        fpd.add_phi_delta_mapping(phi_delta_map)
        ct = CharacteristicTerms(phi_delta=fpd)
        numpy.testing.assert_array_equal(numpy.asarray([0, 1, 1]), ct.evaluate(CategoryGroup([ci1, ci2, ci3])))

    def test_discriminant_terms(self):
        ci1 = FakeCategoryInfo("A", 4)
        ci2 = FakeCategoryInfo("B", 4)
        ci3 = FakeCategoryInfo("C", 4)
        ci12 = CategoryGroup([ci1, ci2]).build_parent_info()
        ci13 = CategoryGroup([ci1, ci3]).build_parent_info()
        ci23 = CategoryGroup([ci2, ci3]).build_parent_info()
        phi_delta_map = {
            (ci1, ci23): [
                DISC, DISC, CHAR, CHAR
            ],
            (ci2, ci13): [
                DISC, CHAR, CHAR, DISC
            ],
            (ci3, ci12): [
                DISC, CHAR, DISC, CHAR
            ]
        }
        fpd = FakePhiDelta()
        fpd.add_phi_delta_mapping(phi_delta_map)
        dt = DiscriminantTerms(phi_delta=fpd).evaluate(CategoryLayer.build_closed_layer([ci1, ci2, ci3]))
        numpy.testing.assert_array_equal(numpy.asarray([1, 1, 0, 0]), dt[ci1])
        numpy.testing.assert_array_equal(numpy.asarray([1, 0, 0, 1]), dt[ci2])
        numpy.testing.assert_array_equal(numpy.asarray([1, 0, 1, 0]), dt[ci3])

    def test_look_ahead(self):
        ci1 = FakeCategoryInfo("A", 4)
        ci2 = FakeCategoryInfo("B", 4)
        ci3 = FakeCategoryInfo("C", 4)
        ci4 = FakeCategoryInfo("D", 4)
        g12 = CategoryGroup([ci1, ci2])
        g34 = CategoryGroup([ci3, ci4])
        ci12 = g12.build_parent_info()
        ci34 = g34.build_parent_info()
        phi_delta_map = {
            (ci1, ci2): [
                DISC, CHAR, CHAR, CHAR
            ],
            (ci3, ci4): [
                DISC, DISC, CHAR, CHAR
            ],
            (ci12, ci34): [
                DISC, DISC, DISC, CHAR
            ]
        }
        fpd = FakePhiDelta()
        fpd.add_phi_delta_mapping(phi_delta_map)
        ct = CharacteristicTerms(phi_delta=fpd)
        dt = DiscriminantTerms(phi_delta=fpd)
        lh = LookAhead(ct, dt).evaluate(CategoryLayer([g12, g34]).build_parent())
        self.assertEqual(3, lh)
        lh = LookAhead(ct, dt).evaluate(CategoryLayer([g12]).build_parent())
        self.assertEqual(0, lh)
