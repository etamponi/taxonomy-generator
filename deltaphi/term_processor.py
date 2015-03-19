__author__ = 'Emanuele Tamponi'


class TermProcessor(object):

    def __init__(self, min_length):
        self.min_length = min_length

    def filter(self, terms):
        return [term for term in terms if len(term) >= self.min_length]
