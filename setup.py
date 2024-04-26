import webbrowser
import sys
import os
from cell import Cell

rows = {'1', '2', '3', '4'}
columns = {'A', 'B', 'C', 'D'}


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5500')


def setup_dir() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Is it running as exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)

    audio_folder = os.path.join(base_dir, 'audio')
    os.makedirs(audio_folder, exist_ok=True)

    # Make folder for each audio file
    alphas = ['A', 'B', 'C', 'D']
    players = ['P1', 'P2', 'P3', 'P4']
    for i in range(1, 5):
        for alpha in alphas:
            for player in players:
                name = alpha + str(i) + '_' + player
                new_folder = os.path.join(audio_folder, name)
                os.makedirs(new_folder, exist_ok=True)

    return audio_folder


def load_board(board, audio_folder):
    for row in rows:
        for column in columns:
            cell_id = column + row
            board[cell_id] = Cell(cell_id)

    for root, dirs, files in os.walk(audio_folder, topdown=True):
        for file_name in files:
            _, file_ext = os.path.splitext(file_name)
            if file_ext.lower() == '.mp3':
                file_path = os.path.join(root, files[0])
                parent_directory = os.path.basename(os.path.dirname(file_path))
                print(f"Loaded existing file: {file_path}")

                board_cell_id = parent_directory.split('_')[0]
                player_id = parent_directory.split('_')[1]
                board[board_cell_id].add_audio(player_id, file_path, files[0])
            else:
                print(f"Skipped non-MP3 file: {file_name}")
