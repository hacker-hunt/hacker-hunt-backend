from pymongo import MongoClient


class Database:
    def __init__(self, url, db_name):
        # connect to mongo client
        self.client = MongoClient(url)
        # create DB
        self.db = self.client[db_name]
        # create collection 'data' that contains 'visited' list, 'global_que' list and 'map' dict
        self.data = self.db.data
        # create colelction 'rooms' that contains instances of Room class
        self.rooms = self.db.rooms

    def insert_to_db(self):
        # add item to DB
        v = {"visited": [], "global_que": [], "map": {}}
        data_result = self.data.insert_one(v)

        # get ID of item added to DB
        vis_id = data_result.inserted_id

        print(f'Created new visited list, global queue and map: {vis_id}')
        return vis_id

    def find_any(self):
        return self.data.find_one()

    def get_visited(self, id):
        # find item from DB
        query = {"_id": id}
        a = self.data.find_one(query)
        return a['visited']

    def update_visited(self, id, value):
        a = self.get_visited(id)
        # update item in DB
        b = a.copy()
        b.append(value)
        new_a = {"$set": {"visited": b}}
        self.data.update_one({"_id": id}, new_a)

    def get_que(self, id):
        # find item from DB
        query = {"_id": id}
        a = self.data.find_one(query)
        return a['global_que']

    def update_que(self, id, value):
        a = self.get_que(id)
        # update item in DB
        b = a.copy()
        b.append(value)
        new_a = {"$set": {"global_que": b}}
        self.data.update_one({"_id": id}, new_a)

    def get_map(self, id):
        # find item from DB
        query = {"_id": id}
        a = self.data.find_one(query)
        return a['map']

    def update_map(self, id, value):
        a = self.get_map(id)
        # update item in DB
        b = a.copy()
        b.update(value)
        new_a = {"$set": {"map": b}}
        self.data.update_one({"_id": id}, new_a)

    def get_id(self):
        if not self.find_any():
            db_id = self.insert_to_db()
        else:
            a = self.find_any()
            db_id = a["_id"]
        return db_id
