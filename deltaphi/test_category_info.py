import unittest

import numpy

from deltaphi.category_info import CategoryInfoFactory, RawCategoryInfo


__author__ = 'Emanuele Tamponi'


class TestCategoryInfo(unittest.TestCase):

    def setUp(self):
        self.builder = CategoryInfoFactory({"a", "b", "c"})

    def test_build_leaf(self):
        ci = self.builder.build(RawCategoryInfo("Name", 100, {"a": 10, "b": 30, "c": 80}))
        self.assertIsInstance(ci.frequencies, numpy.ndarray)
        self.assertEqual("Name", ci.category)
        self.assertEqual(100, ci.documents)
        self.assertEqual(None, ci.child_group)
        numpy.testing.assert_array_equal([10, 30, 80], ci.frequencies)
