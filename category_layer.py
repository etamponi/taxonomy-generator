__author__ = 'Emanuele Tamponi'


class CategoryLayer(object):

    def __init__(self, iterable):
        self.groups = []
        for ci in iterable:
            self.groups.append({ci})
