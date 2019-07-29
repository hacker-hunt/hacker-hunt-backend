import os

from pymongo import MongoClient

# connect to mongo client
client = MongoClient(f"{os.environ['DB']}")
# create DB
db = client['hacker_hunt']
# create collection 'visited'
visited = db.visited

def insert_to_db():
    # add item to DB
    v = {"visited": [], "global_que": [], "map": {}}
    visited_result = visited.insert_one(v)

    # get ID of item added to DB
    vis_id = visited_result.inserted_id

    print(f'Created new visited list, global queue and map: {vis_id}')
    return vis_id

def find_any():
    return visited.find_one()

def get_visited(id):
    # find item from DB
    query = {"_id": id}
    a = visited.find_one(query)
    return a['visited']

def update_visited(id, value):
    a = get_visited(id)
    # update item in DB
    b = a.copy()
    b.append(value)
    new_a = {"$set": {"visited": b}}
    visited.update_one({"_id": id}, new_a)

if not find_any():
    db_id = insert_to_db()
else:
    a = find_any()
    db_id = a["_id"]

print(f'db_id: {db_id}')