import csv

from deltaphi.category_info import RawCategoryInfo, CategoryInfoFactory


__author__ = 'Emanuele Tamponi'


class RawSource(object):

    def open(self):
        pass

    def iterate(self):
        pass


class CSVRawSource(RawSource):

    def __init__(self, file_path):
        self.file_path = file_path
        self.terms = None

    def open(self):
        with open(self.file_path) as f:
            all_terms = set()
            for row in csv.reader(f):
                # row[0] -> category
                # row[1] -> documents
                row_terms = set(row[2].strip().split(" "))
                all_terms |= row_terms
            self.terms = all_terms

    def iterate(self):
        with open(self.file_path) as f:
            for row in csv.reader(f):
                category = row[0].strip()
                documents = int(row[1].strip())
                row_terms = row[2].strip().split(" ")
                row_frequencies = map(int, row[3].strip().split(" "))
                yield RawCategoryInfo(category, documents, dict(zip(row_terms, row_frequencies)))


class CategoryInfoSource(object):

    def __init__(self, raw_source, preprocessor):
        self.raw_source = raw_source
        self.preprocessor = preprocessor
        self.factory = None

    def open(self):
        self.raw_source.open()
        temporary = RawCategoryInfo("", 0, {term: 0 for term in self.raw_source.terms})
        terms = self.preprocessor.process(temporary).term_frequencies.keys()
        self.factory = CategoryInfoFactory(terms)

    def iterate(self):
        for raw in self.raw_source.iterate():
            raw = self.preprocessor.process(raw)
            yield self.factory.build(raw)
