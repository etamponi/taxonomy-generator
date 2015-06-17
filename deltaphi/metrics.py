import itertools

import numpy

from deltaphi import shapes
from deltaphi import category_info

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
        self._computed = {}

    def pairwise_evaluate(self, ci1, ci2):
        if (ci1, ci2) not in self._computed:
            phis = self.characteristic.pairwise_evaluate(ci1, ci2)
            deltas = self.discriminant.pairwise_evaluate(ci1, ci2)
            self._computed[(ci1, ci2)] = numpy.vstack((phis, deltas)).transpose()
            self._computed[(ci2, ci1)] = numpy.vstack((phis, -deltas)).transpose()
        return self._computed[(ci1, ci2)]


class GroupMetric(object):

    def evaluate(self, group):
        pass


class IntegralMetric(GroupMetric):

    def __init__(self, area, phi_delta=PhiDelta()):
        """
        :type area: shapes.Shape
        """
        self.phi_delta = phi_delta
        self.area = area

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

    DEFAULT_AREA = (
        shapes.PSphere([0, 1], 1, 1) | shapes.PSphere([0, -1], 1, 1)
    )

    def __init__(self, area=DEFAULT_AREA, phi_delta=PhiDelta()):
        super(Separability, self).__init__(area, phi_delta)

    def integrate(self, points, inside):
        den = inside.sum()
        return numpy.dot(abs(points[:, 1]) - abs(points[:, 0]), inside) / den if den > 0 else 0


class Cohesion(IntegralMetric):

    DEFAULT_AREA = shapes.PSphere([1.0, 0.0], 1, 1)

    def __init__(self, area=DEFAULT_AREA, phi_delta=PhiDelta()):
        super(Cohesion, self).__init__(area, phi_delta)

    def integrate(self, points, inside):
        den = inside.sum()
        # noinspection PyTypeChecker
        return numpy.dot(numpy.sqrt(numpy.sum(points**2, axis=1)), inside) / den if den > 0 else 0


class GeometricMeanScore(GroupMetric):

    def __init__(self, cohesion=Cohesion(), separability=Separability()):
        self.cohesion = cohesion
        self.separability = separability

    def evaluate(self, group):
        return self.separability.evaluate(group) * self.cohesion.evaluate(group)


class CharacteristicTerms(GroupMetric):

    def __init__(self, characteristic_area=Cohesion.DEFAULT_AREA, phi_delta=PhiDelta()):
        self.phi_delta = phi_delta
        self.area = characteristic_area

    def evaluate(self, group):
        insiders = numpy.zeros(len(group.terms))
        for ci1, ci2 in group.one_vs_siblings():
            insiders += self.area.contains(self.phi_delta.pairwise_evaluate(ci1, ci2))
        # Majority vote
        # noinspection PyTypeChecker
        return numpy.asarray(insiders > (len(group) / 2), dtype=int)


class PairwiseCharacteristicTerms(GroupMetric):

    def __init__(self, characteristic_area=Cohesion.DEFAULT_AREA, phi_delta=PhiDelta()):
        self.phi_delta = phi_delta
        self.area = characteristic_area

    def evaluate(self, group):
        count = numpy.zeros(len(group.terms))
        for ci1, ci2 in itertools.combinations(group, 2):
            count += self.area.contains(self.phi_delta.pairwise_evaluate(ci1, ci2))
        return numpy.asarray(count > (len(group) / 2), dtype=int)


class LayerMetric(object):

    def evaluate(self, layer):
        pass


class DiscriminantTerms(LayerMetric):

    def __init__(self, discriminant_area=Separability.DEFAULT_AREA, phi_delta=PhiDelta()):
        self.area = discriminant_area
        self.phi_delta = phi_delta

    def evaluate(self, layer):
        """
        :type layer: category_info.CategoryLayer
        """
        if not layer.is_singleton_layer():
            raise Exception("DiscriminantTerms can only be evaluated for singleton layers")
        group_all = category_info.CategoryGroup([group[0] for group in layer.groups])
        metric_map = {}
        for ci1, ci2 in group_all.one_vs_siblings():
            metric_map[ci1] = self.area.contains(self.phi_delta.pairwise_evaluate(ci1, ci2))
        return metric_map


class PairwiseDiscriminantTerms(LayerMetric):

    def __init__(self, discriminant_area=Separability.DEFAULT_AREA, phi_delta=PhiDelta()):
        self.area = discriminant_area
        self.phi_delta = phi_delta

    def evaluate(self, layer):
        """
        :type layer: category_info.CategoryLayer
        """
        if not layer.is_singleton_layer():
            raise Exception("PairwiseDiscriminantTerms can only be evaluated for singleton layers")
        ret = {}
        for ci1 in map(lambda g: g[0], layer.groups):
            count = numpy.zeros(len(ci1.terms))
            for ci2 in map(lambda g: g[0], layer.groups):
                if ci1 == ci2:
                    continue
                count += self.area.contains(self.phi_delta.pairwise_evaluate(ci1, ci2))
            ret[ci1] = numpy.asarray(count > ((len(layer.groups)-1) / 2), dtype=int)
        return ret


class LookAhead(LayerMetric):

    def __init__(self, characteristic_terms=CharacteristicTerms(), discriminant_terms=DiscriminantTerms()):
        self.characteristic_terms = characteristic_terms
        self.discriminant_terms = discriminant_terms

    def evaluate(self, layer):
        ret = 0
        for ci, dt in self.discriminant_terms.evaluate(layer).iteritems():
            if ci.child_group is None:
                continue
            ct = self.characteristic_terms.evaluate(ci.child_group)
            ret += numpy.sum(dt * ct)
        return ret
