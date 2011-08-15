from harstorage.tests import *

class TestChartController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='chart', action='index'))
        # Test response...
