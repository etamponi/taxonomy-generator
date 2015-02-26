import os

__author__ = 'Emanuele Tamponi'


def test_file_path(test_file):
    return os.path.join(os.path.dirname(__file__), "test_resources/", test_file)