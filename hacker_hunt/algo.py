import time

from utils import Stack, Queue
from player import get_status


# Update directions in map for both rooms
def update_map(current_room, next_room, db, db_id):
    current_room_id = str(list(current_room.keys())[0])
    current_room_dir = current_room[current_room_id]
    next_id = str(next_room["room_id"])
    # get map first
    game_map = db.get_map(db_id)
    obj = {"n": None, "s": None, "e": None, "w": None}
    # saves object of current room directions
    if current_room_id in game_map:
        current_map_directions = game_map[current_room_id]
    else:
        game_map[current_room_id] = obj.copy()
        current_map_directions = game_map[current_room_id]

    # update map
    # current room directions to next room
    if current_map_directions[current_room_dir] == None:
        current_map_directions[current_room_dir] = next_id
        # next room directions to current room
        if next_id in game_map:
            next_map_dir = game_map[next_id]
        else:
            game_map[next_id] = obj.copy()
            next_map_dir = game_map[next_id]

        oposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
        # if (0, 'n') = 1, then (1, 's') must be equal to 0
        next_map_dir[oposite_directions[current_room_dir]
                     ] = current_room_id
        # update map in db
        game_map[current_room_id] = current_map_directions
        game_map[next_id] = next_map_dir
        db.update_map(db_id, game_map)


# check for treasure and pick it up if you can
def treasure_check(room, player):
    print(f"Examining room for treasure and picking it up if I can")
    if len(room['items']) > 0:
        print('Waiting for CD before picking up items')
        time.sleep(room["cooldown"])
        for item in room['items']:
            # examine each treasure if you can pick it up
            examined_item = player.examine_item(item)
            print(f"Examined item: {examined_item}")
            # wait for cooldown before picking it up
            time.sleep(examined_item['cooldown'])

            # get the latest player status
            status = get_status()
            print(f"Player status: {status}")
            time.sleep(status['cooldown'])
            player.update_player(status)

            # see if player have enough capacity to pick it up
            player_capacity = player['strength'] - \
                player['encumbrance']

            if player_capacity > examined_item['weight']:
                # pick it up
                res = player.take_item(item)
                print(f'*** Picked up an item: {res} ***')
                # wait for cooldown before moving on
                time.sleep(res['cooldown'])
            else:
                print(
                    f"There was an item '{item}', which I could not pick up")
    else:
        print('Nothing to pick up here')


# check if room is a shop. save it in DB and sell items if yes
def shop_check(room, player, db, db_id):
    print(f"Player inventory: {player['inventory']}")
    if room['title'] == 'Shop':
        if len(player['inventory']) > 0:
            print('Waiting for CD before selling items')
            time.sleep(room["cooldown"])
            # sell treasures
            for item in player['inventory']:
                shop_res = player.sell_item(item)
                time.sleep(shop_res['cooldown'])
                print(f'*** Sold item: {shop_res} ***')

        # get shops from DB to check if its already saved
        shops = db.get_shops(db_id)
        if len(shops) > 0:
            for shop in shops:
                if room['room_id'] not in shop[0]:
                    db.update_shops(
                        db_id, [room['room_id'], room["coordinates"]])
        else:
            db.update_shops(
                db_id, [room['room_id'], room["coordinates"]])


