# Map the physical board to the grid
board_map = {'A': 'A1', 'B': 'B1', 'C': 'C1', 'D': 'D1',
             'E': 'A2', 'F': 'B2', 'G': 'C2', 'H': 'D2',
             'I': 'A3', 'J': 'B3', 'K': 'C3', 'L': 'D3',
             'M': 'A4', 'N': 'B4', 'O': 'C4', 'P': 'D4'}

# Map the physical piece to piece number
piece_map = {'0': 'P1', '1': 'P2', '2': 'P3', '3': 'P4'}


class BoardData:
    def __init__(self, piece, pos, status):
        self.piece = piece_map[piece]
        self.pos = board_map[pos]
        if status == 'DOWN':
            self.on_board = True
        else:
            self.on_board = False
