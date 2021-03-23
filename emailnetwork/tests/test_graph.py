import os
from unittest import TestCase, mock

from emailnetwork.extract import MBoxReader
# from emailnetwork.graph import plot_single_email
import emailnetwork.graph as graph

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

@mock.patch(f"{__name__}.graph.plt")
def test_plot_single_directed(mock_plt):
    reader = MBoxReader(MBOX_PATH)
    graph.plot_single_directed(reader, 1, True)
    mock_plt.title.assert_called_once_with("Three tips to get the most out of Gmail\n Delivery date: 04/17/2020", fontdict={'fontname': 'Helvetica', 'color': 'k', 'fontweight': 'bold', 'fontsize': 8})
    assert mock_plt.figure.called


class TestGraph(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.emails = self.reader.extract()

    def test_single_graph(self):
        # TODO: to be implemented later
        pass
        
