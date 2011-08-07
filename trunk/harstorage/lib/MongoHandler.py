from pymongo import objectid, Connection

class MongoDB():
    def __init__(self,host='localhost',port=27017):
        connection = Connection(host, port)
        db = connection['harstorage']        
        self.collection = db['results']