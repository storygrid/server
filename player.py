class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.audio = None
        self.enabled = False

    def add_audio(self, audio):
        self.enable()
        self.audio = audio

    def get_audio(self):
        return self.audio

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
