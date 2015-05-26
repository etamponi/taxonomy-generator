import itertools

import numpy

from deltaphi import shapes

__author__ = 'Emanuele Tamponi'


class PairwiseMetric(object):

    def pairwise_evaluate(self, ci1, ci2):
        pass


class Discriminant(PairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents - ci2.frequencies / ci2.documents


class Characteristic(PairwiseMetric):

    def pairwise_evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents + ci2.frequencies / ci2.documents - 1.0


class PhiDelta(PairwiseMetric):

    def __init__(self):
        self.characteristic = Characteristic()
        self.discriminant = Discriminant()

    def pairwise_evaluate(self, ci1, ci2):
        return numpy.vstack((
            self.characteristic.pairwise_evaluate(ci1, ci2),
            self.discriminant.pairwise_evaluate(ci1, ci2)
        )).transpose()


class GroupMetric(object):

    def evaluate(self, group):
        pass


class CharacteristicTerms(GroupMetric):

    def __init__(self, characteristic_area=shapes.PSphere(center=numpy.asarray([1.0, 0.0]), radius=1, p=1)):
        """
        :type characteristic_area: shapes.Shape
        """
        self.phi_delta = PhiDelta()
        self.area = shapes.PSphere(numpy.asarray([0.0, 0.0]), 1, 1) & characteristic_area

    def evaluate(self, group):
        insiders = numpy.zeros(len(group.terms))
        for ci1, ci2 in group.one_vs_siblings():
            insiders += self.area.contains(self.phi_delta.pairwise_evaluate(ci1, ci2))
        # Majority vote
        return numpy.asarray(insiders > (len(group) / 2), dtype=int)


class IntegralMetric(GroupMetric):

    def __init__(self, area):
        """
        :type area: shapes.Shape
        """
        self.phi_delta = PhiDelta()
        self.area = shapes.PSphere(numpy.asarray([0.0, 0.0]), 1, 1) & area

    def pairwise_evaluate(self, ci1, ci2):
        points = self.phi_delta.pairwise_evaluate(ci1, ci2)
        inside = self.area.contains(points)
        return self.integrate(points, inside)

    def evaluate(self, group):
        metric = 1
        for ci1, ci2 in itertools.combinations(group, 2):
            metric = min(metric, self.pairwise_evaluate(ci1, ci2))
        return metric

    def integrate(self, points, inside):
        pass


class Separability(IntegralMetric):

    def __init__(self):
        super(Separability, self).__init__(
            shapes.PSphere(numpy.asarray([0.0, 1.0]), 1, 1) | shapes.PSphere(numpy.asarray([0.0, -1.0]), 1, 1)
        )

    def integrate(self, points, inside):
        den = inside.sum()
        return numpy.dot(abs(points[:, 1]) - abs(points[:, 0]), inside) / den if den > 0 else 0


class Cohesion(IntegralMetric):

    def __init__(self):
        super(Cohesion, self).__init__(shapes.PSphere(numpy.asarray([1.0, 0.0]), 1, 1))

    def integrate(self, points, inside):
        den = inside.sum()
        return numpy.dot(numpy.sqrt(numpy.sum(points**2, axis=1)), inside) / den if den > 0 else 0


class GroupScore(GroupMetric):

    def __init__(self):
        self.separability = Separability()
        self.cohesion = Cohesion()

    def evaluate(self, group):
        return self.separability.evaluate(group) * self.cohesion.evaluate(group)


class LayerMetric(object):

    def evaluate(self, layer):
        pass


class LayerScore(LayerMetric):

    def evaluate(self, layer):
        pass
