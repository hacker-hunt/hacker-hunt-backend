import os

from flask import Flask
from mongo import Database
from player import Player, get_status
from test_obj import test_obj
from settings import DB, DB_NAME
from algo import explore


app = Flask(__name__)

p = Player(get_status())
db = Database(DB, DB_NAME)
db_id = db.get_id()


@app.route('/')
def server_check():
    return 'Server is running'


@app.route('/launch')
def launch_app():
    '''Initiates the application, the main logic loop goes inside here'''

    # initialize the algorith
    explore(p, db, db_id)

    final_map = db.get_map(db_id)
    return f"{final_map}"


@app.route('/player')
def player_check():
    res = get_status()
    return f"{res}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
