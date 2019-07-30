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

# Manual commands test
# print(p.initalize())

# print(p.dash('w', '7', '327,256,243,178,90,86,80'))
# print(f"{p.move('e')}")
# print(f"{p.wise_explore('e', 0)}")
# print(get_status())
# print(p.sell_item())
# print(p.examine_item('tiny treasure'))
# print(p.examine_player('player59'))

# print(f"{p.take_item()}")
# print(get_status())


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
