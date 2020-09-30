class Piece:
    """A representation of the color of the pieces.
	A piece is Empty if it has not been assigned a color yet. Otherwise it is Black or White.
    """
	
    Empty = 0
    Black = 1
    White = 2

class Board:
    """A representation of the board.
	Contains a board located in variable board that is empty.
	Contains all mill possibilities located in variable lines.
    """
	
    board = None

    mills = [
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


    def get_mills_for_position(self, position):
        """Looks for which mills the given position can be in.
        It will go through every possible mills to find those who contain the given position.
		It will then return all possible mills that contains the given position.

        Keyword arguments:
        position -- The position to look for in possible mills.
        return -- An array of all possible mills the given position can be in.
        """
        found_mills = []

        for mill in self.mills:
            if (position in mill):
                found_mills.append(mill)

        return found_mills

    def has_three_at_position(self, piece, position):
        """Looks for possible mills the given position can be in.
        It will look at the mills the given piece on the given position can be at and check if any of the mills are actual mills.
		
        Keyword arguments:
        piece - The piece to check if it is in a mill.
        position -- The position to look for in possible mills.
        return -- True if the given piece on the given position is in a mill. Otherwise False.
        """
        mills = self.get_mills_for_position(position)
        for mill in mills:
            mill_full = True
            for position in mill:
                if (self.board[position] != piece):
                    mill_full = False
                    break
            if (mill_full):
                return True

        return False

    def get_other_piece(self, piece):
        """Gets the opposite color of the given piece.
        If the given piece is Piece.Black it will return Piece.White and vice versa. Otherwise it will return Piece.Empty.

        Keyword arguments:
        piece - The given color to get its opposite color.
        return -- Returns Piece.White if the given piece is Piece.Black and vice versa. Otherwise it will return Piece.Empty.
        """
        if (piece == Piece.Black):
            return Piece.White
        if (piece == Piece.White):
            return Piece.Black
        return Piece.Empty

    def __getitem__(self, index):
        """Gets what is on the given position on the board.

        Keyword arguments:
        index - An index on the board
        return -- Returns what is on the given index on the board.
        """
        return self.board[index]

    def __setitem__(self, index, value):
        """Updates the board on the given index with the given value.

        Keyword arguments:
        index - An index on the board to place the given value.
        value - The value to be placed on the given index on the board.
        return -- Returns nothing. Sets the given value on the given index on the board.
        """
        self.board[index] = value

    def __init__(self):
        """Initiates the board with 24 empty positions.

        Keyword arguments:
        return -- Returns nothing. Initiates the board with 24 empty positions.
        """
        self.board = [Piece.Empty] * 24