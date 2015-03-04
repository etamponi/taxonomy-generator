import numpy

__author__ = 'Emanuele Tamponi'


class AreaBounds(object):

    def isInside(self, phi, delta):
        pass


class Checker(AreaBounds):

    def __init__(self, active=None):
        if active is None:
            self.active = []
        else:
            self.active = active

    def isInside(self, phi, delta):
        n1 = [1, -1]
        n2 = [1, 1]
        c1 = numpy.dot(n1, [phi, delta])
        c2 = numpy.dot(n2, [phi, delta])
        is_up = (c1 <= 0) and (c2 >= 0)
        is_right = (c1 >= 0) and (c2 >= 0)
        is_down = (c1 >= 0) and (c2 <= 0)
        is_left = (c1 <= 0) and (c2 <= 0)
        if "up" in self.active and is_up:
            return True
        if "right" in self.active and is_right:
            return True
        if "down" in self.active and is_down:
            return True
        if "left" in self.active and is_left:
            return True
        return False
