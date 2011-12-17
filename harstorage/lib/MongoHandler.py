import pymongo

class MongoDB():

    """
    Interface for MongoDB database
    """

    def __init__(self, host='localhost', port=27017):
        """Initilize connection and check indeces"""

        # Connection handler
        connection = pymongo.Connection(host, port)
        db = connection['harstorage']        
        self.collection = db['results']

        # Indeces
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