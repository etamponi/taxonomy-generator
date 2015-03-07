import itertools

import numpy

from deltaphi.area_bounds import CheckerBoard


__author__ = 'Emanuele Tamponi'


class Metric(object):

    def evaluate(self, *infos):
        pass


class PairwiseMetric(Metric):

    def pairwise_evaluate(self, ci1, ci2):
        pass

    def evaluate(self, *infos):
        if len(infos) != 2:
            return NotImplemented
        return self.pairwise_evaluate(*infos)


class Discriminant(PairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents - ci2.frequencies / ci2.documents


class Characteristic(PairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents + ci2.frequencies / ci2.documents - 1.0


class Separability(Metric):

    def __init__(self, characteristic, discriminant):
        self.characteristic = characteristic
        self.discriminant = discriminant
        self.area_bounds = CheckerBoard("up", "down")

    def evaluate(self, *infos):
        sep = 1
        for ci1, ci2 in itertools.combinations(infos, 2):
            phis = self.characteristic.evaluate(ci1, ci2)
            deltas = self.discriminant.evaluate(ci1, ci2)
            inside = self.area_bounds.is_inside(phis, deltas)
            sep = min(sep, numpy.dot(abs(deltas) - abs(phis), inside) / inside.sum())
        return sep


class Cohesion(Metric):

    def __init__(self, characteristic, discriminant):
        self.characteristic = characteristic
        self.discriminant = discriminant
        self.area_bounds = CheckerBoard("right")

    def evaluate(self, *infos):
        coh = 1
        for ci1, ci2 in itertools.combinations(infos, 2):
            phis = self.characteristic.evaluate(ci1, ci2)
            deltas = self.discriminant.evaluate(ci1, ci2)
            inside = self.area_bounds.is_inside(phis, deltas)
            coh = min(coh, numpy.dot(numpy.sqrt(phis**2 + deltas**2), inside) / inside.sum())
        return coh
