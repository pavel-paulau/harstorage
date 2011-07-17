from pymongo import objectid, Connection

class MongoHandler():
    def __init__(self,host='localhost',port=27017):
        connection = Connection(host, port)
        db = connection['har-storage']        
        self.collection = db['har-files']
    
    def store_to_mongo(self,har):
        return self.collection.insert({"har":har})

    def read_from_mongo(self,id):
        return self.collection.find_one(objectid.ObjectId(id))['har']
