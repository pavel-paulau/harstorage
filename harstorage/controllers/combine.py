from pylons import request, response
from pylons import config
from pylons.decorators.rest import restrict

from harstorage.lib.base import BaseController

class CombineController(BaseController):

    """
    Combine multiple static text resources (CSS, JavaScript)
    into single file

    """

    @restrict("GET")
    def styles(self):
        """Read list of stylesheets and combine them"""

        # Concatenation
        for key in request.GET.keys():
            if key != "ver":
                base = config["pylons.paths"]["static_files"]
                try:
                    with open(base + "/styles/" + key) as file:
                        try:
                            combo += file.read()
                        except UnboundLocalError:
                            combo = file.read()
                except IOError:
                    response.status_int = 404
                    return None

        # Additional HTTP headers
        response.headerlist = [("Content-type", "text/css")]

        return combo

    @restrict("GET")
    def scripts(self):
        """Read list of JavaScript files and combine them"""

        # Concatenation
        for key in request.GET.keys():
            if key != "ver":
                base = config["pylons.paths"]["static_files"]
                try:
                    with open(base + "/scripts/" + key) as file:
                        try:
                            combo += file.read()
                        except UnboundLocalError:
                            combo = file.read()
                except IOError:
                    response.status_int = 404
                    return None

        # Additional HTTP headers
        response.headerlist = [("Content-type", "application/javascript")]

        return combo