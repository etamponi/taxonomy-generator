import itertools

import numpy

from deltaphi.area_bounds import CheckerBoard


__author__ = 'Emanuele Tamponi'


class Metric(object):

    def evaluate(self, group):
        pass


class PairwiseMetric(Metric):

    def pairwise_evaluate(self, ci1, ci2):
        pass


class OnlyPairwiseMetric(PairwiseMetric):

    def evaluate(self, group):
        if len(group) != 2:
            return NotImplemented
        return self.pairwise_evaluate(group[0], group[1])


class Discriminant(OnlyPairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents - ci2.frequencies / ci2.documents


class Characteristic(OnlyPairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents + ci2.frequencies / ci2.documents - 1.0


class IntegralMetric(PairwiseMetric):

    def __init__(self, characteristic, discriminant, area_bounds):
        self.characteristic = characteristic
        self.discriminant = discriminant
        self.area_bounds = area_bounds

    def pairwise_evaluate(self, ci1, ci2):
        phis = self.characteristic.pairwise_evaluate(ci1, ci2)
        deltas = self.discriminant.pairwise_evaluate(ci1, ci2)
        inside = self.area_bounds.is_inside(phis, deltas)
        return self.integrate(phis, deltas, inside)

    def evaluate(self, group):
        metric = 1
        for ci1, ci2 in itertools.combinations(group, 2):
            metric = min(metric, self.pairwise_evaluate(ci1, ci2))
        return metric

    def integrate(self, phis, deltas, inside):
        pass


class Separability(IntegralMetric):

    def __init__(self):
        super(Separability, self).__init__(Characteristic(), Discriminant(), CheckerBoard("up", "down"))

    def integrate(self, phis, deltas, inside):
        return numpy.dot(abs(deltas) - abs(phis), inside) / inside.sum()


class Cohesion(IntegralMetric):

    def __init__(self):
        super(Cohesion, self).__init__(Characteristic(), Discriminant(), CheckerBoard("right"))

    def integrate(self, phis, deltas, inside):
        return numpy.dot(numpy.sqrt(phis**2 + deltas**2), inside) / inside.sum()


class RankingMetric(Metric):

    def __init__(self):
        self.separability = Separability()
        self.cohesion = Cohesion()

    def evaluate(self, group):
        return self.separability.evaluate(group) * self.cohesion.evaluate(group)
