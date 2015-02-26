import unittest
from deltaphi.category_info import CategoryInfo, InvalidParameters

__author__ = 'Emanuele Tamponi'


class TestCategoryInfo(unittest.TestCase):

    def test_init_valid_inputs(self):
        ci = CategoryInfo("DummyCategory", "100", "aaa bb c", "50 60 40")
        self.assertEqual("DummyCategory", ci.category)
        self.assertEqual(100, ci.n_observations)
        self.assertEqual({"aaa": 50, "bb": 60, "c": 40}, ci.predictors)
        self.assertEqual({}, ci.children)

    def test_init_invalid_inputs(self):
        self.assertRaises(InvalidParameters, CategoryInfo, "DummyCategory", "100", "aaa", "10 20")
        self.assertRaises(InvalidParameters, CategoryInfo, "DummyCategory", "10.2", "aaa", "10")

    def test_pairwise_merge(self):
        ci1 = CategoryInfo("A", "100", "a b", "40 60")
        ci2 = CategoryInfo("B", "50", "b c", "20 70")
        merged = CategoryInfo.merge(ci1, ci2)
        self.assertEqual("(A+B)", merged.category)
        self.assertEqual(150, merged.n_observations)
        self.assertEqual({"a": 40, "b": 80, "c": 70}, merged.predictors)
        self.assertEqual({ci1, ci2}, merged.children)

    def test_multiple_merge(self):
        ci1 = CategoryInfo("A", "100", "a b", "40 60")
        ci2 = CategoryInfo("B", "50", "b c", "20 70")
        ci3 = CategoryInfo("C", "30", "a c", "30 20")
        merged = CategoryInfo.merge(ci1, ci2, ci3)
        self.assertEqual("(A+B+C)", merged.category)
        self.assertEqual(180, merged.n_observations)
        self.assertEqual({"a": 70, "b": 80, "c": 90}, merged.predictors)
        self.assertEqual({ci1, ci2, ci3}, merged.children)

    def test_hierarchical_merge(self):
        ci1 = CategoryInfo("A", "100", "a b", "40 60")
        ci2 = CategoryInfo("B", "50", "b c", "20 70")
        ci3 = CategoryInfo("C", "30", "a c", "30 20")
        middle = CategoryInfo.merge(ci1, ci2)
        merged = CategoryInfo.merge(ci3, middle)
        self.assertEqual("((A+B)+C)", merged.category)
        self.assertEqual(180, merged.n_observations)
        self.assertEqual({"a": 70, "b": 80, "c": 90}, merged.predictors)
        self.assertEqual({middle, ci3}, merged.children)