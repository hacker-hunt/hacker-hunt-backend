import os

from flask import Flask
from mongo import Database
from player import Player, get_status
from test_obj import test_obj
from settings import DB, DB_NAME, PROD_DB
from algo import explore


app = Flask(__name__)

p = Player(get_status())
db = Database(DB, DB_NAME)
db_id = db.get_id()
atlas_db = Database(PROD_DB, DB_NAME)
atlas_id = atlas_db.get_id()

# print(db_id, atlas_id)
# data_to_upload = db.download_data(db_id)
# print(data_to_upload)
# print(atlas_db.upload_data_to_atlas(data_to_upload))

# rooms_to_upload = list(db.download_rooms())
# print(rooms_to_upload)
# print(atlas_db.upload_rooms_to_atlas(rooms_to_upload))

# Manual commands test
# print(p.initalize())

# print(p.dash('w', '7', '327,256,243,178,90,86,80'))
# print(f"{p.move('w')}")

# print(p.sell_item())
# print(p.examine_item('great treasure'))
# print(p.examine_player('shiny treasure'))
# print(f"{p.take_item('small treasure')}")
# print(f"{p.drop_item('small treasure')}")

# print(db.get_room_by_id('0'))

# print(get_status())
# print(f"{p.wise_explore('e', 0)}")
explore(p, atlas_db, atlas_id)


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


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
