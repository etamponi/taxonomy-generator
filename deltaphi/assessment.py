from deltaphi.category_info import CategoryLayer, CategoryGroup

__author__ = 'Emanuele Tamponi'


class Taxonomy(object):

    def __init__(self, leaf_layer):
        assert leaf_layer.is_closed()
        self.layers = [leaf_layer]

    def add_layer(self, layer):
        self.layers.insert(0, CategoryLayer(CategoryGroup(group.leafs()) for group in layer.groups))


class TaxonomyScore(object):

    def __init__(self, reference):
        self.reference = reference

    def evaluate(self, taxonomy):
        score = 0
        k = len(self.reference.layers) - 1
        assert k == (len(taxonomy.layers) - 1)
        for i, (reference_layer, taxonomy_layer) in enumerate(zip(self.reference.layers, taxonomy.layers))[:-1]:
            layer_score = self._layer_score(reference_layer, taxonomy_layer)
            score += float(i + 1) / k * layer_score
        score *= 2.0 / (k + 1)
        return score

    @staticmethod
    def _layer_score(layer1, layer2):

        return 0
