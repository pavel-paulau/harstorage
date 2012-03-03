import pymongo
import json
import time

from harstorage.tests import *

class TestResultsController(TestController):

    """
    Test suite for test results

    """

    def test_01_upload_empty(self):
        """Upload empty file"""

        # Expected valid response
        response = self.app.post(
            url(controller="results", action="upload"),
            params = {"file": ""},
            status = 200)

        # Response body
        assert "Empty file" in response.body

        # Template context
        assert response.tmpl_context.error == "Empty file"

    def test_02_upload_empty_auto(self):
        """Upload empty file in automated mode"""

        # Expected valid response
        response = self.app.post(
            url(controller="results", action="upload"),
            params = {"file": ""},
            headers = {"Automated": "true"},
            status = 200)

        # Response body
        assert response.body == "Empty file"

    def test_03_upload_valid_file(self):
        """Upload valid file"""

        # Database collection
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        # Check data in database before
        before = collection.find({"label":"validfile"}).count()

        # Expected redirect
        with open("harstorage/tests/functional/testdata/validfile.har") as file:
            response = self.app.post(
                url(controller="results", action="upload"),
                params = {"file": file.read()},
                status = 302)

        # Response header
        assert "results/details?label=validfile" in response.location

        time.sleep(1)

        # Check data in database before
        after = collection.find({"label":"validfile"}).count()

        assert after - before == 1

    def test_04_upload_valid_file_auto(self):
        """Upload valid file in automated mode"""

        # Database collection
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        # Check data in database before
        before = collection.find({"label":"validfile"}).count()

        # Expected redirect
        with open("harstorage/tests/functional/testdata/validfile.har") as file:
            response = self.app.post(
                url(controller="results", action="upload"),
                params = {"file": file.read()},
                headers = {"Automated": "true"},
                status = 200)

        # Response header
        assert response.body == "Successful"

        time.sleep(1)

        # Check data in database before
        after = collection.find({"label": "validfile"}).count()

        assert after - before == 1

    def test_05_index_get(self):
        """Valid GET request"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="index"),
            status = 200)

        # Template context
        assert response.tmpl_context.rev == response.config["app_conf"]["static_version"]

        assert response.tmpl_context.rowcount > 0

    def test_06_index_post(self):
        """Prohibited POST request"""

        # Expected 405 status code
        response = self.app.post(
            url(controller="results", action="index"),
            status = 405)

        # Response body
        assert "405 Method Not Allowed" in response.body

        # Template context
        assert response.tmpl_context.rev == response.config["app_conf"]["static_version"]

        assert response.tmpl_context.message == "405 Method Not Allowed"

    def test_07_index_404(self):
        """Error document"""

        # Expected 404 status code
        response = self.app.get(
            url("/404"),
            status = 404)

        # Response body
        assert "404 Not Found" in response.body

        # Template context
        assert response.tmpl_context.rev == response.config["app_conf"]["static_version"]

        assert response.tmpl_context.message == "404 Not Found"

    def test_08_details_label(self):
        """Test results - label"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="details"),
            params = {"label": "validfile"},
            status = 200)

        # Template context
        assert response.tmpl_context.rev == response.config["app_conf"]["static_version"]
        assert response.tmpl_context.label == "validfile"

    def test_09_details_url(self):
        """Test results - url"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="details"),
            params = {"url": "http://valid.host/"},
            status = 200)

        # Template context
        assert response.tmpl_context.rev == response.config["app_conf"]["static_version"]
        assert response.tmpl_context.label == "http://valid.host/"

    def test_10_timeline_label(self):
        """Timeline data - label"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="timeline"),
            params = {"label": "validfile", "mode": "label"},
            status = 200)

        # Data validation
        assert len(response.body.split("#")) == 35
        assert len(response.body.split(";")) == 19
        

    def test_11_timeline_url(self):
        """Timeline data - url"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="timeline"),
            params = {"label": "http://valid.host/",
                      "mode": "url"},
            status = 200)

        # Data validation
        assert len(response.body.split("#")) == 35
        assert len(response.body.split(";")) == 19

    def test_12_runinfo(self):
        """Runinfo"""

        # Fetch data from database
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        timestamp = collection.find_one({"label":"validfile"})["timestamp"]

        # Successful response
        response = self.app.get(
            url(controller="results", action="runinfo"),
            params = {"timestamp": timestamp},
            status = 200)

        # Data validation
        assert json.loads(response.body)

    def test_13_donwload(self):
        """Download HAR"""

        # Fetch data from database
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        id = collection.find_one({"label": "validfile"})["_id"]

        # Successful response
        response = self.app.get(
            url(controller="results", action="download"),
            params = {"id": id},
            status = 200)

        # Data validation
        har = response.body.replace("onInputData(","")[:-2]

        assert json.loads(har)

    def test_14_harviewer(self):
        """HAR Viewer iframe"""

        # Successful response
        response = self.app.get(
            url(controller="results", action="harviewer"),
            status = 200)

        # Cookie
        cookie = response.response.headers.get("Set-Cookie")

        assert "phaseInterval=-1;" in cookie
        assert "Max-Age=31536000;" in cookie
        assert "Path=/" in cookie

    def test_15_delete_label(self):
        """Delete - label"""

        # Fetch data from database
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        timestamp = collection.find_one({"label":"validfile"})["timestamp"]

        # Successful response
        response = self.app.get(
            url(controller="results", action="deleterun"),
            params = {"label": "validfile", "timestamp": timestamp,
                      "mode": "label", "all": "false"},
            status = 200)

        # Response validation
        assert response.body == "details?label=validfile"

    def test_16_delete_url(self):
        """Delete - url"""

        # Fetch data from database
        collection = pymongo.Connection("localhost:27017")["harstorage"]["results"]

        timestamp = collection.find_one({"url":"http://valid.host/"})["timestamp"]

        # Successful response
        response = self.app.get(
            url(controller="results", action="deleterun"),
            params = {"label": "http://valid.host/", "timestamp" : timestamp,
                      "mode": "url", "all": "false"},
            status = 200)

        # Response validation
        assert response.body == "/"