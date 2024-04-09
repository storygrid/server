class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.audio = None

    def add_audio(self, audio):
        self.audio = audio
