import unittest

from deltaphi.category_info import CategoryGroup, CategoryLayer
from deltaphi import test_file_path
from deltaphi.gateways import CSVGateway


__author__ = 'Emanuele Tamponi'


class TestCategoryLayer(unittest.TestCase):

    def setUp(self):
        self.gateway = CSVGateway(test_file_path("example.csv"))
        self.gateway.open()

    def test_pairwise_merge(self):
        layer = CategoryLayer.build_singleton_layer(self.gateway.iterate())
        expected_layer = CategoryLayer([
            layer.groups[0],
            layer.groups[1] + layer.groups[2]
        ])
        self.assertEqual(expected_layer, layer.merge_groups(1, 2))

    def test_build_parent_layer(self):
        layer = CategoryLayer.build_singleton_layer(self.gateway.iterate())
        merged = layer.merge_groups(0, 1)
        expected_parent = CategoryLayer([
            layer.groups[2],
            CategoryGroup([(layer.groups[0] + layer.groups[1]).build_parent_info()])
        ])
        self.assertEqual(expected_parent, merged.build_parent())
