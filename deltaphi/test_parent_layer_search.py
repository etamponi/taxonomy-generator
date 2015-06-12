import unittest

from nltk.corpus import stopwords

from deltaphi import test_file_path
from deltaphi.category_info import CategoryLayer
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CSVRawSource, CategoryInfoSource
from deltaphi.metrics import GeometricMeanScore
from deltaphi.parent_layer_search import GreedyMergeSearch

__author__ = 'Emanuele Tamponi'


class TestParentLayerSearch(unittest.TestCase):

    def setUp(self):
        self.search_impls = [
            GreedyMergeSearch(GeometricMeanScore()),
            #LayerGreedyMergeSearch(LookAhead(PairwiseCharacteristicTerms(), PairwiseDiscriminantTerms()))
        ]
        source = CategoryInfoSource(
            CSVRawSource(test_file_path("dmoz_arts_full.csv")),
            RawFilter(min_length=1, stopwords=stopwords.words("english"))
        )
        source.open()
        self.base_layer = CategoryLayer.build_singleton_layer(source.iterate())

    def test_implementations(self):
        for search in self.search_impls:
            candidates = search.perform(self.base_layer)
            for candidate in candidates:
                print candidate
                self.assertTrue(candidate.is_singleton_layer())
                # Verifies that we didn't forget any CategoryInfo
                self.assertEqual(
                    len(self.base_layer.groups),
                    sum(
                        len(group[0].child_group) if group[0].child_group is not None else 1
                        for group in candidate.groups
                    )
                )
