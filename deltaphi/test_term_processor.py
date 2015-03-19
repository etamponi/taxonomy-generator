import unittest

from deltaphi.term_processor import TermProcessor


__author__ = 'Emanuele Tamponi'


class TestTermProcessor(unittest.TestCase):

    def test_filter_terms(self):
        original_terms = [u"a", u"aa", u"aaa", u"aaaa"]
        expected_terms_1 = [u"aaa", u"aaaa"]
        expected_terms_2 = [u"aa", u"aaa", u"aaaa"]
        tp = TermProcessor(min_length=3)
        self.assertEqual(expected_terms_1, tp.filter(original_terms))
        tp = TermProcessor(min_length=2)
        self.assertEqual(expected_terms_2, tp.filter(original_terms))
