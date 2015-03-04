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
