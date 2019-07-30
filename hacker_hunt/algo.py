import time

from utils import Stack, Queue
from room import Room


# Update directions in map for both rooms
def update_map(current_room, next_room, db, db_id):
    current_room_id = list(current_room.keys())[0]
    current_room_dir = current_room[current_room_id]
    # get map first
    game_map = db.get_map(db_id)
    obj = {"n": None, "s": None, "e": None, "w": None}
    # saves object of current room directions
    if current_room_id in game_map:
        current_map_directions = game_map[current_room_id]
    else:
        game_map[current_room_id] = obj
        current_map_directions = game_map[current_room_id]

    # update map
    # current room directions to next room
    if current_map_directions[current_room_dir] == None:
        current_map_directions[current_room_dir] = next_room["room_id"]
        # next room directions to current room
        if next_room["room_id"] in game_map:
            next_map_dir = game_map[next_room["room_id"]]
        else:
            game_map[next_room["room_id"]] = obj
            next_map_dir = game_map[next_room["room_id"]]

        oposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
        # if (0, 'n') = 1, then (1, 's') must be equal to 0
        next_map_dir[oposite_directions[current_map_directions]
                     ] = current_room_id
        # update map in db
        game_map[current_room_id] = current_map_directions
        game_map[next_room["room_id"]] = next_map_dir
        db.update_map(db_id, game_map)


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
            print(f'Currently in {cr_id}')
            if cr_id == target["room_id"]:
                current_room["path"].append(cr_id)
                return current_room["path"]

            db_id = db.get_id()
            game_map = db.get_map(db_id)
            # add all neighbouring nodes to queue
            for direction in current_room["node"].get_exits():
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
        print(f'Game server response: {init_room}\n')
        # save room in db
        db.insert_room(init_room)

        # add exit rooms from starting room to local stack and global que
        for direction in init_room["exits"]:
            s.push({str(init_room["room_id"]): direction})
            db.update_que(db_id, {str(init_room["room_id"]): direction})
        print(f"stack: {s.stack}")
        print(f"que: {db.get_que(db_id)}")

        # cooldown management
        print('Going to sleep')
        time.sleep(init_room["cooldown"])
        print('Woke up')
    # STOP conditon == empty local stack and global que
    while s.size() > 0 or len(db.get_que(db_id)):
        print(
            f'Running while loop. stack: {s.size()}, que: {len(db.get_que(db_id))}')
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
            f'Currently in room {current_room_id} moving to {current_room_dir}')
        global_visited = db.get_visited(db_id)
        if current_room_id not in local_visited and current_room not in global_visited:
            local_visited.add(current_room_id)
            db.update_visited(db_id, current_room)
            print(
                f"global_visited rooms : {db.get_visited(db_id)}\nlocal_visited: {local_visited}")
            # Make request for next movement
            # TODO optimize the request => IF you have the room ID in current_room_dir
            # use wise explorer to save cooldown
            # otherwise just use move
            next_room = player.move(current_room_dir)
            print(f'Game server response: {next_room}\n')
            print(f"next room is {next_room['room_id']}")
            # save next_room in DB
            db.insert_room(next_room)

            # check if next room is a shop and save it in DB if it is
            if next_room['title'] == 'Shop':
                # get shops from DB to check if its already saved
                shops = db.get_shops(db_id)
                if next_room['room_id'] not in shops:
                    db.update_shops(
                        db_id, [next_room['room_id'], next_room["coordinates"]])

            # check for treasure
            if len(next_room['items']) > 0:
                for item in next_room['items']:
                    # examine each treasure if you can pick it up
                    examined_item = player.examine_item(item)
                    # see if player have enough capacity to pick it up
                    player_capacity = player['strength'] - \
                        player['encumbrance']
                    if player_capacity > examined_item['weight']:
                        time.sleep(examined_item['cooldown'])
                        # pick it up
                        player.take_item(item)
                    else:
                        time.sleep(examined_item['cooldown'])

            # update map with newly discovered directions
            update_map(current_room, next_room, db, db_id)

            stack_before = s.size()

            next_room_instance = Room(next_room)
            # add exits from next_room to stack and que
            for direction in next_room_instance.get_exits():
                n_dict = {str(next_room["room_id"]): direction}
                global_visited = db.get_visited(db_id)
                if next_room["room_id"] not in local_visited and n_dict not in global_visited:
                    s.push(n_dict)
                    db.update_que(db_id, n_dict)
            print(f"stack: {s.stack}")
            print(f"que: {db.get_que(db_id)}")
            stack_after = s.size()

            # if we dont push any rooms to the stack, we hit dead end => start BFT
            if stack_before == stack_after:
                # BFT will return shortest PATH to the next non-visited room
                shortest_path = []
                try:
                    # if current_room_id == s.stack[-1].id (you hit a dead end in looped nodes(cyclic graph))
                    # take s.stack[-2].id as TARGET if it exist
                    # if it doesnt (means the stack is empty) you are finished
                    if current_room_id == list(s.stack[-1].keys())[0]:
                        # BFS entry and target nodes:
                        # both have to be instances of Room class

                        # get rooms from DB by their ID
                        start = db.get_room_by_id(current_room_id)
                        target = db.get_room_by_id(
                            list(s.stack[-2].keys())[0])

                        # TODO MAKE MOVE REQUESTS ACCORDING TO THE SHORTEST PATH LIST
                        shortest_path = traverse(
                            start, target, db)

                    else:
                        # BFS entry and target nodes:
                        # get room from DB by its ID
                        start = db.get_room_by_id(current_room_id)
                        target = db.get_room_by_id(
                            list(s.stack[-1].keys())[0])

                        # TODO MAKE MOVE REQUESTS ACCORDING TO THE SHORTEST PATH LIST
                        shortest_path = traverse(
                            start, target, db)

                    print(f"Path from traverse: {shortest_path}")

                except IndexError:
                    print('We are done!')

            # cooldown management
            print('Going to sleep')
            time.sleep(next_room["cooldown"])
            print('Woke up\n')
