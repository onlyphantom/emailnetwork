import os
from unittest import TestCase, mock

import emailnetwork.header as header
from emailnetwork.extract import MBoxReader
from emailnetwork.header import HeaderCounter
from numpy import histogram

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

class TestHeader(TestCase):
    
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.headers = HeaderCounter(self.reader)
        self.n_headers = 10

    def tearDown(self):
        self.reader = None

    def test_header_instance(self):
        self.assertTrue(isinstance(self.headers, HeaderCounter))
        self.assertTrue(isinstance(self.headers.__str__(), str))

    def test_header_plot(self):
        k, v = (list(self.headers.keys())[:self.n_headers], list(self.headers.values())[:self.n_headers])
        self.assertEqual(len(k), self.n_headers)
        self.assertEqual(len(v), self.n_headers)

    #@mock.patch("%s.header.plt" % __name__)
    def test_histogram(self):
        with mock.patch("%s.header.HeaderCounter.plt" % __name__) as patch:
            head = header.HeaderCounter(self.reader)
            head.histogram(self.n_headers)
            patch.title.assert_called_once_with("Email Header Analysis")
            assert patch.figure.called


        
