import unittest
import numpy
from deltaphi.category_info import SingleCategoryInfo, MultipleCategoryInfo

__author__ = 'Emanuele Tamponi'


class TestCategoryInfo(unittest.TestCase):

    def test_init(self):
        ci = SingleCategoryInfo("Name", 100, ["a", "b", "c"], [10, 30, 80])
        self.assertIsInstance(ci.frequencies, numpy.ndarray)
        self.assertEqual("Name", ci.category)
        self.assertEqual(100, ci.documents)
        self.assertEqual(set(), ci.children)
        numpy.testing.assert_array_equal([10, 30, 80], ci.frequencies)

    def test_pairwise_merge(self):
        terms = ["a", "b", "c"]
        ci1 = SingleCategoryInfo("C1", 100, terms, [50, 0, 80])
        ci2 = SingleCategoryInfo("C2", 80, terms, [0, 40, 20])
        merged = MultipleCategoryInfo(ci1, ci2)
        numpy.testing.assert_array_equal([50, 40, 100], merged.frequencies)
        self.assertEqual("(C1+C2)", merged.category)
        self.assertEqual(180, merged.documents)
        self.assertEqual({ci1, ci2}, merged.children)

    def test_multiple_merge(self):
        terms = ["a", "b", "c"]
        ci1 = SingleCategoryInfo("C1", 100, terms, [50, 0, 80])
        ci2 = SingleCategoryInfo("C2", 80, terms, [0, 40, 20])
        ci3 = SingleCategoryInfo("C3", 130, terms, [20, 20, 30])
        merged = MultipleCategoryInfo(ci1, ci2, ci3)
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("(C1+C2+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual({ci1, ci2, ci3}, merged.children)

    def test_hierarchical_merge(self):
        terms = ["a", "b", "c"]
        ci1 = SingleCategoryInfo("C1", 100, terms, [50, 0, 80])
        ci2 = SingleCategoryInfo("C2", 80, terms, [0, 40, 20])
        ci3 = SingleCategoryInfo("C3", 130, terms, [20, 20, 30])
        middle = MultipleCategoryInfo(ci1, ci2)
        merged = MultipleCategoryInfo(middle, ci3)
        numpy.testing.assert_array_equal([70, 60, 130], merged.frequencies)
        self.assertEqual("((C1+C2)+C3)", merged.category)
        self.assertEqual(310, merged.documents)
        self.assertEqual({middle, ci3}, merged.children)
