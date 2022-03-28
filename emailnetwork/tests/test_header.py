import os
from unittest import TestCase, mock
from collections import Counter

from emailnetwork.extract import MBoxReader
from emailnetwork.header import HeaderCounter

import matplotlib.pyplot as plt

MBOX_PATH = f"{os.path.dirname(__file__)}/test.mbox"


class TestHeader(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.headers = HeaderCounter(self.reader)

    def tearDown(self):
        self.headers = None

    def test_header(self):
        self.assertIsInstance(self.headers, HeaderCounter)

    @mock.patch(f"{__name__}.plt")
    def test_histogram(self, mock_plt):
        HeaderCounter.histogram(self.headers, n=10)
        assert mock_plt.figure.called
