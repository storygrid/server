from flask import Flask, request, jsonify
from cell import Cell, AUDIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

board = {}
rows = {'1', '2', '3', '4'}
columns = {'A', 'B', 'C', 'D'}


@app.route("/load", methods=['POST'])
def load():
    data = request.json
    print(data)
    return jsonify({'status': 'success', 'message': 'Data successfully loaded'})


# Load the board state
with app.app_context():
    for row in rows:
        for column in columns:
            cell_id = column + row
            board[cell_id] = Cell()

    print(board)
    print("Loaded Board!")
