import unittest

from deltaphi.category_info import CategoryGroup, CategoryLayer
from deltaphi import test_file_path
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CSVRawSource, CategoryInfoSource


__author__ = 'Emanuele Tamponi'


class TestCategoryLayer(unittest.TestCase):

    def setUp(self):
        self.source = CategoryInfoSource(CSVRawSource(test_file_path("example.csv")), RawFilter())
        self.source.open()

    def test_pairwise_merge(self):
        layer = CategoryLayer.build_closed_layer(self.source.iterate())
        expected_layer = CategoryLayer([
            layer.groups[0],
            layer.groups[1] + layer.groups[2]
        ])
        self.assertEqual(expected_layer, layer.merge_groups(layer.groups[1], layer.groups[2]))

    def test_build_parent_layer(self):
        layer = CategoryLayer.build_closed_layer(self.source.iterate())
        merged = layer.merge_groups(layer.groups[0], layer.groups[1])
        expected_parent = CategoryLayer([
            layer.groups[2],
            CategoryGroup([(layer.groups[0] + layer.groups[1]).build_parent_info()])
        ])
        self.assertEqual(expected_parent, merged.build_parent())
