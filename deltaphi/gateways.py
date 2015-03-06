import csv

from deltaphi.category_info import CategoryInfoBuilder


__author__ = 'Emanuele Tamponi'


class Gateway(object):

    def open(self):
        pass


class CSVGateway(Gateway):

    def __init__(self, file_path):
        self.file_path = file_path
        self.builder = None

    def open(self):
        with open(self.file_path) as f:
            all_terms = set()
            for row in csv.reader(f):
                # row[0] -> category
                # row[1] -> documents
                row_terms = set(row[2].strip().split(" "))
                all_terms |= row_terms
            self.builder = CategoryInfoBuilder(all_terms)

    def iterate(self):
        with open(self.file_path) as f:
            for row in csv.reader(f):
                category = row[0].strip()
                documents = int(row[1].strip())
                row_terms = row[2].strip().split(" ")
                row_frequencies = row[3].strip().split(" ")
                yield self.builder.build_leaf(category, documents, dict(zip(row_terms, row_frequencies)))
