import unittest

from category_layer import CategoryLayer
from deltaphi import test_file_path
from deltaphi.gateways import CSVGateway


__author__ = 'Emanuele Tamponi'


class TestCategoryLayer(unittest.TestCase):

    def setUp(self):
        self.gateway = CSVGateway(test_file_path("example.csv"))
        self.gateway.open()
        self.infos = list(self.gateway.iterate())
        self.layer = CategoryLayer(self.infos)

    def test_layer_init(self):
        self.assertEqual(3, len(self.layer.groups))
        self.assertEqual([{info} for info in self.infos], self.layer.groups)

    def test_layer_explore(self):
        pass