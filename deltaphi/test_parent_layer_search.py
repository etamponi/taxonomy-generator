import unittest

from deltaphi import test_file_path
from deltaphi.category_info import CategoryLayer
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CSVRawSource, CategoryInfoSource
from deltaphi.metrics import GeometricMeanScore, LookAhead
from deltaphi.parent_layer_search import GreedyMergeSearch, LayerGreedyMergeSearch

__author__ = 'Emanuele Tamponi'


class TestParentLayerSearch(unittest.TestCase):

    def setUp(self):
        self.search_impls = [
            GreedyMergeSearch(GeometricMeanScore()),
            LayerGreedyMergeSearch(LookAhead())
        ]
        source = CategoryInfoSource(
            CSVRawSource(test_file_path("dmoz_arts_7.csv")),
            RawFilter()
        )
        source.open()
        self.base_layer = CategoryLayer.build_singleton_layer(source.iterate())

    def test_implementations(self):
        for search in self.search_impls:
            candidates = search.perform(self.base_layer)
            for candidate in candidates:
                self.assertTrue(candidate.is_singleton_layer())
                # Verifies that we didn't forget any CategoryInfo
                self.assertEqual(
                    len(self.base_layer.groups),
                    sum(len(group[0].child_group) for group in candidate.groups)
                )
