import requests

from settings import TOKEN
from utils import consts


class Player:
    def __init__(self, p):
        '''Construct a new Player class'''
        self.name = p["name"]
        self.cooldown = p["cooldown"]
        self.encumbrance = p["encumbrance"]
        self.strength = p["strength"]
        self.speed = p["speed"]
        self.gold = p["gold"]
        self.inventory = p["inventory"]
        self.status = p["status"]
        self.errors = p["errors"]
        self.messages = p["messages"]

        # auth token for requests
        self.token = TOKEN
        self.auth = {"Authorization": f"Token {self.token}"}

    def initalize(self):
        '''Get all relevant stats before player starts moving.'''
        res = requests.get(
            f"{consts['path']}{consts['init']}",
            headers=self.auth
        )
        return res.json()

    def move(self, direction):
        '''Move the player in a provided direction.'''
        res = requests.post(
            f"{consts['path']}{consts['move']}",
            headers=self.auth,
            json={"direction": f"{direction}"}
        )
        return res.json()

    def wise_explore(self, direction, next_room_id):
        '''Move the player to a known room for 50% faster cooldown.'''
        res = requests.post(
            f"{consts['path']}{consts['move']}",
            headers=self.auth,
            json={"direction": f"{direction}",
                  "next_room_id": f"{next_room_id}"}
        )
        return res.json()

    def take_item(self, item_name="treasure"):
        '''Pick up an item found in a room.'''
        res = requests.post(
            f"{consts['path']}{consts['take']}",
            headers=self.auth,
            json={"name": f"{item_name}"}
        )
        return res.json()

    def drop_item(self, item_name="treasure"):
        '''Drop an item held in inventory.'''
        res = requests.post(
            f"{consts['path']}{consts['drop']}",
            headers=self.auth,
            json={"name": f"{item_name}"}
        )
        return res.json()

    def sell_item(self, item_name="treasure"):
        '''Sell an item held in inventory at a shop.'''
        res = requests.post(
            f"{consts['path']}{consts['sell']}",
            headers=self.auth,
            json={"name": f"{item_name}", 'confirm': 'yes'}
        )
        return res.json()

    def examine_item(self, item_name):
        '''Examine items in inventory'''
        res = requests.post(
            f"{consts['path']}{consts['examine']}",
            headers=self.auth,
            json={"name": f"{item_name}"}
        )
        return res.json()

    def examine_player(self, player_name):
        '''Examine player in the same room'''
        res = requests.post(
            f"{consts['path']}{consts['examine']}",
            headers=self.auth,
            json={"name": f"{player_name}"}
        )
        return res.json()

    def change_name(self, new_name):
        '''Change player name at a name changer room'''
        res = requests.post(
            f"{consts['path']}{consts['change_name']}",
            headers=self.auth,
            json={"name": f"{new_name}"}
        )
        return res.json()

    def pray(self):
        '''Pray at a shrine to earn powers'''
        res = requests.post(
            f"{consts['path']}{consts['pray']}",
            headers=self.auth
        )
        return res.json()

    def fly(self, direction):
        '''Use the flight power to move without penalty on elevated terrain'''
        res = requests.post(
            f"{consts['path']}{consts['fly']}",
            headers=self.auth,
            json={"direction": f"{direction}"}
        )
        return res.json()

    def dash(self, direction, num_of_rooms, next_rooms_string):
        '''Cover many rooms in one direction quickly'''
        # next_room_ids = ",".join([str(item) for item in next_rooms_list])
        res = requests.post(
            f"{consts['path']}{consts['dash']}",
            headers=self.auth,
            json={"direction": str(direction), "num_rooms": str(
                num_of_rooms), "next_room_ids": next_rooms_string}
        )
        return res.json()

    def update_player(self, p):
        self.name = p["name"]
        self.cooldown = p["cooldown"]
        self.encumbrance = p["encumbrance"]
        self.strength = p["strength"]
        self.speed = p["speed"]
        self.gold = p["gold"]
        self.inventory = p["inventory"]
        self.status = p["status"]
        self.errors = p["errors"]
        self.messages = p["messages"]


# Use this function to initialize an instance of player
def get_status():
    '''Get basic player status and inventory.'''
    res = requests.post(
        f"{consts['path']}{consts['status']}",
        headers={"Authorization": f"Token {TOKEN}"}
    )
    return res.json()


"""
EXAMINE ITEM RESPONSE

{
    'name': 'tiny treasure',
    'description': 'This is a tiny piece of treasure',
    'weight': 1,
    'itemtype': 'TREASURE',
    'level': 1,
    'exp': 0,
    'attributes': '{}',
    'cooldown': 15.0,
    'errors': [],
    'messages': []
}
"""
