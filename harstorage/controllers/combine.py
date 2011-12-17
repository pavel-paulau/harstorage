import logging

from pylons import request, response
from pylons import config

from harstorage.lib.base import BaseController

log = logging.getLogger(__name__)

class CombineController(BaseController):

    """
    Combine multiple static text resources (CSS, JavaScript)
    into single file

    """

    def styles(self):
        """Read list of stylesheets and combine them"""

        # Concatenation
        for key in request.GET.keys():
            if key != 'ver':
                base = config['pylons.paths']['static_files']
                file = open(base + "/styles/" + key)
                try:
                    combo += file.read()
                except:
                    combo  = file.read()
                file.close()

        # Additional HTTP headers
        response.headerlist = [
            ('Content-type', 'text/css'),
            ('Last-Modified', 'Fri, 16 Dec 2011 12:00:00 GMT')
        ]

        return combo