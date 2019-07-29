import os
import requests

from flask import Flask, jsonify, request
from utils import consts
from mongo import find_any, update_visited

class FlaskTest():
    def get_init(self):
        res = requests.get(f"{consts['path']}{consts['init']}", headers={'Authorization': f"Token {os.environ['TOKEN']}"})
        return res.json()
    
    def get_status(self):
        res = requests.post(f"{consts['path']}{consts['status']}", headers={'Authorization': f"Token {os.environ['TOKEN']}"})
        return res.json()

app = Flask(__name__)

@app.route('/launch')
def launch_app():
    '''Initiates the application, the main logic loop goes inside here'''
    FT = FlaskTest()

    if not find_any():
        db_id = insert_to_db()
    else:
        a = find_any()
        db_id = a["_id"]

    # get init
    init = FT.get_init()
    update_visited(db_id, init["room_id"])
    return f"{init}"

    # get status
    # status = FT.get_status()
    # return f"{status}"
