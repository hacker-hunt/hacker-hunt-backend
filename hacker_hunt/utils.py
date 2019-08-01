consts = {
    'path': 'https://lambda-treasure-hunt.herokuapp.com/api/adv/',
    'init': 'init/',
    'status': 'status/',
    'move': 'move/',
    'take': 'take/',
    'drop': 'drop/',
    'sell': 'sell/',
    'examine': 'examine/',
    'change_name': 'change_name/',
    'pray': 'pray/',
    'fly': 'fly/',
    'dash': 'dash/',
    'transmogrify': 'transmogrify/',
    # paths below belong to bc_url
    'bc_url': 'https://lambda-treasure-hunt.herokuapp.com/api/bc/',
    'mine': 'mine/',
    'last_proof': 'last_proof/',
    'get_balance': 'get_balance/'
}


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

    def get_stack(self):
        return self.stack

    def replace_stack(self, new_stack):
        self.stack = new_stack
