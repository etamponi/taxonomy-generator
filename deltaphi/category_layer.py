import itertools

__author__ = 'Emanuele Tamponi'


class CategoryLayerBuilder(object):

    @classmethod
    def build_from_singletons(cls, info_iterable):
        return CategoryLayer(frozenset([info]) for info in info_iterable)

    @classmethod
    def build_from_group_merge(cls, layer, group_i, group_j):
        groups = layer.groups - {group_i, group_j}
        groups = groups | {group_i | group_j}
        return CategoryLayer(groups)

    @classmethod
    def build_parent_layer(cls, layer, category_info_builder):
        parent_groups = set()
        for group in layer.groups:
            if len(group) > 1:
                parent_groups.add(frozenset([category_info_builder.build_node(group)]))
            else:
                parent_groups.add(group)
        return CategoryLayer(parent_groups)


class CategoryLayer(object):

    def __init__(self, groups):
        self.groups = frozenset(groups)

    def iterate_pairwise_merges(self):
        for group_i, group_j in itertools.combinations(self.groups, 2):
            yield CategoryLayerBuilder.build_from_group_merge(self, group_i, group_j)
