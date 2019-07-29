from util import Stack, Queue
from room import Room


class Algo:
    def __init__(self):
        pass

    # start and target are both instances of Room Class
    # returns the path (list of room_id) from START to TARGET
    def bfs(self, start, target):
        que = Queue()
        # enqueue first room
        que.enqueue({"node": start, "path": []})
        bfs_visited = set()

        while que.size() > 0:
            current_room = que.queue[0]

            if current_room["node"].room_id not in bfs_visited:
                bfs_visited.add(current_room["node"].room_id)

                if current_room["node"].room_id == target.room_id:
                    current_room["path"].append(current_room["node"].room_id)
                    return current_room["path"]

                # add all neighbouring nodes to queue
                for direction in current_room["node"].get_exits():
                    room = current_room["node"].get_room_in_direction(
                        direction)

                    # Make a COPY of the PATH set from current node to neighbour nodes
                    path_to_neighbour = current_room["path"].copy()
                    path_to_neighbour.append(current_room["node"].room_id)

                    que.enqueue(
                        {"node": room, "path": path_to_neighbour})

            que.dequeue()
        return None
