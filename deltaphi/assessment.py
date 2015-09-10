from collections import defaultdict
from itertools import combinations
import math

import numpy

from deltaphi.category_info import CategoryLayer, CategoryGroup

__author__ = 'Emanuele Tamponi'


class Taxonomy(object):

    def __init__(self, leaf_layer):
        assert leaf_layer.is_closed()
        top_layer = CategoryLayer([CategoryGroup([group.infos[0] for group in leaf_layer.groups])])
        self.layers = [top_layer, leaf_layer]

    def add_layer(self, layer):
        exploded_layer = CategoryLayer(CategoryGroup(group.leafs()) for group in layer.groups)
        assert self._has_all_leafs(exploded_layer)
        self.layers.insert(1, exploded_layer)

    def leafs(self):
        return set(self.layers[0].groups[0].infos)

    def _has_all_leafs(self, exploded_layer):
        new_leafs = set(sum((list(group.infos) for group in exploded_layer.groups), []))
        orig_leafs = set(group.infos[0] for group in self.layers[-1].groups)
        return new_leafs == orig_leafs

    @classmethod
    def build_from_category_names(cls, leafs):
        tables = defaultdict(lambda: defaultdict(list))
        depth = 0
        for category in leafs:
            full_name = category.category
            tokens = full_name.split("/")
            if len(tokens) > depth:
                depth = len(tokens)
            for i, token in enumerate(tokens[:-1]): # Skip last token because it is the leaf category
                tables[i][token].append(category)
        taxonomy = Taxonomy(CategoryLayer.build_closed_layer(leafs))
        for i in range(0, depth - 1)[::-1]:
            raw_groups = tables[i].values()
            groups = map(CategoryGroup, raw_groups)
            layer = CategoryLayer(groups)
            taxonomy.add_layer(layer)
        return taxonomy


class TaxonomyScore(object):

    def __init__(self, reference):
        self.reference = reference

    def evaluate(self, taxonomy):
        all_leafs = self.reference.leafs() | taxonomy.leafs()
        score = 0
        k = len(self.reference.layers) - 1
        assert k == (len(taxonomy.layers) - 1)
        if k == 1:
            return 1
        for i, (reference_layer, taxonomy_layer) in enumerate(zip(self.reference.layers, taxonomy.layers)):
            if i == k:
                break
            layer_score = self.layer_score(reference_layer, taxonomy_layer, all_leafs)
            score += float(i + 1) / k * layer_score
        score *= 2.0 / (k + 1)
        return score

    def layer_score(self, reference_layer, taxonomy_layer, all_leafs):
        n = numpy.zeros((2, 2))
        for cat1, cat2 in combinations(all_leafs, 2):
            same_group_in_reference = int(self._same_group(reference_layer, cat1, cat2))
            same_group_in_taxonomy = int(self._same_group(taxonomy_layer, cat1, cat2))
            n[same_group_in_reference, same_group_in_taxonomy] += 1
        den = math.sqrt((n[1, 1] + n[1, 0]) * (n[1, 1] + n[0, 1]))
        score = n[1, 1] / den if den > 0 else 0
        return score

    @staticmethod
    def _same_group(layer, cat1, cat2):
        return any(cat2 in group for group in layer.groups_of(cat1))
