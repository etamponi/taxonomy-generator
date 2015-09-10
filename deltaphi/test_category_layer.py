import unittest

from deltaphi.category_info import CategoryGroup, CategoryLayer
from deltaphi import test_file_path
from deltaphi.fake_entities import FakeCategoryInfo
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

    def test_group_of(self):
        c1 = FakeCategoryInfo("A", 4)
        c2 = FakeCategoryInfo("B", 4)
        c3 = FakeCategoryInfo("C", 4)
        c4 = FakeCategoryInfo("D", 4)
        g1 = CategoryGroup([c1, c2])
        g2 = CategoryGroup([c2, c3])
        layer = CategoryLayer([g1, g2])
        self.assertEqual([g1], layer.groups_of(c1))
        self.assertEqual([g1, g2], layer.groups_of(c2))
        self.assertEqual([g2], layer.groups_of(c3))
        self.assertEqual([], layer.groups_of(c4))
