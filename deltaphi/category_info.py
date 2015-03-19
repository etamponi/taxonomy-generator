from blist import sortedlist
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

    def __repr__(self):
        return self.category


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

    def __cmp__(self, other):
        return cmp(self.infos, other.infos)

    def build_parent_info(self):
        if len(self.infos) == 1:
            return self.infos[0]
        merged_category = "(" + "+".join(ci.category for ci in self) + ")"
        merged_documents = sum(ci.documents for ci in self)
        merged_frequencies = sum(ci.frequencies for ci in self)
        return CategoryInfo(merged_category, merged_documents, self.terms, merged_frequencies, self)

    def __repr__(self):
        return repr(list(self.infos))


class CategoryLayer(object):

    def __init__(self, groups):
        self.groups = sortedlist(groups)

    def merge_groups(self, a, b):
        new_layer = CategoryLayer(self.groups)
        new_layer.groups.remove(a)
        new_layer.groups.remove(b)
        new_layer.groups.add(a + b)
        return new_layer

    def __cmp__(self, other):
        return cmp(self.groups, other.groups)

    def build_parent(self):
        return CategoryLayer.build_singleton_layer(group.build_parent_info() for group in self.groups)

    @classmethod
    def build_singleton_layer(cls, info_iterable):
        return CategoryLayer([CategoryGroup([info]) for info in info_iterable])

    def __repr__(self):
        return "Layer: {}".format(list(self.groups))


class CategoryInfoBuilder(object):

    def __init__(self, terms):
        self.terms = sortedlist(unicode(term, "utf-8") for term in terms)
        self.term_positions = {term: i for i, term in enumerate(self.terms)}

    def build_leaf(self, category, documents, term_frequencies):
        full_frequencies = numpy.zeros(len(self.terms))
        for term, frequency in term_frequencies.iteritems():
            term = unicode(term, "utf-8")
            if term in self.term_positions:
                full_frequencies[self.term_positions[term]] = frequency
        return CategoryInfo(category, documents, self.terms, full_frequencies, None)
