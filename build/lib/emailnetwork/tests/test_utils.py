import os
from unittest import TestCase

from emailnetwork.extract import MBoxReader

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

class TestNetwork(TestCase):
    def setUp(self):
        # self.reader = MBoxReader(MBOX_PATH)
        # self.emails = self.reader.extract()
        pass

    # test PeopleCombination

