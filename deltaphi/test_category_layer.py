import unittest

from deltaphi.category_layer import CategoryLayerBuilder
from deltaphi import test_file_path
from deltaphi.gateways import CSVGateway


__author__ = 'Emanuele Tamponi'


class TestCategoryLayer(unittest.TestCase):

    def setUp(self):
        self.gateway = CSVGateway(test_file_path("example.csv"))
        self.gateway.open()

    def test_layer_init(self):
        infos = list(self.gateway.iterate())
        layer = CategoryLayerBuilder.build_from_singletons(infos)
        self.assertEqual(3, len(layer.groups))
        group_list = list(layer.groups)
        layer_merge = CategoryLayerBuilder.build_from_layer_merge(layer, group_list[1], group_list[2])
        self.assertEqual(2, len(layer_merge.groups))
        merged_groups = frozenset([
            group_list[0],
            group_list[1] | group_list[2]
        ])
        self.assertEqual(merged_groups, layer_merge.groups)

    def test_layer_is_ready(self):
        layer = CategoryLayerBuilder.build_from_singletons(self.gateway.iterate())
        group_list = list(layer.groups)
        self.assertFalse(layer.is_ready())
        layer.groups = {group_list[0] | group_list[1], group_list[2]}
        self.assertFalse(layer.is_ready())
        layer.groups = {group_list[0] | group_list[1] | group_list[2]}
        self.assertTrue(layer.is_ready())

    def test_iterate_pairwise_merges(self):
        layer = CategoryLayerBuilder.build_from_singletons(self.gateway.iterate())
        group_list = list(layer.groups)
        expected_groups = [
            frozenset([group_list[0], group_list[1] | group_list[2]]),
            frozenset([group_list[0] | group_list[1], group_list[2]]),
            frozenset([group_list[0] | group_list[2], group_list[1]])
        ]
        self.assertEqual(set(expected_groups), set(layer.groups for layer in layer.iterate_pairwise_merges()))
        layer.groups = expected_groups[0]
        expected_groups = [
            frozenset([group_list[0] | group_list[1] | group_list[2]])
        ]
        self.assertEqual(set(expected_groups), set(layer.groups for layer in layer.iterate_pairwise_merges()))
