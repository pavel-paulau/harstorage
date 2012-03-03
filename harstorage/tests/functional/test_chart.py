from harstorage.tests import *

class TestChartController(TestController):

    """
    Test suite for chart export

    """

    def test_01_export_svg(self):
        """Export SVG"""

        # Expected valid image
        with open("harstorage/tests/functional/testdata/validfile.svg") as file:
            response = self.app.post(
                url(controller="chart", action="export"),
                params = {"svg": file.read(), "type": "image/svg+xml",
                          "filename": "timeline", "width": 960},
                status = 200)

        # Response header
        assert response.content_type == "image/svg+xml"

    def test_02_export_png(self):
        """Export PNG"""

        # Expected valid image
        with open("harstorage/tests/functional/testdata/validfile.svg") as file:
            response = self.app.post(
                url(controller="chart", action="export"),
                params = {"svg": file.read(), "type": "image/png",
                          "filename": "timeline", "width": 960},
                status = 200)

        # Response header
        assert response.content_type == "image/png"