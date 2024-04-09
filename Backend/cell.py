from player import Player


class Cell:
    def __init__(self, cell_id):
        self.cell_id = cell_id
        # Initialize 4 players
        self.players = {"P1": Player("P1"), "P2": Player("P2"), "P3": Player("P3"), "P4": Player("P4")}

    def add_audio(self, player: str, audio):
        self.players[player].add_audio(audio)

    def get_player(self, player: str):
        if player in self.players:
            return self.players[player]

        return None
