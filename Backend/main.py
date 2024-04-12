import os

from flask import Flask, request, jsonify
from cell import Cell
from flask_cors import CORS
from werkzeug.utils import secure_filename
from playsound import playsound
from board_data import BoardData
import serial
import threading

app = Flask(__name__)
CORS(app)

board = {}
rows = {'1', '2', '3', '4'}
columns = {'A', 'B', 'C', 'D'}

AUDIO_FOLDER = 'audio'


@app.route("/load", methods=['POST'])
def load():
    # Process other values
    for key, value in request.form.items():
        print(f"Processed data: [{key}, {value}]")

    # Process files
    for key, file in request.files.items():
        # key in the format A1_P1+audio if audio
        action = key.split("+")[1]
        board_cell_id = key.split("+")[0].split("_")[0]
        player_id = key.split("+")[0].split("_")[1]

        if action == "audio":
            # Rename audio file
            new_file_name = board_cell_id + "_" + player_id + ".mp3"

            # Sanitize
            filename = secure_filename(new_file_name)
            filepath = os.path.join(AUDIO_FOLDER, filename)
            file.save(filepath)

            # Save reference
            board[board_cell_id].add_audio(player_id, filepath)

            print(f"Processed audio file: {new_file_name}")

    return jsonify({'status': 'success', 'message': 'Data successfully loaded'})


def play_audio(board_cell_id, player_id):
    player = board[board_cell_id].get_player(player_id)
    file_path = player.get_audio()
    if player.enabled:
        print(f"Playing audio on {board_cell_id} for {player_id}")
        if file_path is not None:
            playsound(file_path)


class ThreadSerial(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Started Serial Thread.")
        with serial.Serial(baudrate=9600, port='/dev/cu.usbmodem14301', timeout=10) as ser:
            while True:
                s = ser.readline()
                data = str(s)[2:]
                if data != "'":
                    piece = data.split('@')[0].strip()
                    pos = data.split('@')[1].strip()[0]
                    status = data.split('-')[1].strip()[:-5]

                    board_data = BoardData(piece, pos, status)
                    if board_data.on_board:
                        play_audio(board_data.pos, board_data.piece)


# Load the board state
with app.app_context():
    for row in rows:
        for column in columns:
            cell_id = column + row
            board[cell_id] = Cell(cell_id)

    print("Loaded Board!")
    tserial = ThreadSerial("Serial Thread")
    tserial.start()
