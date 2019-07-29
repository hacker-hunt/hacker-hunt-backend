import os
import requests

from flask import Flask, jsonify, request
from utils import consts
from mongo import Database
from settings import TOKEN, DB, DB_NAME


class ServerRequests():
    '''Construct a new SR class'''
    def __init__(self):
        self.token = os.environ['TOKEN']
        self.authorization = {"Authorization": f"{self.token}"}
        

    def initalize(self):
        '''Get all relevant stats before player starts moving.'''
        res = requests.get(
            f"{consts['path']}{consts['init']}", 
            headers=self.authorization
        )
        return res.json()
    
    def move(self, direction):
        '''Move the player in a provided direction.'''
        res = requests.post(
            f"{consts['path']}{consts['move']}", 
            headers=self.authorization,
            json={"direction": f"{direction}"}
        )
        return res.json()
    
    def wise_explorer(self, direction, next_room_id):
        '''Move the player to a known room for 50% faster cooldown.'''
        res = requests.post(
            f"{consts['path']}{consts['move']}", 
            headers=self.authorization,
            json={"direction": f"{direction}", "next_room_id": f"{next_room_id}"}
        )
        return res.json()
    
    def take_item(self, item_name="treasure"):
        '''Pick up an item found in a room.'''
        res = requests.post(
            f"{consts['path']}{consts['take']}", 
            headers=self.authorization,
            json={"name": f"{item_name}"}
        )
        return res.json()
    
    def drop_item(self, item_name="treasure"):
        '''Drop an item held in inventory.'''
        res = requests.post(
            f"{consts['path']}{consts['drop']}", 
            headers=self.authorization,
            json={"name": f"{item_name}"}
        )
        return res.json()
    
    def sell_item(self, item_name="treasure"):
        '''Sell an item held in inventory at a shop.'''
        res = requests.post(
            f"{consts['path']}{consts['sell']}", 
            headers=self.authorization,
            json={"name": f"{item_name}", 'confirm': 'yes'}
        )
        return res.json()

    def examine_item(self, item_name):
        '''Examine items in inventory'''
        res = requests.post(
            f"{consts['path']}{consts['examine']}", 
            headers=self.authorization,
            json={"name": f"{item_name}"}
        )

    def examine_player(self, player_name):
        '''Examine player in the same room'''
        res = requests.post(
            f"{consts['path']}{consts['examine']}", 
            headers=self.authorization,
            json={"name": f"{player_name}"}
        )
    
    def status(self):
        '''Check status and inventory.'''
        res = requests.post(
            f"{consts['path']}{consts['status']}", 
            headers=self.authorization
        )
        return res.json()
    
    def change_name(self, new_name):
        '''Change player name at a name changer room'''
        res = requests.post(
            f"{consts['path']}{consts['change_name']}", 
            headers=self.authorization,
            json={"name": f"{new_name}"}
        )
    
    def pray_at_shrine(self):
        '''Pray at a shrine to earn powers'''
        res = requests.post(
            f"{consts['path']}{consts['pray']}", 
            headers=self.authorization
        )
    
    def fly(self, direction):
        '''Use the flight power to move without penalty on elevated terrain'''
        res = requests.post(
            f"{consts['path']}{consts['fly']}", 
            headers=self.authorization,
            json={"direction": f"{direction}"}
        )
        return res.json()
    
    def dash(self, next_rooms_list):
        '''Cover many rooms in one direction quickly'''
        next_room_ids = ",".join([str(item) for item in next_rooms_list])
        res = requests.post(
            f"{consts['path']}{consts['fly']}", 
            headers=self.authorization,
            json={"direction": f"{next_room_ids}"}
        )
        return res.json()
    

app = Flask(__name__)


@app.route('/')
def server_check():
    return 'Server is running'


@app.route('/launch')
def launch_app():
    '''Initiates the application, the main logic loop goes inside here'''
    FT = FlaskTest()
    db = Database(os.environ['DB'], os.environ['DB_NAME'])
    db_id = db.get_id()

    # get init
    init = FT.get_init()
    print(f"Number of players: {len(init['players'])}")
    # test db connection
    db.update_visited(db_id, init["room_id"])

    return f"{init}"

    # get status
    # status = FT.status()
    # return f"{status}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
