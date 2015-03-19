# coding: utf-8

import unittest

from deltaphi import test_file_path
from deltaphi.gateways import CSVGateway


__author__ = 'Emanuele Tamponi'


class TestUnicode(unittest.TestCase):

    def test_unicode(self):
        gateway = CSVGateway(test_file_path("unicode.csv"))
        gateway.open()
        string_terms = ["è", "à", "ì", "ò", "ù", "é", "°", "ç", "§"]
        unicode_terms = map(lambda t: unicode(t, "utf-8"), string_terms)
        self.assertNotEqual(set(string_terms), set(gateway.builder.terms))
        self.assertEqual(set(unicode_terms), set(gateway.builder.terms))
