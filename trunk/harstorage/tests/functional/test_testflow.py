from harstorage.tests import *

class TestTestflowController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='testflow', action='index'))
        # Test response...
