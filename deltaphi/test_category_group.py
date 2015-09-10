import unittest

import numpy

from deltaphi.category_info import RawCategoryInfo, CategoryGroup, CategoryInfoFactory
from deltaphi.fake_entities import FakeCategoryInfo

__author__ = 'Emanuele Tamponi'


class TestCategoryGroup(unittest.TestCase):

    def setUp(self):
        self.builder = CategoryInfoFactory({"a", "b", "c"})

    def test_build_parent_pairwise(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        merged = CategoryGroup([ci1, ci2]).build_parent_info()
        numpy.testing.assert_array_equal([50, 40, 100], merged.frequencies)
        self.assertEqual("(C1+C2)", merged.category)
        self.assertEqual(180, merged.documents)
        self.assertEqual(CategoryGroup([ci1, ci2]), merged.child_group)

    def test_build_parent_multiple(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        ci3 = self.builder.build(RawCategoryInfo("C3", 130, {"a": 20, "b": 20, "c": 30}))
        merged = CategoryGroup([ci1, ci2, ci3]).build_parent_info()
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("(C1+C2+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual(CategoryGroup([ci1, ci2, ci3]), merged.child_group)

    def test_hierarchical_build_node(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        ci3 = self.builder.build(RawCategoryInfo("C3", 130, {"a": 20, "b": 20, "c": 30}))
        middle = CategoryGroup([ci1, ci2]).build_parent_info()
        merged = CategoryGroup([ci3, middle]).build_parent_info()
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("((C1+C2)+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual(CategoryGroup([ci3, middle]), merged.child_group)

    def test_category_group_one_vs_siblings(self):
        ci1 = FakeCategoryInfo("C1", 4)
        ci2 = FakeCategoryInfo("C2", 4)
        ci3 = FakeCategoryInfo("C3", 4)
        expected_info_pair = [
            (ci1, CategoryGroup([ci2, ci3]).build_parent_info()),
            (ci2, CategoryGroup([ci1, ci3]).build_parent_info()),
            (ci3, CategoryGroup([ci1, ci2]).build_parent_info())
        ]
        group = CategoryGroup([ci1, ci2, ci3])
        for expected_info_pair, actual_info_pair in zip(expected_info_pair, group.one_vs_siblings()):
            self.assertEqual(expected_info_pair[0], actual_info_pair[0])
            self.assertEqual(expected_info_pair[1], actual_info_pair[1])

    def test_leafs(self):
        ci1 = FakeCategoryInfo("C1", 4)
        ci2 = FakeCategoryInfo("C2", 4)
        ci3 = FakeCategoryInfo("C3", 4)
        ci4 = FakeCategoryInfo("C4", 4)
        ci12 = CategoryGroup([ci1, ci2]).build_parent_info()
        ci34 = CategoryGroup([ci3, ci4]).build_parent_info()
        g12 = CategoryGroup([ci12])
        g34 = CategoryGroup([ci34])
        expected_leafs = [ci1, ci2]
        self.assertEqual(expected_leafs, g12.leafs())
        expected_leafs = [ci3, ci4]
        self.assertEqual(expected_leafs, g34.leafs())
        ci1234 = CategoryGroup([ci12, ci34]).build_parent_info()
        g1234 = CategoryGroup([ci1234])
        expected_leafs = [ci1, ci2, ci3, ci4]
        self.assertEqual(expected_leafs, g1234.leafs())
