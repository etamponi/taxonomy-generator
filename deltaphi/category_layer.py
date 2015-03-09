import itertools

__author__ = 'Emanuele Tamponi'


class CategoryLayerBuilder(object):

    @classmethod
    def build_from_singletons(cls, info_iterable):
        return CategoryLayer(frozenset([info]) for info in info_iterable)

    @classmethod
    def build_from_layer_merge(cls, layer, group_i, group_j):
        groups = layer.groups - {group_i, group_j}
        groups = groups | {group_i | group_j}
        return CategoryLayer(groups)


class CategoryLayer(object):

    def __init__(self, groups):
        self.groups = frozenset(groups)

    def is_ready(self):
        return all(len(group) > 1 for group in self.groups)

    def iterate_pairwise_merges(self):
        for group_i, group_j in itertools.combinations(self.groups, 2):
            yield CategoryLayerBuilder.build_from_layer_merge(self, group_i, group_j)
