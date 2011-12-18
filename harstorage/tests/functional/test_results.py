from harstorage.tests import *

class TestResultsController(TestController):

    """
    Test suite for test results

    """

    def test_index_get(self):
        """Valid GET request"""

        # Successful response
        response = self.app.get(
            url(controller='results', action='index')
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert response.tmpl_context.rowcount > 0

    def test_index_post(self):
        """Prohibeted POST request"""

        # Expected 405 status code
        response = self.app.post(
            url(controller='results', action='index'),
            status = 405
        )

        assert 'The method POST is not allowed for this resource.' in response.body

    def test_index_404(self):
        """Error document"""

        # Expected 404 status code
        response = self.app.get(
            url('/404'),
            status = 404
        )

        # Response body
        assert '404 Not Found' in response.body

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert response.tmpl_context.message == '404 Not Found'