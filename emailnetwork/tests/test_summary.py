import os
from unittest import TestCase
from collections import Counter
from datetime import datetime

from emailnetwork.extract import MBoxReader
from emailnetwork.summary import DomainSummary, IncomingOutgoingSummary

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'


class TestSummary(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.domain_summary = DomainSummary(self.reader)
        self.incoming_outgoing_summary = IncomingOutgoingSummary(self.reader)

    def tearDown(self):
        self.domain_summary = None
        self.incoming_outgoing_summary = None

    def test_summary_instance(self):
        self.assertTrue(isinstance(self.domain_summary, DomainSummary))
        self.assertTrue(isinstance(self.domain_summary.summary, Counter))
        self.assertTrue(isinstance(
            self.incoming_outgoing_summary, IncomingOutgoingSummary))
        self.assertTrue(isinstance(
            self.incoming_outgoing_summary.summary, dict))

    def test_one_summary(self):
        for summary in self.domain_summary.summary:
            self.assertTrue(isinstance(summary, str))
            self.assertTrue(isinstance(
                self.domain_summary.summary[summary], int))
            self.assertGreater(self.domain_summary.summary[summary], 0)

        for summary in self.incoming_outgoing_summary.summary:
            self.assertTrue(isinstance(summary, str))
            self.assertTrue(isinstance(
                self.incoming_outgoing_summary.summary[summary], dict))
            for keys in self.incoming_outgoing_summary.summary[summary]:
                self.assertIn(keys, ('Incoming', 'Outgoing'))
                self.assertIsInstance(
                    self.incoming_outgoing_summary.summary[summary][keys], int)
