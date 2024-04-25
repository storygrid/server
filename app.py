import os
import serial
import serial.tools.list_ports
import threading
import webbrowser
import sys

from flask import Flask, request, jsonify, render_template
from cell import Cell
from flask_cors import CORS
from werkzeug.utils import secure_filename
from playsound import playsound
from boarddata import BoardData

app = Flask(__name__)
CORS(app)

board = {}
rows = {'1', '2', '3', '4'}
columns = {'A', 'B', 'C', 'D'}

AUDIO_FOLDER = ''

# For reading from USB port
VID = "PID=2341"  # Vendor ID for Arduino
PORT = None
BAUD = 9600
TIMEOUT = 10


# Load POST request, receives data from front end
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

            # Save the file
            filepath = os.path.join(AUDIO_FOLDER, filename)
            print(f"Saving {filename} to {filepath}.")
            file.save(filepath)

            # Save reference
            board[board_cell_id].add_audio(player_id, filepath)

            print(f"Processed audio file: {new_file_name}")

    return jsonify({'status': 'success', 'message': 'Data successfully loaded'})


# Plays audio given the position and player
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
        with serial.Serial(baudrate=BAUD, port=PORT, timeout=TIMEOUT) as ser:
            while True:
                s = ser.readline()

                # Data: "0 @ A - UP"
                # <Piece #> @ <Cell> - <UP/DOWN>
                data = str(s)[2:]

                # Occasionally arduino produces ', so do not parse
                if data != "'":
                    # Parse the string
                    piece = data.split('@')[0].strip()
                    pos = data.split('@')[1].strip()[0]
                    status = data.split('-')[1].strip()[:-5]

                    # Convert to BoardData object which will handle the translations
                    if piece != '-1':
                        if status == 'DOWN':
                            print(f"{piece} has been placed.")
                        else:
                            print(f"{piece} has been lifted.")
                        board_data = BoardData(piece, pos, status)
                        if board_data.on_board:
                            play_audio(board_data.pos, board_data.piece)
                    else:
                        print("Piece has not been scanned!")


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5500')


@app.route('/')
def home():
    return render_template('index.html')


def setup_dir():
    global AUDIO_FOLDER
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Is it running as exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)

    AUDIO_FOLDER = os.path.join(base_dir, 'audio')
    os.makedirs(AUDIO_FOLDER, exist_ok=True)


# Runs when Flask app starts
if __name__ == '__main__':
    setup_dir()
    # Load the board state
    for row in rows:
        for column in columns:
            cell_id = column + row
            board[cell_id] = Cell(cell_id)

    print("Loaded Board!")
    # Open the Web Page
    threading.Timer(1.25, open_browser).start()

    for port, desc, hwid in serial.tools.list_ports.comports():
        if VID in hwid:
            print(f"Found Arduino Device.")
            print(f"Port set to {port}.")
            PORT = port

    if PORT is None:
        print("ERROR: Arduino Not Found!")
    else:
        # Launch the thread serial to read from USB port
        t_serial = ThreadSerial("Serial Thread")
        t_serial.start()

    try:
        app.run(port=5500)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
