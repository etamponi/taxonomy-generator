# coding=utf-8

import unittest

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

from deltaphi.category_info import RawCategoryInfo
from deltaphi.filter import Filter


__author__ = 'Emanuele Tamponi'


class TestFilter(unittest.TestCase):

    def test_min_length(self):
        original_rci = RawCategoryInfo("A", 100, {"a": 10, "aa": 20, "aaa": 30, "aaaa": 40})
        expected_rci_1 = RawCategoryInfo("A", 100, {u"aaa": 30, u"aaaa": 40})
        expected_rci_2 = RawCategoryInfo("A", 100, {u"aa": 20, u"aaa": 30, u"aaaa": 40})
        filter = Filter(min_length=3)
        self.assertEqual(expected_rci_1.term_frequencies, filter.apply(original_rci).term_frequencies)
        filter = Filter(min_length=2)
        self.assertEqual(expected_rci_2.term_frequencies, filter.apply(original_rci).term_frequencies)

    def test_lemmatize(self):
        original_rci = RawCategoryInfo("A", 100, {"testing": 10, "taken": 20, "loved": 30, "reported": 40})
        expected_rci = RawCategoryInfo("A", 100, {u"test": 10, u"take": 20, u"love": 30, u"report": 40})
        filter = Filter(lemmatizer=WordNetLemmatizer())
        self.assertEqual(expected_rci.term_frequencies, filter.apply(original_rci).term_frequencies)

    def test_stopwords(self):
        original_rci = RawCategoryInfo("A", 100, {"a": 10, "an": 20, "do": 30, "test": 40})
        expected_rci = RawCategoryInfo("A", 100, {u"test": 40})
        filter = Filter(stopwords=stopwords.words("english"))
        self.assertEqual(expected_rci.term_frequencies, filter.apply(original_rci).term_frequencies)

    def test_unicode(self):
        original = RawCategoryInfo("A", 100, {"è": 1, "à": 1, "ì": 1, "ò": 1, "ù": 1, "é": 1, "ç": 1, "§": 1})
        expected = RawCategoryInfo("A", 100, {u"è": 1, u"à": 1, u"ì": 1, u"ò": 1, u"ù": 1, u"é": 1, u"ç": 1, u"§": 1})
        filter = Filter()
        self.assertNotEqual(original.term_frequencies, filter.apply(original).term_frequencies)
        self.assertEqual(expected.term_frequencies, filter.apply(original).term_frequencies)
