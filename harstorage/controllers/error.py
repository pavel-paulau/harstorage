from pylons import request, tmpl_context as c
from pylons import config
from webhelpers.html.builder import literal

from harstorage.lib.base import BaseController, render

class ErrorController(BaseController):

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    """

    def __before__(self):
        """Define version of static content"""

        c.rev = config["app_conf"]["static_version"]

    def document(self):
        """Render the error document"""

        resp = request.environ.get("pylons.original_response")
        c.message = literal(resp.status)

        return render("/error.html")