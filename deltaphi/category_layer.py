from blist import blist

from deltaphi.category_info import CategoryGroup


__author__ = 'Emanuele Tamponi'


class CategoryLayerBuilder(object):

    @classmethod
    def build_from_singletons(cls, info_iterable):
        return CategoryLayer([CategoryGroup(info) for info in info_iterable])

    @classmethod
    def build_by_pairwise_group_merge(cls, layer, i, j):
        new_layer = CategoryLayer(layer.groups)
        if i > j:
            i, j = j, i
        del new_layer.groups[j]
        del new_layer.groups[i]
        new_layer.groups.append(layer.groups[i] + layer.groups[j])
        return new_layer


class CategoryLayer(object):

    def __init__(self, groups):
        self.groups = blist(groups)

    def build_parent(self):
        return CategoryLayer([CategoryGroup(group.build_parent_info()) for group in self.groups])
