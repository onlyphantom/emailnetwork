import os
from telnetlib import DO
from unittest import TestCase, mock
from unittest.mock import MagicMock
from collections import Counter
from datetime import datetime

from emailnetwork.extract import MBoxReader
from emailnetwork.summary import DomainSummary, IncomingOutgoingSummary
from emailnetwork.header import HeaderCounter

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'


class TestSummary(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.domain_summary = DomainSummary(self.reader)
        self.incoming_outgoing_summary = IncomingOutgoingSummary(self.reader)
        self.headers = HeaderCounter(self.reader)

    def tearDown(self):
        self.domain_summary = None
        self.incoming_outgoing_summary = None

    def test_summary_instance(self):
        self.assertIsInstance(self.domain_summary, DomainSummary)
        self.assertIsInstance(self.domain_summary.summary, Counter)
        self.assertIsInstance(
            self.incoming_outgoing_summary, IncomingOutgoingSummary)
        self.assertIsInstance(
            self.incoming_outgoing_summary.summary, dict)

    def test_one_summary(self):
        for summary in self.domain_summary.summary:
            self.assertIsInstance(summary, str)
            self.assertIsInstance(
                self.domain_summary.summary[summary], int)
            self.assertGreater(self.domain_summary.summary[summary], 0)

        for summary in self.incoming_outgoing_summary.summary:
            self.assertIsInstance(summary, str)
            self.assertIsInstance(
                self.incoming_outgoing_summary.summary[summary], dict)
            for keys in self.incoming_outgoing_summary.summary[summary]:
                self.assertIn(keys, ('Incoming', 'Outgoing'))
                self.assertIsInstance(
                    self.incoming_outgoing_summary.summary[summary][keys], int)


    


