import os

__author__ = 'Emanuele Tamponi'


TEST_RESOURCES = "test_resources/"


def test_file_path(test_file):
    return os.path.join(os.path.dirname(__file__), TEST_RESOURCES, test_file)
