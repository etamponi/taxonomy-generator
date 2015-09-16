import csv
import unittest
import sys

from deltaphi import test_file_path
from deltaphi.experiments.assessment import Taxonomy, TaxonomyScore, SearchTaxonomy
from deltaphi.category_info import CategoryLayer, CategoryGroup
from deltaphi.fake_entities import FakeCategoryInfo
from deltaphi.metrics import LookAhead
from deltaphi.parent_layer_search import LayerGreedyMergeSearch
from deltaphi.raw_filter import RawFilter
from deltaphi.sources import CategoryInfoSource, CSVRawSource

__author__ = 'Emanuele Tamponi'


class TestTaxonomy(unittest.TestCase):

    def test_init(self):
        c1 = FakeCategoryInfo("A", 4)
        c2 = FakeCategoryInfo("B", 4)
        c3 = FakeCategoryInfo("C", 4)
        layer = CategoryLayer.build_closed_layer([c1, c2, c3])
        taxonomy = Taxonomy(layer)
        self.assertEqual(layer, taxonomy.layers[1])
        top_layer = CategoryLayer([CategoryGroup([c1, c2, c3])])
        self.assertEqual(top_layer, taxonomy.layers[0])

    def test_add_layer(self):
        c1 = FakeCategoryInfo("A", 4)
        c2 = FakeCategoryInfo("B", 4)
        c3 = FakeCategoryInfo("C", 4)
        layer = CategoryLayer.build_closed_layer([c1, c2, c3])
        taxonomy = Taxonomy(layer)
        exploded_new_layer = layer.merge_groups(layer.groups[0], layer.groups[1])
        taxonomy.add_layer(exploded_new_layer.build_parent())
        self.assertEqual(exploded_new_layer, taxonomy.layers[1])
        exploded_new_layer = exploded_new_layer.merge_groups(exploded_new_layer.groups[0], exploded_new_layer.groups[1])
        taxonomy.add_layer(exploded_new_layer.build_parent())
        self.assertEqual(exploded_new_layer, taxonomy.layers[1])

    def test_build_from_names(self):
        c1 = FakeCategoryInfo("A/a/1", 4)
        c2 = FakeCategoryInfo("A/a/2", 4)
        c3 = FakeCategoryInfo("A/b/3", 4)
        c4 = FakeCategoryInfo("B/c/4", 4)
        c5 = FakeCategoryInfo("B/d/5", 4)
        c6 = FakeCategoryInfo("B/d/6", 4)
        taxonomy = Taxonomy.build_from_category_names([c1, c2, c3, c4, c5, c6])
        first_layer = CategoryLayer([
            CategoryGroup([c1, c2, c3]),
            CategoryGroup([c4, c5, c6]),
        ])
        self.assertEqual(first_layer, taxonomy.layers[1])
        second_layer = CategoryLayer([
            CategoryGroup([c1, c2]),
            CategoryGroup([c3]),
            CategoryGroup([c4]),
            CategoryGroup([c5, c6]),
        ])
        self.assertEqual(second_layer, taxonomy.layers[2])


class TestTaxonomyScore(unittest.TestCase):

    def test_score_sum_to_one(self):
        c1 = FakeCategoryInfo("A", 4)
        c2 = FakeCategoryInfo("B", 4)
        c3 = FakeCategoryInfo("C", 4)
        layer = CategoryLayer.build_closed_layer([c1, c2, c3])
        taxonomy = Taxonomy(layer)
        new_layer = layer.merge_groups(layer.groups[0], layer.groups[1])
        taxonomy.add_layer(new_layer)
        scorer = TaxonomyScore(taxonomy)
        self.assertEqual(1, scorer.evaluate(taxonomy)[0])

    def test_ontolearn_example(self):
        # Taken from OntoLearn Reloaded: A Graph-Based Algorithm for Taxonomy Induction pag. 693
        taxonomy1 = self._build_taxonomy1()
        taxonomy2 = self._build_taxonomy2()
        scorer = TaxonomyScore(reference=taxonomy1)
        score, layer_scores = scorer.evaluate(taxonomy2)
        self.assertEqual(3, len(layer_scores))
        self.assertAlmostEqual(0.67, layer_scores[0], 2)
        self.assertAlmostEqual(0.95, layer_scores[1], 2)
        self.assertEqual(0.00, layer_scores[2], 2)

        self.assertAlmostEqual(0.43, score, 2)
        # Swapping taxonomies improves the score!
        self.assertAlmostEqual(0.86, TaxonomyScore(reference=taxonomy2).evaluate(taxonomy1)[0], 2)

    def _build_taxonomy1(self):
        leafs = [
            FakeCategoryInfo("A", 4),
            FakeCategoryInfo("B", 4),
            FakeCategoryInfo("C", 4),
            FakeCategoryInfo("D", 4),
            FakeCategoryInfo("E", 4),
            FakeCategoryInfo("F", 4)
        ]
        taxonomy = Taxonomy(CategoryLayer.build_closed_layer(leafs))
        taxonomy.add_layer(
            CategoryLayer(
                [
                    CategoryGroup([leafs[0], leafs[1]]),
                    CategoryGroup([leafs[2], leafs[3]]),
                    CategoryGroup([leafs[4]]),
                    CategoryGroup([leafs[5]]),
                ]
            )
        )
        taxonomy.add_layer(
            CategoryLayer(
                [
                    CategoryGroup(leafs[0:5]),
                    CategoryGroup(leafs[4:]),
                ]
            )
        )
        return taxonomy

    def _build_taxonomy2(self):
        leafs = [
            FakeCategoryInfo("A", 4),
            FakeCategoryInfo("B", 4),
            FakeCategoryInfo("C", 4),
            FakeCategoryInfo("D", 4),
            FakeCategoryInfo("E", 4),
            FakeCategoryInfo("G", 4)
        ]
        taxonomy = Taxonomy(CategoryLayer.build_closed_layer(leafs))
        taxonomy.add_layer(
            CategoryLayer(
                [
                    CategoryGroup(leafs[0:5]),
                    CategoryGroup([leafs[4]]),
                    CategoryGroup([leafs[5]]),
                ]
            )
        )
        return taxonomy


class TestSearchTaxonomy(unittest.TestCase):

    def setUp(self):
        csv.field_size_limit(sys.maxint)
        source = CategoryInfoSource(
            CSVRawSource(
                test_file_path("dmoz_arts_7.csv")
            ),
            RawFilter(
                min_length=3
            )
        )
        source.open()
        self.base_layer = CategoryLayer.build_closed_layer(source.iterate())

    def test_it_runs(self):
        search = SearchTaxonomy(LayerGreedyMergeSearch(LookAhead()))
        taxonomy = search.build_taxonomy(self.base_layer)
        for i, layer in enumerate(taxonomy.layers):
            print i, "=", layer
        print (
            "Score:",
            TaxonomyScore(reference=Taxonomy.build_from_category_names(taxonomy.leafs())).evaluate(taxonomy)[0]
        )
        self.assertGreaterEqual(3, len(taxonomy.layers))
