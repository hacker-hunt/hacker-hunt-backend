import os

from flask import Flask
from mongo import Database
from player import Player
from test_obj import test_obj
from settings import DB, DB_NAME


app = Flask(__name__)

p = Player(test_obj['test_player'], test_obj['test_room'])
db = Database(DB, DB_NAME)
db_id = db.get_id()


@app.route('/')
def server_check():
    return 'Server is running'


@app.route('/launch')
def launch_app():
    '''Initiates the application, the main logic loop goes inside here'''

    # get init
    init = p.initalize()
    print(f"Number of players: {len(init['players'])}")
    return f"{init}"


@app.route('/player')
def player_check():
    res = p.get_status()
    return f"{res}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
