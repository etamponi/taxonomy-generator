import unittest

import numpy

import deltaphi.sources
from deltaphi.category_info import RawCategoryInfo, CategoryInfoFactory
from deltaphi.raw_filter import RawFilter
from deltaphi import test_file_path


__author__ = 'Emanuele Tamponi'


class TestRawSources(unittest.TestCase):

    def setUp(self):
        self.source_impls = [
            deltaphi.sources.CSVRawSource(test_file_path("example.csv"))
        ]
        self.expected_infos = [
            RawCategoryInfo("A", 100, {"a": 40, "b": 60}),
            RawCategoryInfo("B", 80, {"b": 20, "c": 70, "d": 30}),
            RawCategoryInfo("C", 30, {"a": 30, "c": 20})
        ]

    def test_open(self):
        for source in self.source_impls:
            source.open()
            self.assertEqual({"a", "b", "c", "d"}, source.terms)

    def test_iterate(self):
        for source in self.source_impls:
            source.open()
            for expected_info, actual_info in zip(self.expected_infos, source.iterate()):
                self.assertEqual(expected_info.category, actual_info.category)
                self.assertEqual(expected_info.documents, actual_info.documents)
                self.assertEqual(expected_info.term_frequencies, actual_info.term_frequencies)


class TestCategoryInfoSource(unittest.TestCase):

    def test_iterate(self):
        factory = CategoryInfoFactory({u"a", u"b", u"c", u"d"})
        expected_infos = [
            factory.build(RawCategoryInfo("A", 100, {u"a": 40, u"b": 60})),
            factory.build(RawCategoryInfo("B", 80, {u"b": 20, u"c": 70, u"d": 30})),
            factory.build(RawCategoryInfo("C", 30, {u"a": 30, u"c": 20}))
        ]
        source = deltaphi.sources.CategoryInfoSource(
            deltaphi.sources.CSVRawSource(test_file_path("example.csv")), RawFilter()
        )
        source.open()
        for expected_info, actual_info in zip(expected_infos, source.iterate()):
            self.assertEqual(expected_info.category, actual_info.category)
            self.assertEqual(expected_info.documents, actual_info.documents)
            numpy.testing.assert_array_equal(expected_info.frequencies, actual_info.frequencies)
