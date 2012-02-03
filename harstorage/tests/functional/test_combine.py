from harstorage.tests import *

class TestCombineController(TestController):

    """
    Test suite for consolidation of static resources

    """

    def test_01_combine_styles(self):
        """Combine common styles"""

        # Expected valid response
        response = self.app.get(
            url(controller='combine', action='styles'),
            params = {'ver': '1.0', 'main.css': '', 'tabber.css' : '',
                      'datatables/table_jui.css': '',
                      'datatables/ColReorder.css': '',
                      'datatables/TableTools_JUI.css': ''},
            status = 200)

        # Response body
        assert response.content_type == 'text/css'

    def test_02_combine_missing_styles(self):
        """Combine missing styles"""

        # Expected 404 status code
        response = self.app.get(
            url(controller='combine', action='styles'),
            params = {'ver': '1.0', 'imnotexistingfile.css': ''},
            status = 404)

        # Response body
        assert '404 Not Found' in response.body

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert response.tmpl_context.message == '404 Not Found'