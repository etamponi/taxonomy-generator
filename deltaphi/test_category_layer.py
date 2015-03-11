import unittest

from deltaphi.category_layer import CategoryLayerBuilder
from deltaphi import test_file_path
from deltaphi.gateways import CSVGateway


__author__ = 'Emanuele Tamponi'


class TestCategoryLayer(unittest.TestCase):

    def setUp(self):
        self.gateway = CSVGateway(test_file_path("example.csv"))
        self.gateway.open()

    def test_pairwise_merge(self):
        layer = CategoryLayerBuilder.build_from_singletons(self.gateway.iterate())
        self.assertEqual(3, len(layer.groups))
        expected_merged_categories = [
            layer.groups[0].categories,
            (layer.groups[1] + layer.groups[2]).categories
        ]
        actual_merged_categories = [
            group.categories for group in CategoryLayerBuilder.build_by_pairwise_group_merge(layer, 1, 2).groups
        ]
        self.assertEqual(expected_merged_categories, actual_merged_categories)

    def test_build_parent_layer(self):
        layer = CategoryLayerBuilder.build_from_singletons(self.gateway.iterate())
        layer = CategoryLayerBuilder.build_by_pairwise_group_merge(layer, 0, 1)
        layer = layer.build_parent()
        self.assertEqual(2, len(layer.groups))
        self.assertEqual({1, 1}, {len(group) for group in layer.groups})
