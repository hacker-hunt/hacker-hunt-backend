class Room:
    def __init__(self, r):
        self.room_id = r["room_id"]
        self.title = r["title"]
        self.description = r["description"]
        self.coordinates = r["coordinates"]
        self.players = r["players"]
        self.items = r["items"]
        self.exits = r["exits"]
        self.cooldown = r["cooldown"]
        self.errors = r["errors"]
        self.messages = r["messages"]

        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

    def connect_rooms(self, direction, connectingRoom):
        if direction == "n":
            self.n_to = connectingRoom
            connectingRoom.s_to = self
        elif direction == "s":
            self.s_to = connectingRoom
            connectingRoom.n_to = self
        elif direction == "e":
            self.e_to = connectingRoom
            connectingRoom.w_to = self
        elif direction == "w":
            self.w_to = connectingRoom
            connectingRoom.e_to = self
        else:
            print("INVALID ROOM CONNECTION")
            return None

    def get_room_in_direction(self, direction):
        if direction == "n":
            return self.n_to
        elif direction == "s":
            return self.s_to
        elif direction == "e":
            return self.e_to
        elif direction == "w":
            return self.w_to
        else:
            return None

    def get_coords(self):
        return self.coordinates

    def get_exits(self):
        return self.exits

    def get_items(self):
        return self.items

    def get_cooldown(self):
        return self.cooldown
