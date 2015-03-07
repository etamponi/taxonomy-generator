import unittest

import numpy

from deltaphi.category_info import CategoryInfoBuilder
import gateways
from deltaphi import test_file_path


__author__ = 'Emanuele Tamponi'


class TestGateways(unittest.TestCase):

    def setUp(self):
        builder = CategoryInfoBuilder(["a", "b", "c", "d"])
        self.gateway_impls = [
            gateways.CSVGateway(test_file_path("example.csv"))
        ]
        self.expected_infos = [
            builder.build_leaf("A", 100, {"a": 40, "b": 60}),
            builder.build_leaf("B", 80, {"b": 20, "c": 70, "d": 30}),
            builder.build_leaf("C", 30, {"a": 30, "c": 20})
        ]

    def test_gateway_open(self):
        for gateway in self.gateway_impls:
            gateway.open()
            numpy.testing.assert_array_equal(["a", "b", "c", "d"], gateway.builder.terms)

    def test_gateway_iterate(self):
        for gateway in self.gateway_impls:
            gateway.open()
            for expected_info, actual_info in zip(self.expected_infos, gateway.iterate()):
                self.assertEqual(expected_info.category, actual_info.category)
                self.assertEqual(expected_info.documents, actual_info.documents)
                # The terms array has to be *the same*, not just equal
                self.assertIs(gateway.builder.terms, actual_info.terms)
                numpy.testing.assert_array_equal(expected_info.frequencies, actual_info.frequencies)
