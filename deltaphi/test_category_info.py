import unittest

import numpy

from deltaphi.category_info import CategoryInfoBuilder


__author__ = 'Emanuele Tamponi'


class TestCategoryInfo(unittest.TestCase):

    def setUp(self):
        self.builder = CategoryInfoBuilder({"a", "b", "c"})

    def test_build_leaf(self):
        ci = self.builder.build_leaf("Name", 100, {"a": 10, "b": 30, "c": 80})
        self.assertIsInstance(ci.frequencies, numpy.ndarray)
        self.assertEqual("Name", ci.category)
        self.assertEqual(100, ci.documents)
        self.assertEqual(None, ci.children)
        numpy.testing.assert_array_equal([10, 30, 80], ci.frequencies)

    def test_build_parent_pairwise(self):
        ci1 = self.builder.build_leaf("C1", 100, {"a": 50, "c": 80})
        ci2 = self.builder.build_leaf("C2", 80, {"b": 40, "c": 20})
        merged = self.builder.build_parent(ci1, ci2)
        numpy.testing.assert_array_equal([50, 40, 100], merged.frequencies)
        self.assertEqual("(C1+C2)", merged.category)
        self.assertEqual(180, merged.documents)
        self.assertEqual((ci1, ci2), merged.children.categories)

    def test_build_parent_multiple(self):
        ci1 = self.builder.build_leaf("C1", 100, {"a": 50, "c": 80})
        ci2 = self.builder.build_leaf("C2", 80, {"b": 40, "c": 20})
        ci3 = self.builder.build_leaf("C3", 130, {"a": 20, "b": 20, "c": 30})
        merged = self.builder.build_parent(ci1, ci2, ci3)
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("(C1+C2+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual((ci1, ci2, ci3), merged.children.categories)

    def test_hierarchical_build_node(self):
        ci1 = self.builder.build_leaf("C1", 100, {"a": 50, "c": 80})
        ci2 = self.builder.build_leaf("C2", 80, {"b": 40, "c": 20})
        ci3 = self.builder.build_leaf("C3", 130, {"a": 20, "b": 20, "c": 30})
        middle = self.builder.build_parent(ci1, ci2)
        merged = self.builder.build_parent(ci3, middle)
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("((C1+C2)+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual((ci3, middle), merged.children.categories)
