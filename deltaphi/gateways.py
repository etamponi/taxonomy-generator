import csv

import numpy

from deltaphi.category_info import SingleCategoryInfo


__author__ = 'Emanuele Tamponi'


class Gateway(object):

    def open(self):
        pass


class CSVGateway(Gateway):

    def __init__(self, file_path):
        self.file_path = file_path
        self.terms = None
        self._term_positions = None

    def open(self):
        with open(self.file_path) as f:
            all_terms = set()
            for row in csv.reader(f):
                # row[0] -> category
                # row[1] -> documents
                row_terms = set(row[2].strip().split(" "))
                all_terms |= row_terms
            self.terms = sorted(all_terms)
            self._term_positions = {term: i for i, term in enumerate(self.terms)}

    def iterate(self):
        with open(self.file_path) as f:
            for row in csv.reader(f):
                category = row[0].strip()
                documents = int(row[1].strip())
                row_terms = row[2].strip().split(" ")
                row_frequencies = row[3].strip().split(" ")
                frequencies = numpy.zeros(len(self.terms))
                for term, frequency in zip(row_terms, row_frequencies):
                    frequencies[self._term_positions[term]] = frequency
                yield SingleCategoryInfo(category, documents, self.terms, frequencies)
