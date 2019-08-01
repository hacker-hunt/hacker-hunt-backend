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
        # create colelction 'stacks' that contains copies of local stack for each player
        self.stacks = self.db.stacks

    def insert_to_db(self):
        # add item to DB
        v = {"visited": [], "global_que": [], "map": {}, "shops": []}
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

    def insert_room(self, room):
        # add room to DB
        room_result = self.rooms.insert_one(room)

        # get ID of item added to DB
        room_id = room_result.inserted_id

        # print(f'Created new room: {room["room_id"]} in DB')
        return room_id

    def get_room_by_id(self, id):
        # check online how to filter query based on object property {"room_id": id}
        query = {"room_id": int(id)}
        room_dict = self.rooms.find_one(query)
        return room_dict

    def get_shops(self, id):
        # find item from DB
        query = {"_id": id}
        a = self.data.find_one(query)
        return a['shops']

    def update_shops(self, id, shop):
        a = self.get_shops(id)
        # update item in DB
        b = a.copy()
        b.append(shop)
        new_a = {"$set": {"shops": b}}
        self.data.update_one({"_id": id}, new_a)

    def download_data(self, id):
        query = {"_id": id}
        data = self.data.find_one(query)
        data["visited"] = []
        data["global_que"] = []
        return data

    def download_rooms(self):
        data = self.rooms.find({})
        return data

    def upload_data_to_atlas(self, data):
        data_result = self.data.insert_one(data)

        # get ID of item added to DB
        item_id = data_result.inserted_id

        print(f'Created new visited list, global queue and map: {item_id}')
        return item_id

    def upload_rooms_to_atlas(self, rooms):
        data_result = self.rooms.insert_many(rooms)
        return data_result

    def first_stack_insert(self, player, stack):
        obj = {"player_name": player["name"], "stack": stack}
        # add stack to DB
        stack_result = self.stacks.insert_one(obj)

        # get ID of item added to DB
        stack_id = stack_result.inserted_id

        # print(f'Created new stack: {stack["stack_id"]} in DB')
        return stack_id

    def update_stack(self, player, stack):
        query = {"player_name": player["name"]}
        stack_data = self.stacks.find_one(query)
        if not stack_data:
            self.first_stack_insert(player, stack)
        else:
            new_stack = {"$set": {"stack": stack}}
            self.stacks.update_one({"player_name": player["name"]}, new_stack)

    def get_stack(self, player):
        query = {"player_name": player["name"]}
        stack_data = self.stacks.find_one(query)
        return stack_data

    def clean_visited(self, id):
        # find item from DB
        query = {"_id": id}
        cleaned_data = {"$set": {"visited": []}}
        self.data.update_one(query, cleaned_data)
