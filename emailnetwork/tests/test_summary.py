import os
import matplotlib.pyplot as plt
from unittest import TestCase, mock
from collections import Counter

from emailnetwork.extract import MBoxReader
from emailnetwork.summary import DomainSummary, IncomingOutgoingSummary
from emailnetwork.header import HeaderCounter

import emailnetwork.summary as summary

MBOX_PATH = f"{os.path.dirname(__file__)}/test.mbox"


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
        self.assertIsInstance(self.incoming_outgoing_summary, IncomingOutgoingSummary)
        self.assertIsInstance(self.incoming_outgoing_summary.summary, dict)

    def test_one_summary(self):
        for summary in self.domain_summary.summary:
            self.assertIsInstance(summary, str)
            self.assertIsInstance(self.domain_summary.summary[summary], int)
            self.assertGreater(self.domain_summary.summary[summary], 0)

        for summary in self.incoming_outgoing_summary.summary:
            self.assertIsInstance(summary, str)
            self.assertIsInstance(self.incoming_outgoing_summary.summary[summary], dict)
            for keys in self.incoming_outgoing_summary.summary[summary]:
                self.assertIn(keys, ("Incoming", "Outgoing"))
                self.assertIsInstance(
                    self.incoming_outgoing_summary.summary[summary][keys], int
                )

    def test_header(self):
        self.assertIsInstance(self.headers, HeaderCounter)

    @mock.patch(f"{__name__}.summary.plt")
    def test_mock_plot(self, mock_plt):
        reader = MBoxReader(MBOX_PATH)
        ds = DomainSummary(reader=reader)
        ds.plot()
        mock_plt.title.assert_called_once_with(
            "Sender's Domain Occurences",
            fontdict={
                "fontname": "Helvetica",
                "color": "k",
                "fontweight": "bold",
                "fontsize": 12,
            },
        )
        assert mock_plt.figure.called
