import numpy
from blist import sortedlist

from deltaphi.category_info import CategoryInfo
from deltaphi.metrics import PairwiseMetric

__author__ = 'Emanuele Tamponi'


class FakeCategoryInfo(CategoryInfo):

    def __init__(self, category, num_terms):
        super(FakeCategoryInfo, self).__init__(
            category, 100, sortedlist(range(num_terms)), numpy.zeros(num_terms), None
        )


class FakePhiDelta(PairwiseMetric):

    def __init__(self):
        self.phi_delta_mapping = {}

    def add_phi_delta_mapping(self, mapping):
        for (ci1, ci2), phi_delta in mapping.iteritems():
            phi_delta = numpy.asarray(phi_delta)
            self.phi_delta_mapping[(ci1, ci2)] = phi_delta
            if (ci2, ci1) not in mapping:
                self.phi_delta_mapping[(ci2, ci1)] = numpy.asarray([
                    phi_delta[:, 0], -phi_delta[:, 1]
                ]).transpose()

    def pairwise_evaluate(self, ci1, ci2):
        return self.phi_delta_mapping[(ci1, ci2)]

