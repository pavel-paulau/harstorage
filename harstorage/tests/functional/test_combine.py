from harstorage.tests import *

class TestCombineController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='combine', action='index'))
        # Test response...
