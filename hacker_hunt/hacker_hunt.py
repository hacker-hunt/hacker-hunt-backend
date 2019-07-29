import os
import requests

from flask import Flask, jsonify, request
from utils import consts
from mongo import Database
from settings import TOKEN, DB, DB_NAME


class FlaskTest():
    def get_init(self):
        res = requests.get(f"{consts['path']}{consts['init']}", headers={
                           'Authorization': f"Token {TOKEN}"})
        return res.json()

    def get_status(self):
        res = requests.post(f"{consts['path']}{consts['status']}", headers={
                            'Authorization': f"Token {TOKEN}"})
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
    # status = FT.get_status()
    # return f"{status}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
