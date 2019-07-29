import os
import requests

from flask import Flask, jsonify, request
from utils import consts

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

    # get init
    init = FT.get_init()
    return f"{init}"

    # get status
    # status = FT.get_status()
    # return f"{status}"
