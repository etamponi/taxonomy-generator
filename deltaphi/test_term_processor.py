import unittest

from deltaphi.term_processor import TermProcessor


__author__ = 'Emanuele Tamponi'


class TestTermProcessor(unittest.TestCase):

    def test_filter_terms_min_length(self):
        original_terms = [u"a", u"aa", u"aaa", u"aaaa"]
        expected_terms_1 = [u"aaa", u"aaaa"]
        expected_terms_2 = [u"aa", u"aaa", u"aaaa"]
        tp = TermProcessor(min_length=3)
        self.assertEqual(expected_terms_1, tp.filter(original_terms))
        tp = TermProcessor(min_length=2)
        self.assertEqual(expected_terms_2, tp.filter(original_terms))

    def test_filter_lemmatize(self):
        original_terms = [u"testing", u"taken", u"loved", u"reported"]
        expected_terms = [u"test", u"take", u"love", u"report"]
        tp = TermProcessor(min_length=1)
        self.assertEqual(expected_terms, tp.filter(original_terms))

    def test_transform_term(self):
        tp = TermProcessor(min_length=3)
        self.assertEqual(None, tp.transform(u"a"))
        self.assertEqual(None, tp.transform(u"aa"))
        self.assertEqual(u"take", tp.transform(u"taken"))

    def test_stopwords(self):
        original_terms = [u"a", u"an", u"the", u"test"]
        expected_terms = [u"test"]
        tp = TermProcessor(min_length=1)
        self.assertEqual(expected_terms, tp.filter(original_terms))
