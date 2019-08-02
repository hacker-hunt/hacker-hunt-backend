import time
import sys

from utils import Stack, Queue
from player import get_status


# Update directions in map for both rooms
def update_map(current_room, next_room, db, db_id):
    current_room_id = str(list(current_room.keys())[0])
    current_room_dir = current_room[current_room_id]
    next_id = str(next_room["room_id"])
    # get map first
    game_map = db.get_map(db_id)

    # saves object of current room directions
    if current_room_id not in game_map:
        game_map[current_room_id] = {}

    current_map_directions = game_map[current_room_id]

    # update map
    # current room directions to next room

    current_map_directions[current_room_dir] = next_id

    # next room directions to current room
    if next_id not in game_map:
        game_map[next_id] = {}

    next_map_dir = game_map[next_id]

    oposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
    # if (0, 'n') = 1, then (1, 's') must be equal to 0
    next_map_dir[oposite_directions[current_room_dir]] = current_room_id
    # update map in db
    game_map[current_room_id] = current_map_directions
    game_map[next_id] = next_map_dir
    db.update_map(db_id, game_map)


# traverse shortest path
def traverse_path(shortest_path, player, db, db_id):
    for idx, room_id in enumerate(shortest_path):
        # initialize destination variable
        destination_id = ""
        # get instance of room class
        global_map = db.get_map(db_id)
        origin = global_map[str(room_id)]

        # check to see if it's the last room in the list
        if idx < (len(shortest_path) - 1):
            # get next room in list
            destination_id = shortest_path[idx+1]
            # find dir to destination
            for direction, room_id in origin.items():
                if room_id and int(room_id) == destination_id:
                    next_direction = direction

            # make wise explore request
            destination_room = player.wise_explore(
                next_direction, destination_id)
            print(f'destination room: {destination_room}')
            # do cooldown in between each loop
            time.sleep(destination_room["cooldown"])


# traverse from current player room to target room
def traverse_player_to_target(player, target_id, db, db_id):
    if target_id != None:
        start_room = player.initalize()
        time.sleep(start_room['cooldown'])
        target_room = db.get_room_by_id(int(target_id))
        path = traverse(start_room, target_room, db)
        traverse_path(path, player, db, db_id)


# check for treasure and pick it up if you can
def treasure_check(room, player, db, db_id):
    print(f"Examining room for treasure and picking it up if I can")
    if len(room['items']) > 0:
        # get the latest player status
        status = get_status()
        print(f"Player status: {status}")
        time.sleep(status['cooldown'])
        player.update_player(status)

        # see if player have enough capacity to pick it up
        player_capacity = player['strength'] - \
            player['encumbrance']

        if player_capacity > 1:
            for item in room['items']:

                if item != 'tiny treasure' and item != 'small treasure':
                    # examine each treasure if you can pick it up
                    examined_item = player.examine_item(item)
                    print(f"Examined item: {examined_item}")
                    # wait for cooldown before picking it up
                    time.sleep(examined_item['cooldown'])

                    if player_capacity > examined_item['weight']:
                        # pick it up
                        res = player.take_item(item)
                        print(f'*** Picked up an item: {res} ***')
                        # wait for cooldown before moving on
                        time.sleep(res['cooldown'])

                        # get the latest player status
                        status = get_status()
                        print(f"Player status: {status}")
                        time.sleep(status['cooldown'])
                        player.update_player(status)

                        # see if player have enough capacity to pick it up
                        player_capacity = player['strength'] - \
                            player['encumbrance']
                    else:
                        print(
                            f"There was an item '{item}', which I could not pick up")

        # if the player is carrying over 80% of his strength, go to Shop
        if player['encumbrance'] >= 0.8*player['strength']:
            # traverse there
            shortest_path = find_nearest_shop(room, db, db_id)
            traverse_path(shortest_path, player, db, db_id)
            # get shop room
            shop_room = db.get_room_by_id(1)
            # sell items
            shop_check(shop_room, player, db, db_id)
            # get path back => reversed shortest_path
            shortest_path.reverse()
            # traverse back to current room
            traverse_path(shortest_path, player, db, db_id)

    else:
        print('Nothing to pick up here')


# check if room is a shop. save it in DB and sell items if yes
def shop_check(room, player, db, db_id):
    if room['title'] == 'Shop':
        print(f"Checking shop. Player inventory: {player['inventory']}")
        if len(player['inventory']) > 0:
            # sell treasures
            for item in player['inventory']:
                shop_res = player.sell_item(item)
                time.sleep(shop_res['cooldown'])
                print(f"*** Sold item: {shop_res['messages']} ***")


# find nearest shop
# run traverse for every current_room - shop pair
# and return the shortest
def find_nearest_shop(room, db, db_id):
    shop_room = db.get_room_by_id(1)
    path = traverse(room, shop_room, db)
    return path


