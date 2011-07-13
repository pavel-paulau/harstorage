from harstorage.tests import *

class TestResultsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='results', action='index'))
        # Test response...
