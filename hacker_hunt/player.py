class Player:
    def __init__(self, p, room):
        self.name = p["name"]
        self.cooldown = p["cooldown"]
        self.encumbrance = p["encumbrance"]
        self.strength = p["strength"]
        self.speed = p["speed"]
        self.gold = p["gold"]
        self.inventory = p["inventory"]
        self.status = p["status"]
        self.errors = p["errors"]
        self.messages = p["messages"]
        # this does not come from the player dict
        self.current_room = room
