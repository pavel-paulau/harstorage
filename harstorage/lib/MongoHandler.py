import pymongo

class MongoDB():
    def __init__(self,host='localhost',port=27017):
        connection = pymongo.Connection(host, port)
        db = connection['harstorage']        
        self.collection = db['results']
        
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