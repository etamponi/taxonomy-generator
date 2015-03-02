import numpy

__author__ = 'Emanuele Tamponi'


class TermsError(Exception):
    pass


class CategoryInfo(object):

    def __init__(self, category, documents, terms, frequencies):
        self.category = category
        self.documents = documents
        self.terms = terms
        self.frequencies = numpy.asarray(frequencies)
        self.children = set()

    @classmethod
    def merge(cls, *category_infos):
        if any(ci.terms is not category_infos[0].terms for ci in category_infos):
            raise TermsError()
        categories = sorted(ci.category for ci in category_infos)
        merged_category = "(" + "+".join(categories) + ")"
        merged_documents = sum(ci.documents for ci in category_infos)
        merged_frequencies = sum(ci.frequencies for ci in category_infos)
        merged_children = set(category_infos)
        merged = CategoryInfo(merged_category, merged_documents, category_infos[0].terms, merged_frequencies)
        merged.children = merged_children
        return merged
