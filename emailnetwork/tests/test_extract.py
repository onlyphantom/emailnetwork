import os
from unittest import TestCase

from emailnetwork.extract import MBoxReader, extract_meta

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

class TestExtract(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)

    def tearDown(self):
        self.reader = None

    def test_read_mbox(self):
        self.assertTrue(isinstance(self.reader, MBoxReader))

    def test_length_mbox(self):
        self.assertEqual(len(self.reader), 140)

    def test_extract(self):
        pass

    def test_filter_by_date(self):
        pass

    def test_extract_meta_single(self):
        pass
