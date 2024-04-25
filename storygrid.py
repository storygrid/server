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
            # Sanitize
            filename = secure_filename(file.filename)

            # Save the file
            folder = os.path.join(AUDIO_FOLDER, board_cell_id + "_" + player_id)
            filepath = os.path.join(folder, filename)
            print(f"Saving {file.filename} to {filepath}.")
            file.save(filepath)

            # Save reference
            board[board_cell_id].add_audio(player_id, filepath)

            print(f"Processed audio file: {file.filename}")

    return jsonify({'status': 'success', 'message': 'Data successfully loaded'})


@app.route("/play", methods=['GET'])
def play():
    cell = request.args.get('cell')
    player = request.args.get('player')

    if cell is None or player is None:
        return "Missing parameters", 400

    if not board[cell].get_player(player).enabled:
        return "Player disabled", 400

    play_audio(cell, player)

    return f"Audio requested for board cell {cell} and player {player}"


# Plays audio given the position and player
def play_audio(board_cell_id, player_id):
    player = board[board_cell_id].get_player(player_id)
    file_path = player.get_audio()
    if player.enabled:
        print(f"Playing audio on {board_cell_id} for {player_id} from {file_path}.")
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

    # Make folder for each audio file
    alphas = ['A', 'B', 'C', 'D']
    players = ['P1', 'P2', 'P3', 'P4']
    for i in range(1, 5):
        for alpha in alphas:
            for player in players:
                name = alpha + str(i) + '_' + player
                new_folder = os.path.join(AUDIO_FOLDER, name)
                os.makedirs(new_folder, exist_ok=True)


def load_board():
    for row in rows:
        for column in columns:
            cell_id = column + row
            board[cell_id] = Cell(cell_id)

    global AUDIO_FOLDER
    for root, dirs, files in os.walk(AUDIO_FOLDER, topdown=True):
        if len(files) > 0:
            file_path = os.path.join(root, files[0])
            parent_directory = os.path.basename(os.path.dirname(file_path))
            print(f"Loaded existing file: {file_path}")

            board_cell_id = parent_directory.split('_')[0]
            player_id = parent_directory.split('_')[1]
            board[board_cell_id].add_audio(player_id, file_path)


# Runs when Flask app starts
if __name__ == '__main__':
    setup_dir()
    # Load the board state
    load_board()

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
