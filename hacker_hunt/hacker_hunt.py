import os

from flask import Flask, Response, request
from flask_cors import CORS
from threading import Thread
from mongo import Database
from player import Player, get_status
from settings import DB, DB_NAME, PROD_DB
from algo import explore, traverse_player_to_target


app = Flask(__name__)
CORS(app)

p = Player(get_status())
db = Database(DB, DB_NAME)
db_id = db.get_id()
atlas_db = Database(PROD_DB, DB_NAME)
atlas_id = atlas_db.get_id()


# MANUAL COMMANDS. ONLY RUN ONE AT A TIME
# print(p.dash('w', '7', '327,256,243,178,90,86,80'))
# print(f"{p.move('w')}")
# print(f"{p.wise_explore('s', 22)}")

# print(p.sell_item('nice jacket'))
# print(p.examine_item('amazing treasure'))
# print(p.examine_player('shiny treasure'))
# print(f"{p.take_item('shiny treasure')}")
# print(f"{p.drop_item('small treasure')}")
# print(p.pray())
# print(p.fly('s'))
# print(p.change_name(f'🔥🔥🔥 pavol🔥🔥🔥'))

# print(p.initalize())
# print(get_status())
# explore(p, atlas_db, atlas_id)
# traverse_player_to_target(p, 495, atlas_db, atlas_id)

# print(p.transmogrify('nice boots'))
# print(p.equip_item('nice boots'))
# print(p.get_coin_balance())


def get_uncovered_rooms():
    rooms_uncovered = []
    rooms_covered = atlas_db.rooms.distinct("room_id")
    for i in range(499):
        if i not in rooms_covered:
            rooms_uncovered.append(i)
    print(f"Uncovered: {rooms_uncovered}")
    print(f"Num_uncovered: {len(rooms_uncovered)}")


# get_uncovered_rooms()


def start_exploring():
    explore(p, atlas_db, atlas_id)


def requested_to_run():
    print('STARTING TO EXPLORE')
    t = Thread(target=start_exploring)
    t.start()
    return "Exploring"


@app.route('/')
def server_check():
    return 'Server is running'


@app.route('/launch', methods=['POST'])
def launch_app():
    '''Initiates the application, the main logic loop goes inside here'''
    return Response(requested_to_run(), mimetype="text/html")


@app.route('/player', methods=['GET'])
def player_check():
    res = get_status()
    return f"{res}"


@app.route('/stop', methods=['GET', 'POST'])
def stop_explorer():
    return "You simply can not stop exploring"


@app.route('/traverse', methods=['POST'])
def traverse_it():
    values = request.get_json()

    if "target_id" not in values:
        return "Missing target_id in request body"
    else:
        target_id = values["target_id"]
        if not isinstance(target_id, int) and not isinstance(target_id, str):
            return "target_id is not a str or int"
        else:
            traverse_player_to_target(p, target_id, atlas_db, atlas_id)
    return f'{values}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
