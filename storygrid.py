import os
import serial
import serial.tools.list_ports
import threading

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from playsound import playsound
from boarddata import BoardData
from setup import load_board, open_browser, setup_dir

app = Flask(__name__)
CORS(app)

board = {}

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


@app.route('/')
def home():
    return render_template('index.html')


# Load any existing file information
@app.route("/setup", methods=['GET'])
def setup():
    data = {}
    players = ['P1', 'P2', 'P3', 'P4']
    cells = ['A1', 'A2', 'A3', 'A4',
             'B1', 'B2', 'B3', 'B4',
             'C1', 'C2', 'C3', 'C4',
             'D1', 'D2', 'D3', 'D4']

    for cell in cells:
        data[cell] = {}
        for player in players:
            if board[cell].get_player(player).enabled:
                data[cell][player] = board[cell].get_player(player).get_audio_file()

    return jsonify(data)


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


# Runs when Flask app starts
if __name__ == '__main__':
    AUDIO_FOLDER = setup_dir()

    load_board(board, AUDIO_FOLDER)

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
