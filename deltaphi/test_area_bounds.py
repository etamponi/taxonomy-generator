import unittest
from deltaphi.area_bounds import Checker

__author__ = 'Emanuele Tamponi'


class TestAreaBounds(unittest.TestCase):

    def test_checker(self):
        area = Checker(active=["up"])
        self.assertTrue(area.isInside(delta=1.0, phi=0.0))
        self.assertTrue(area.isInside(delta=0.5, phi=0.5))
        self.assertTrue(area.isInside(delta=0.0, phi=0.0))
        self.assertTrue(area.isInside(delta=0.5, phi=-0.5))
        self.assertFalse(area.isInside(delta=0.0, phi=0.5))
        self.assertFalse(area.isInside(delta=0.0, phi=-0.5))
        area = Checker(active=["left"])
        self.assertTrue(area.isInside(delta=0.0, phi=-0.5))
        self.assertFalse(area.isInside(delta=0.0, phi=0.5))
