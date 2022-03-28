import os
from unittest import TestCase, mock
from collections import Counter

from emailnetwork.extract import MBoxReader
from emailnetwork.summary import DomainSummary, IncomingOutgoingSummary

import matplotlib.pyplot as plt

MBOX_PATH = f"{os.path.dirname(__file__)}/test.mbox"


class TestSummary(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.domain_summary = DomainSummary(self.reader)
        self.incoming_outgoing_summary = IncomingOutgoingSummary(self.reader)

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

    @mock.patch(f"{__name__}.plt")
    def test_domain_summary_plot(self, mock_plt):
        self.domain_summary.plot()
        assert mock_plt.figure.called

    @mock.patch(f"{__name__}.plt")
    def test_incoming_outgoing_plot(self, mock_plt):
        self.incoming_outgoing_summary.plot()
        mock_plt.set_title.assert_called_once_with(
            "Number of Incoming and Outgoing Emails per Month",
            fontdict={
                "fontname": "Helvetica",
                "color": "k",
                "fontweight": "bold",
                "fontsize": 12,
            },
        )
        assert mock_plt.figure.called
