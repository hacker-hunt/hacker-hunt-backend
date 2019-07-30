import time

from utils import Stack, Queue
from player import get_status
from random import randint

def hunt(player, final_map, db_id):
    # init the player, get first room and gold as global vars
    cur_room = player.initalize()
    time.sleep(cur_room["cooldown"])
    #start the while loop
    hunting()

    def cooldown():
        time.sleep(cur_room["cooldown"])

    # find random exit to travel in
    def find_hunt_dir(cur_room):
        cur_room_exits = cur_room["exits"]
        rand_exit = cur_room_exits[randint(0,len(cur_room_exits) - 1)]
        return rand_exit

    def coord_diff(cur_room_coords, shop_coords):
        coord_re = r"\d+"
        cur_room_coords_match = re.findall(coord_re, cords_a)
        shop_coords_match = re.findall(coord_re, coords_b)
        # calculate x difference
        if cur_room_coords_match[0] > shop_coords_match[0]:
            x_dif = cur_room_coords_match[0] - shop_coords_match[0]
        else:
            x_dif = shop_coords_match[0] - cur_room_coords_match[0]
        # calculate y difference
        if cur_room_coords_match[1] > shop_coords_match[1]:
            y_dif = cur_room_coords_match[1] - shop_coords_match[1]
        else:
            y_dif = shop_coords_match[1] - cur_room_coords_match[1]
        # calculate and return distance proxy
        distance_to_shop = x_dif + y_dif
        return distance_to_shop
    
    def shop_traverse():
        pass
    
    def sell_at_shop(treasure):
        player.sell_item(treasure["name"])
        cooldown()

    def go_to_shop(treasure):
        # get list of shops
        shops = db.get_shops(db_id)
        # calculate nearest shop
        cur_room_coords = cur_room["coordinates"]
        shop_coords = shop[1]
        for idx, shop in enumerate(shops):
            dist_to_shop = coord_diff(cur_room_coords, shop_coords)
            if idx = 0:
                # save as a tuple of room_id and distance
                cur_closest = (shop[0], dist_to_shop)
            elif dist_to_shop < cur_closest[1]:
                cur_closest = (shop[0], dist_to_shop)
        closest_shop_id = cur_closest[0]
        # TODO: implement BFT to nearest shop
        # shop_traverse(cur_room, shop)
        # sell at shop
        sell_at_shop(treasure)

    # check for treasure, pick up able
    def handle_treasure():
        # examine the treasure
        treasure = player.examine_item(f"{cur_room["items"][0]}")
        cooldown()
        # get current player status
        status = player.get_status()
        cooldown()
        # check to see if able to pick up treasure
        if ((status["strength"] - status["encumbrance"] - treasure["weight"]) >= 0) and treasure["itemtype"] == "TREASURE":
            # pick up the item
            player.take_item(treaure["name"])
            cooldown()
            # run go_to_shop function
            # TODO: conditionally run the shop function depending on amount of capacity left after pickup
            go_to_shop(treasure)

    # hunt the known map for treasure and sell
    def hunting():
        # Run hunting loop until server is interupted
        while True:
            # Check, pick-up, and sell treasure
            if len(cur_room["items"]):
                handle_treasure(cur_room)
            # Choose a random direction to travel in
            next_dir = find_hunt_dir(cur_room)
            # Get room_id of next_dir from the map
            next_id = final_map[cur_room["room_id"]][next_dir]
            # Do wise explore and update cur_room
            cur_room = player.wise_explore(next_dir, next_id)
            # handle cooldown
            cooldown()
