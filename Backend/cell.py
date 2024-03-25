AUDIO = 1

class Cell:
    def __init__(self):
        self.actions = {}

    def add_action(self, piece, action):
        self.actions[piece] = action
