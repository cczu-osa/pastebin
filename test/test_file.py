import unittest
import os
from src import application


class TestFile(unittest.TestCase):
    def setUp(self):
        application.test_client()

    def test(self):
        self.assertTrue(os.path.isdir('data'))
        self.assertTrue(os.path.isfile('data/paste.db'))
