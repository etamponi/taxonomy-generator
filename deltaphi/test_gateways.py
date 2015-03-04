import unittest
import numpy

from deltaphi.category_info import SingleCategoryInfo
import gateways
from deltaphi import test_file_path


__author__ = 'Emanuele Tamponi'


class TestGateways(unittest.TestCase):

    def setUp(self):
        self.gateway_impls = [
            gateways.CSVGateway(test_file_path("example.csv"))
        ]
        self.expected_infos = [
            SingleCategoryInfo("A", 100, None, [40, 60, 0, 0]),
            SingleCategoryInfo("B", 80, None, [0, 20, 70, 30]),
            SingleCategoryInfo("C", 30, None, [30, 0, 20, 0])
        ]

    def test_gateway_open(self):
        for gateway in self.gateway_impls:
            gateway.open()
            self.assertEqual(["a", "b", "c", "d"], gateway.terms)

    def test_gateway_iterate(self):
        for gateway in self.gateway_impls:
            gateway.open()
            for expected_info, actual_info in zip(self.expected_infos, gateway.iterate()):
                self.assertEqual(expected_info.category, actual_info.category)
                self.assertEqual(expected_info.documents, actual_info.documents)
                # The terms array has to be *the same*, not just equal
                self.assertIs(gateway.terms, actual_info.terms)
                numpy.testing.assert_array_equal(expected_info.frequencies, actual_info.frequencies)
