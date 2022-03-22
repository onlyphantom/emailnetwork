import os
from unittest import TestCase, mock

from emailnetwork.extract import MBoxReader
# from emailnetwork.graph import plot_single_email
import emailnetwork.graph as graph

MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'


class TestGraph(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.emails = self.reader.extract()
        self.layout = ['shell', 'spring', 'spiral']

    def test_single_graph(self):
        # TODO: to be implemented later
        pass

    @mock.patch(f"{__name__}.graph.plt")
    def test_plot_single_directed(self, mock_plt):
        graph.plot_single_directed(self.reader, 1, True)
        mock_plt.title.assert_called_once_with("Three tips to get the most out of Gmail\n Delivery date: 04/17/2020", fontdict={'fontname': 'Helvetica', 'color': 'k', 'fontweight': 'bold', 'fontsize': 8})
        assert mock_plt.figure.called


    def test_plot_single_undirected(self):
        with mock.patch("%s.graph.plt" % __name__) as patch, mock.patch("%s.graph.nx" % __name__) as patch2:
            graph.plot_single_undirected(self.reader,2, True)
            patch.title.assert_called_once_with("Stay more organized with Gmail's inbox\n Delivery date: 08/13/2020", fontdict={'fontname': 'Helvetica', 'color': 'k', 'fontweight': 'bold', 'fontsize': 8})  
            patch2.Graph.assert_called_once_with(name='Single Email Social Network')  


    def test_plot_directed(self):
        with mock.patch("%s.graph.plt" % __name__) as patch:
            for item in self.layout:
                graph.plot_directed(self.reader, item)
                assert patch.figure.called
    
    def test_plot_undirected(self):
        with mock.patch("%s.graph.plt" % __name__) as patch:
            for item in self.layout:
                graph.plot_undirected(self.reader, item)
                assert patch.figure.called
        