# start and target are both instances of Room Class
# returns the path (list of room_id) from START to TARGET
def traverse(start, target, db):
    que = Queue()
    # enqueue first room
    que.enqueue({"node": start, "path": []})
    visited = set()
    print(f'Moving back from {start["room_id"]} to {target["room_id"]}')
    while que.size() > 0:
        current_room = que.queue[0]
        cr_id = current_room["node"]["room_id"]
        if cr_id not in visited:
            visited.add(cr_id)

            if cr_id == target["room_id"]:
                current_room["path"].append(cr_id)
                return current_room["path"]

            db_id = db.get_id()
            game_map = db.get_map(db_id)
            # add all neighbouring nodes to queue
            for direction in current_room["node"]["exits"]:
                # get ID of the room, that is in direction
                room_in_direction_id = game_map[str(cr_id)][direction]
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
    print(f'EXPLORING THE MAP')
    # first player initializes local stack and global que
    if len(db.get_que(db_id)) == 0:
        print('Initializing first movement')
        # make first request from room 0
        init_room = player.initalize()
        print(f'initial room: {init_room}')
        # save room in db
        db.insert_room(init_room)

        # add exit rooms from starting room to local stack and global que
        for direction in init_room["exits"]:
            s.push({str(init_room["room_id"]): direction})
            db.update_que(db_id, {str(init_room["room_id"]): direction})

        # cooldown management
        print('Going to sleep')
        time.sleep(init_room["cooldown"])
    # STOP conditon == empty local stack and global que
    while s.size() > 0 or len(db.get_que(db_id)):

        # first empty local stack
        if s.size() > 0:
            current_room = s.pop()
        else:
            # pop from global que
            que = db.get_que(db_id)
            current_room = que.pop(0)

        current_room_id = list(current_room.keys())[0]
        current_room_dir = current_room[current_room_id]
        print(
            f'### Currently in room {current_room_id} moving to {current_room_dir} ###')
        global_visited = db.get_visited(db_id)
        if current_room_id not in local_visited or current_room not in global_visited:
            local_visited.add(current_room_id)
            db.update_visited(db_id, current_room)

            # Make request for next movement
            global_map = db.get_map(db_id)

            if current_room_id not in global_map:
                global_map[current_room_id] = {
                    "n": None, "s": None, "e": None, "w": None}
            cur_room_dirs = global_map[current_room_id]
            # check whether the next dir exists on the db map
            if cur_room_dirs[current_room_dir] is not None:
                next_room = player.wise_explore(
                    current_room_dir, cur_room_dirs[current_room_dir])
            else:
                # otherwise just use move
                next_room = player.move(current_room_dir)

            print(f'Next room: {next_room}')
            # save next_room in DB
            db.insert_room(next_room)
            # check if next room is a shop and save it in DB if it is
            shop_check(next_room, player, db, db_id)

            # check for treasure
            treasure_check(next_room, player)

            # update map with newly discovered directions
            update_map(current_room, next_room, db, db_id)

            stack_before = s.size()

            # add exits from next_room to stack and que
            for direction in next_room["exits"]:
                # check if the direction is the return direction
                oposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
                if oposite_directions[direction] != current_room_dir:
                    n_dict = {str(next_room["room_id"]): direction}
                    global_visited = db.get_visited(db_id)
                    if next_room["room_id"] not in local_visited and n_dict not in global_visited:
                        s.push(n_dict)
                        db.update_que(db_id, n_dict)

            stack_after = s.size()

            # if we dont push any rooms to the stack, we hit dead end => start BFT
            if stack_before == stack_after:
                # cooldown management
                print('Going to sleep')
                time.sleep(next_room["cooldown"])

                # BFT will return shortest PATH to the next non-visited room
                shortest_path = []
                try:
                    # if current_room_id == s.stack[-1].id (you hit a dead end in looped nodes(cyclic graph))
                    # take s.stack[-2].id as TARGET if it exist
                    # if it doesnt (means the stack is empty) you are finished
                    if next_room["room_id"] == list(s.stack[-1].keys())[0]:
                        # BFS entry and target nodes:
                        # both have to be instances of Room class
                        # get rooms from DB by their ID
                        start = db.get_room_by_id(next_room["room_id"])
                        target = db.get_room_by_id(
                            list(s.stack[-2].keys())[0])

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

                except IndexError:
                    print('We are done!')
            else:
                # cooldown management
                print('Going to sleep\n')
                time.sleep(next_room["cooldown"])

        else:
            print(
                f"cr_id: {current_room_id} in {local_visited}\n{current_room} in {global_visited}")
