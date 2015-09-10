import unittest

from deltaphi.assessment import Taxonomy, TaxonomyScore
from deltaphi.category_info import CategoryLayer, CategoryGroup
from deltaphi.fake_entities import FakeCategoryInfo

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
        self.assertEqual(1, scorer.evaluate(taxonomy))

    def test_ontolearn_example(self):
        # Taken from OntoLearn Reloaded: A Graph-Based Algorithm for Taxonomy Induction pag. 693
        reference = self._build_reference()
        taxonomy = self._build_taxonomy()
        all_leafs = reference.leafs() | taxonomy.leafs()
        scorer = TaxonomyScore(reference)
        self.assertAlmostEqual(0.67, scorer.layer_score(reference.layers[0], taxonomy.layers[0], all_leafs), 2)
        self.assertAlmostEqual(0.95, scorer.layer_score(reference.layers[1], taxonomy.layers[1], all_leafs), 2)
        self.assertAlmostEqual(0.00, scorer.layer_score(reference.layers[2], taxonomy.layers[2], all_leafs), 2)
        self.assertAlmostEqual(0.00, scorer.layer_score(reference.layers[3], taxonomy.layers[3], all_leafs), 2)

        self.assertAlmostEqual(0.43, scorer.evaluate(taxonomy), 2)

    def _build_reference(self):
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

    def _build_taxonomy(self):
        leafs = [
            FakeCategoryInfo("A", 4),
            FakeCategoryInfo("B", 4),
            FakeCategoryInfo("C", 4),
            FakeCategoryInfo("D", 4),
            FakeCategoryInfo("E", 4),
            FakeCategoryInfo("G", 4)
        ]
        taxonomy = Taxonomy(CategoryLayer.build_closed_layer(leafs))
        # Same layer
        taxonomy.add_layer(CategoryLayer.build_closed_layer(leafs))
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
