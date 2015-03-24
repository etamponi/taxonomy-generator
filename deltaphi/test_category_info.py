import unittest

import numpy

from deltaphi.category_info import CategoryInfoFactory, CategoryGroup, RawCategoryInfo


__author__ = 'Emanuele Tamponi'


class TestCategoryInfo(unittest.TestCase):

    def setUp(self):
        self.builder = CategoryInfoFactory({"a", "b", "c"})

    def test_build_leaf(self):
        ci = self.builder.build(RawCategoryInfo("Name", 100, {"a": 10, "b": 30, "c": 80}))
        self.assertIsInstance(ci.frequencies, numpy.ndarray)
        self.assertEqual("Name", ci.category)
        self.assertEqual(100, ci.documents)
        self.assertEqual(None, ci.children)
        numpy.testing.assert_array_equal([10, 30, 80], ci.frequencies)

    def test_build_parent_pairwise(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        merged = CategoryGroup([ci1, ci2]).build_parent_info()
        numpy.testing.assert_array_equal([50, 40, 100], merged.frequencies)
        self.assertEqual("(C1+C2)", merged.category)
        self.assertEqual(180, merged.documents)
        self.assertEqual(CategoryGroup([ci1, ci2]), merged.children)

    def test_build_parent_multiple(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        ci3 = self.builder.build(RawCategoryInfo("C3", 130, {"a": 20, "b": 20, "c": 30}))
        merged = CategoryGroup([ci1, ci2, ci3]).build_parent_info()
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("(C1+C2+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual(CategoryGroup([ci1, ci2, ci3]), merged.children)

    def test_hierarchical_build_node(self):
        ci1 = self.builder.build(RawCategoryInfo("C1", 100, {"a": 50, "c": 80}))
        ci2 = self.builder.build(RawCategoryInfo("C2", 80, {"b": 40, "c": 20}))
        ci3 = self.builder.build(RawCategoryInfo("C3", 130, {"a": 20, "b": 20, "c": 30}))
        middle = CategoryGroup([ci1, ci2]).build_parent_info()
        merged = CategoryGroup([ci3, middle]).build_parent_info()
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("((C1+C2)+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual(CategoryGroup([ci3, middle]), merged.children)
