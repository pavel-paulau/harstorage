"""Helper functions"""

from routes import url_for
from webhelpers.html.tags import *

def decode_uri(URI):
    """Decode JavaScript encodeURIComponent"""

    return URI.replace("&amp;", "&")