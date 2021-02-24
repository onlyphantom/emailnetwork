import os
from unittest import TestCase
from collections import Counter

from emailnetwork.extract import MBoxReader
from emailnetwork.summary import DomainSummary

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

class TestSummary(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.summary = DomainSummary(self.reader)

    def tearDown(self):
        self.summary = None

    def test_summary_instance(self):
        self.assertTrue(isinstance(self.summary, DomainSummary))
        self.assertTrue(isinstance(self.summary.summary, Counter))

    def test_one_summary(self):
        for summary in self.summary.summary:
            self.assertTrue(isinstance(summary, str))
            self.assertTrue(isinstance(self.summary.summary[summary], int))
            self.assertGreater(self.summary.summary[summary], 0)