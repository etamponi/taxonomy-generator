import numpy

__author__ = 'Emanuele Tamponi'


class AreaBounds(object):

    ALLOWED_ZONES = {"up": 0, "right": 1, "down": 2, "left": 3}

    def __init__(self, *active_zones):
        self._active = numpy.zeros((1, 4), dtype=int)
        for zone in (set(active_zones) & set(AreaBounds.ALLOWED_ZONES.keys())):
            self._active[0, AreaBounds.ALLOWED_ZONES[zone]] = 1

    def is_inside(self, phis, deltas):
        pass


class CheckerBoard(AreaBounds):

    def __init__(self, *active_zones):
        super(CheckerBoard, self).__init__(*active_zones)

    def is_inside(self, phis, deltas):
        a = phis - deltas
        b = phis + deltas
        matrix = numpy.asarray([
            numpy.logical_and(a <= 0, b >= 0),
            numpy.logical_and(a >= 0, b >= 0),
            numpy.logical_and(a >= 0, b <= 0),
            numpy.logical_and(a <= 0, b <= 0)
        ])
        return numpy.sign(numpy.dot(self._active, matrix)[0])