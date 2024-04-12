from boarddata import BoardData
import serial
import threading
from main import play_audio

PORT = '/dev/cu.usbmodem14301'
BAUD = 9600
TIMEOUT = 10


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
                    board_data = BoardData(piece, pos, status)
                    if board_data.on_board:
                        play_audio(board_data.pos, board_data.piece)
