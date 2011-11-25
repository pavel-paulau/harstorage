import logging

from pylons import request, response
from harstorage.lib.base import BaseController

log = logging.getLogger(__name__)

class CombineController(BaseController):
    def styles(self):
        # Read list of stylesheets and combine them
        combo = ''

        for key, value in request.GET.items():
            if key != 'ver':
                file = open("harstorage/public/styles/" + key)
                combo = combo + file.read()
                file.close()

        # Custom HTTP Headers
        response.headerlist = [('Content-type', 'text/css'),('Last-Modified', 'Tue, 22 Nov 2011 12:00:00 GMT')]

        return combo