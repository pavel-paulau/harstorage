import pymongo

from pylons import config, tmpl_context as c

class MongoDB():

    """
    Interface for MongoDB database
    """

    def __init__(self, collection="results"):
        """Initilize connection and check indeces"""

        try:
            # MongoDB URI
            uri = self.make_uri()

            # Database
            database = config["app_conf"]["mongo_db"]

            # Collection
            self.collection = pymongo.Connection(uri, safe=True)[database][collection]

            # Indecies
            self.ensure_index()
        except Exception as error:
            # Exception type: Exception message
            c.message = ": ".join([type(error).__name__, error.message])

    def make_uri(self):
        # Connection handler
        host = config["app_conf"]["mongo_host"]
        port = config["app_conf"]["mongo_port"]
        auth = config["app_conf"]["mongo_auth"]

        uri = "mongodb://"

        if auth == "true":
            user = config["app_conf"]["mongo_user"]
            pswd = config["app_conf"]["mongo_pswd"]
            uri += user + ":" + pswd + "@"

        return uri + host + ":" + port

    def ensure_index(self):
        self.collection.ensure_index([("label", 1), ("timestamp", -1)])
        self.collection.ensure_index([("label", 1), ("timestamp", 1)])
        self.collection.ensure_index([("url", 1), ("timestamp", -1)])
        self.collection.ensure_index([("url", 1), ("timestamp", 1)])