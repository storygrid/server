class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.audio_path = None
        self.enabled = False
        self.audio_file = None

    def add_audio(self, audio_path, file_name):
        self.enable()
        self.audio_path = audio_path
        self.audio_file = file_name

    def get_audio(self):
        return self.audio_path

    def get_audio_file(self):
        return self.audio_file

    def remove_audio_file(self):
        self.audio_file = None
        self.audio_path = None
        self.enabled = False

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
