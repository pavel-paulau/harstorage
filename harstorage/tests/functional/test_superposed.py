import pymongo
import time

from harstorage.tests import *

class TestTestflowController(TestController):

    """
    Test suite for aggregation of test results

    """

    def test_01_init(self):
        """Init data for Superposed"""

        # Add valid file
        with open('harstorage/tests/functional/testdata/validfile.har') as file:
            self.app.post(
                url(controller='results', action='upload'),
                params = {'file' : file.read()},
                status = 302
            )

        time.sleep(1)

    def test_02_create(self):
        """Valid GET request for create form"""

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='create'),
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert type(response.tmpl_context.labels) == type([])

    def test_03_dates(self):
        """Dates for label"""

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='dates'),
            params = {'label' : 'validfile',},
            status = 200
        )

        # Template context
        assert response.body.find(';') == -1

    def test_04_display_average(self):
        """Display superposed - Average"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='display'),
            params = {
                'step_1_label'    : 'validfile',
                'step_1_start_ts' : timestamp,
                'step_1_end_ts'   : timestamp,
                'metric'          : 'Average'
            },
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert len(response.tmpl_context.metrics_table) == 5

    def test_05_display_median(self):
        """Display superposed - Median"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='display'),
            params = {
                'step_1_label'    : 'validfile',
                'step_1_start_ts' : timestamp,
                'step_1_end_ts'   : timestamp,
                'metric'          : 'Median'
            },
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert len(response.tmpl_context.metrics_table) == 5

    def test_06_display_minimum(self):
        """Display superposed - Minimum"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='display'),
            params = {
                'step_1_label'    : 'validfile',
                'step_1_start_ts' : timestamp,
                'step_1_end_ts'   : timestamp,
                'metric'          : 'Minimum'
            },
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert len(response.tmpl_context.metrics_table) == 5

    def test_07_display_maximum(self):
        """Display superposed - Maximum"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='display'),
            params = {
                'step_1_label'    : 'validfile',
                'step_1_start_ts' : timestamp,
                'step_1_end_ts'   : timestamp,
                'metric'          : 'Maximum'
            },
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert len(response.tmpl_context.metrics_table) == 5

    def test_08_display_percentile(self):
        """Display superposed - 90th Percentile"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        response = self.app.get(
            url(controller='superposed', action='display'),
            params = {
                'step_1_label'    : 'validfile',
                'step_1_start_ts' : timestamp,
                'step_1_end_ts'   : timestamp,
                'metric'          : '90th Percentile'
            },
            status = 200
        )

        # Template context
        assert response.tmpl_context.rev == response.config['app_conf']['static_version']

        assert len(response.tmpl_context.metrics_table) == 5

    def test_09_close(self):
        """Clear test data from Superposed"""

        # Fetch data from database
        connection = pymongo.Connection('localhost', 27017)
        db = connection['harstorage']
        collection = db['results']

        timestamp = collection.find_one({"label":'validfile'})['timestamp']

        # Successful response
        self.app.get(
            url(controller='results', action='deleterun'),
            params = {'label'     : 'validfile',
                      'timestamp' : timestamp,
                      'mode'      : 'label',
                      'all'       : 'true'},
            status = 200
        )