import unittest
import numpy
from deltaphi.binary_metrics import BinaryDiscriminant
from deltaphi.category_info import SingleCategoryInfo

__author__ = 'Emanuele Tamponi'


class TestBinaryMetrics(unittest.TestCase):

    def setUp(self):
        self.terms = ["a", "b", "c"]
        self.ci1 = SingleCategoryInfo("A", 100, self.terms, [60, 0, 80])
        self.ci2 = SingleCategoryInfo("B", 80, self.terms, [0, 30, 50])

    def test_discriminant(self):
        d = BinaryDiscriminant()
        expected_discriminant = numpy.asarray([60. / 100., -30. / 80., (80. / 100.) - (50. / 80.)])
        numpy.testing.assert_array_equal(expected_discriminant, d.evaluate(self.ci1, self.ci2))
