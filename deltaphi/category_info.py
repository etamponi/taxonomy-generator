import numpy

__author__ = 'Emanuele Tamponi'


class TermsError(Exception):
    pass


class CategoryInfo(object):

    def __init__(self, category, documents, terms, frequencies, children):
        self.category = category
        self.documents = documents
        self.terms = terms
        self.frequencies = numpy.asarray(frequencies, dtype=float)
        self.children = children


class SingleCategoryInfo(CategoryInfo):

    def __init__(self, category, documents, terms, frequencies):
        super(SingleCategoryInfo, self).__init__(category, documents, terms, frequencies, set())


class MultipleCategoryInfo(CategoryInfo):

    def __init__(self, *category_infos):
        if any(ci.terms is not category_infos[0].terms for ci in category_infos):
            raise TermsError()
        categories = sorted(ci.category for ci in category_infos)
        merged_category = "(" + "+".join(categories) + ")"
        merged_documents = sum(ci.documents for ci in category_infos)
        merged_frequencies = sum(ci.frequencies for ci in category_infos)
        merged_children = set(category_infos)
        super(MultipleCategoryInfo, self).__init__(
            merged_category, merged_documents, category_infos[0].terms, merged_frequencies, merged_children
        )
