import pymongo

from pylons import config

class MongoDB():

    """
    Interface for MongoDB database
    """

    def __init__(self, database='harstorage', collection='results' ):
        """Initilize connection and check indeces"""

        # Connection handler
        host = config['app_conf']['mongo_host']
        port = int( config['app_conf']['mongo_port'] )

        connection = pymongo.Connection(host, port)
        db = connection[database]
        self.collection = db[collection]

        # Indecies
        self.collection.ensure_index([
            ('label',      1),
            ('timestamp', -1)
        ])

        self.collection.ensure_index([
            ('label',      1),
            ('timestamp',  1)
        ])

        self.collection.ensure_index([
            ('url',        1),
            ('timestamp', -1)
        ])

        self.collection.ensure_index([
            ('url',        1),
            ('timestamp',  1)
        ])