# start and target are both instances of rooms
# returns the path (list of room_id) from START to TARGET
def traverse(start, target, db):
    que = Queue()
    # enqueue first room
    que.enqueue({"node": start, "path": []})
    visited = set()
    print(f'Traversing back from {start["room_id"]} to {target["room_id"]}')

    while que.size() > 0:
        current_room = que.queue[0]
        cr_id = current_room["node"]["room_id"]
        if cr_id not in visited:
            visited.add(cr_id)

            if cr_id == target["room_id"]:
                current_room["path"].append(cr_id)
                print(f"Returning on this path: {current_room['path']}")
                return current_room["path"]

            db_id = db.get_id()
            game_map = db.get_map(db_id)
            # add all neighbouring nodes to queue
            for direction in current_room["node"]["exits"]:
                # get ID of the room, that is in direction
                room_in_direction_id = game_map[str(cr_id)][direction]
                if room_in_direction_id != None:
                    # grab that room from DB
                    room = db.get_room_by_id(room_in_direction_id)

                    # Make a COPY of the PATH set from current node to neighbour nodes
                    path_to_neighbour = current_room["path"].copy()
                    path_to_neighbour.append(cr_id)

                    que.enqueue(
                        {"node": room, "path": path_to_neighbour})

        que.dequeue()
    return None


# explore the map and save it in DB
def explore(player, db, db_id):
    s = Stack()
    local_visited = set()
    visited_ids = set()
    print(f'EXPLORING THE MAP')

    init_room = player.initalize()
    print(f'Initial room: {init_room}')
    time.sleep(init_room["cooldown"])
    # save room in db
    db.insert_room(init_room)

    for direction in init_room["exits"]:
        s.push({str(init_room["room_id"]): direction})

    db.update_stack(player, s.get_stack())

    # STOP conditon == empty local stack and global que
    while s.size() > 0:
        current_room = s.pop()
        current_room_id = list(current_room.keys())[0]
        current_room_dir = current_room[current_room_id]

        visited_ids.add(current_room_id)
        print(f"Visited {len(visited_ids)} rooms")
        print(
            f'### Currently in room {current_room_id} moving to {current_room_dir} ###')
        if str(current_room) not in local_visited:
            local_visited.add(str(current_room))

            # Make request for next movement
            global_map = db.get_map(db_id)

            if current_room_id not in global_map:
                global_map[current_room_id] = {}
            cur_room_dirs = global_map[current_room_id]

            # check whether the next dir exists on the db map
            if current_room_dir in cur_room_dirs:
                next_room = player.wise_explore(
                    current_room_dir, cur_room_dirs[current_room_dir])
            else:
                # otherwise just use move
                next_room = player.move(current_room_dir)

            print(f'Next room: {next_room}')
            # save next_room in DB
            db.insert_room(next_room)
            print('Going to sleep')
            time.sleep(next_room["cooldown"])
            # update map with newly discovered directions
            update_map(current_room, next_room, db, db_id)

            # check if next room is a shop and save it in DB if it is
            shop_check(next_room, player, db, db_id)

            # check for treasure
            treasure_check(next_room, player, db, db_id)

            # change name room
            if next_room["room_id"] == 467:
                print(f"Found Pirate Ry's name changer")
                names = {"player55": "pavol", "player52": "diana", "player54": "markm", "player53": "talent antonio"}

                if player["name"] in names:
                    res = player.change_name(names[player["name"]])
                    print(f"Changed name: {res}")
                    time.sleep(res["cooldown"])

            # shrine room
            if next_room["room_id"] == 22:
                print("Found Shrine!")
                i_pray = player.pray()
                print(f"You prayed at the shrine: {i_pray}")
                time.sleep(i_pray["cooldown"])

            stack_before = s.size()

            # add exits from next_room to stack and que
            for direction in next_room["exits"]:
                # check if the direction is the return direction
                oposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
                if oposite_directions[direction] != current_room_dir:
                    n_dict = {str(next_room["room_id"]): direction}

                    if str(n_dict) not in local_visited:
                        s.push(n_dict)

            # update stack on db
            db.update_stack(player, s.get_stack())

            stack_after = s.size()

            # if we dont push any rooms to the stack, we hit dead end => start BFT
            if stack_before == stack_after:

                # BFT will return shortest PATH to the next non-visited room
                shortest_path = []
                try:
                    # if current_room_id == s.stack[-1].id (you hit a dead end in looped nodes(cyclic graph))
                    # take s.stack[-2].id as TARGET if it exist
                    # if it doesnt (means the stack is empty) you are finished
                    if next_room["room_id"] == list(s.stack[-1].keys())[0]:
                        # BFS entry and target nodes:
                        # both have to be instances of room objects
                        # get rooms from DB by their ID
                        start = db.get_room_by_id(next_room["room_id"])
                        target = db.get_room_by_id(
                            list(s.stack[-2].keys())[0])
                        print(f'>>>> HIT A LOOPED NODE <<<<')
                        shortest_path = traverse(
                            start, target, db)

                    else:
                        # BFS entry and target nodes:
                        # get room from DB by its ID
                        start = db.get_room_by_id(next_room["room_id"])
                        target = db.get_room_by_id(
                            list(s.stack[-1].keys())[0])

                        shortest_path = traverse(
                            start, target, db)

                    traverse_path(shortest_path, player, db, db_id)

                except IndexError:
                    print('We are done!')

        else:
            print(
                f"{current_room} already visited")
