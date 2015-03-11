from blist import sortedlist, blist
import numpy

__author__ = 'Emanuele Tamponi'


class TermsError(Exception):
    pass


class CategoryInfo(object):

    def __init__(self, category, documents, terms, frequencies, children):
        self.category = category
        self.documents = documents
        self.terms = terms
        self.frequencies = frequencies
        self.children = children

    def __cmp__(self, other):
        return cmp(self.category, other.category)


class CategoryGroup(object):

    def __init__(self, info_iterable):
        self.infos = sortedlist(info_iterable)
        self.terms = self.infos[0].terms

    def __add__(self, other):
        ret = CategoryGroup(self.infos)
        ret.infos.update(other.infos)
        return ret

    def __iter__(self):
        return iter(self.infos)

    def __getitem__(self, item):
        return self.infos.__getitem__(item)

    def __len__(self):
        return len(self.infos)

    def build_parent_info(self):
        if len(self.infos) == 1:
            return self.infos[0]
        merged_category = "(" + "+".join(ci.category for ci in self) + ")"
        merged_documents = sum(ci.documents for ci in self)
        merged_frequencies = sum(ci.frequencies for ci in self)
        return CategoryInfo(merged_category, merged_documents, self.terms, merged_frequencies, self)

    def __cmp__(self, other):
        return cmp(self.infos, other.infos)


class CategoryLayer(object):

    def __init__(self, groups):
        self.groups = blist(groups)

    def merge_groups(self, i, j):
        new_layer = CategoryLayer(self.groups)
        if i > j:
            i, j = j, i
        del new_layer.groups[j]
        del new_layer.groups[i]
        new_layer.groups.append(self.groups[i] + self.groups[j])
        return new_layer

    def build_parent(self):
        return CategoryLayer.build_singleton_layer(group.build_parent_info() for group in self.groups)

    def __cmp__(self, other):
        return cmp(self.groups, other.groups)

    @classmethod
    def build_singleton_layer(cls, info_iterable):
        return CategoryLayer([CategoryGroup([info]) for info in info_iterable])


class CategoryInfoBuilder(object):

    def __init__(self, terms):
        self.terms = numpy.asarray(sorted(terms))
        self.term_positions = {term: i for i, term in enumerate(self.terms)}

    def build_leaf(self, category, documents, term_frequencies):
        full_frequencies = numpy.zeros(len(self.terms))
        for term, frequency in term_frequencies.iteritems():
            full_frequencies[self.term_positions[term]] = frequency
        return CategoryInfo(category, documents, self.terms, full_frequencies, None)
