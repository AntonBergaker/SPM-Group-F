class Piece:
    Empty = 0
    Black = 1
    White = 2

class Board:
    board = None

    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [9, 10, 11],
        [12, 13, 14],
        [15, 16, 17],
        [18, 19, 20],
        [21, 22, 23],
        [0, 9, 21],
        [3, 10, 18],
        [6, 11, 15],
        [8, 12, 17],
        [5, 13, 20],
        [2, 14, 23],
        [0, 3, 6],
        [2, 5, 8],
        [15, 18, 21],
        [17, 20, 23],
        [1, 4, 7],
        [16, 19, 22]
    ]

    def pieces_of_type_on_board(self, piece):
        count = 0
        for piece_in_board in self.board:
            if (piece == piece_in_board):
                count += 1
        return count

    def positions_are_adjacent(self, position, other_position):
        if (position == other_position):
            return False

        lines = self.get_lines_for_position(position)
        for line in lines:
            if (other_position in line):
                if (abs(line.index(position) - line.index(other_position)) == 1):
                    return True
        
        return False


    def get_lines_for_position(self, position):
        found_lines = []

        for line in self.lines:
            if (position in line):
                found_lines.append(line)

        return found_lines

    def has_three_at_position(self, piece, position):
        lines = self.get_lines_for_position(position)
        for line in lines:
            line_full = True
            for position in line:
                if (self.board[position] != piece):
                    line_full = False
                    break
            if (line_full):
                return True

        return False

    def get_other_piece(self, piece):
        if (piece == Piece.Black):
            return Piece.White
        if (piece == Piece.White):
            return Piece.Black
        return Piece.Empty

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def __init__(self):
        self.board = [Piece.Empty] * 24