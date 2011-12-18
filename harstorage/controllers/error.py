from pylons import request, tmpl_context as c
from webhelpers.html.builder import literal

from harstorage.lib.base import BaseController, render

class ErrorController(BaseController):

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    """

    def document(self):
        """Render the error document"""

        resp = request.environ.get('pylons.original_response')
        c.message = literal(resp.status)

        return render('./error.html')