import pymongo

from pylons import config

class MongoDB():

    """
    Interface for MongoDB database
    """

    def __init__(self, collection="results"):
        """Initilize connection and check indeces"""

        # Connection handler
        host = config["app_conf"]["mongo_host"]
        port = config["app_conf"]["mongo_port"]
        auth = config["app_conf"]["mongo_auth"]

        uri = "mongodb://"

        if auth == "true":
            user = config["app_conf"]["mongo_user"]
            pswd = config["app_conf"]["mongo_pswd"]
            uri += user + ":" + pswd + "@"

        uri += host + ":" + port

        database = config["app_conf"]["mongo_db"]

        self.collection = pymongo.Connection(uri, safe=True)[database][collection]

        # Indecies
        self.collection.ensure_index([("label", 1), ("timestamp", -1)])

        self.collection.ensure_index([("label", 1), ("timestamp", 1)])

        self.collection.ensure_index([("url", 1), ("timestamp", -1)])

        self.collection.ensure_index([("url", 1), ("timestamp", 1)])