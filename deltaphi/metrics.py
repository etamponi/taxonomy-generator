from copy import deepcopy
import numpy
from deltaphi.area_bounds import CheckerBoard

__author__ = 'Emanuele Tamponi'


class Metric(object):

    def evaluate(self, ci1, ci2):
        pass


class BinaryDiscriminant(Metric):

    def evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents - ci2.frequencies / ci2.documents


class BinaryCharacteristic(Metric):

    def evaluate(self, ci1, ci2):
        return ci1.frequencies / ci1.documents + ci2.frequencies / ci2.documents - 1.0


class Separability(Metric):

    def __init__(self, characteristic, discriminant):
        self.characteristic = characteristic
        self.discriminant = discriminant
        self.area_bounds = CheckerBoard("up", "down")

    def evaluate(self, ci1, ci2):
        phis = self.characteristic.evaluate(ci1, ci2)
        deltas = self.discriminant.evaluate(ci1, ci2)
        inside = self.area_bounds.is_inside(phis, deltas)
        return numpy.dot(abs(deltas) - abs(phis), inside) / inside.sum()