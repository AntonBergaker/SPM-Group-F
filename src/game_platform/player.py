from .board import Board, Piece


class Player:
    """A representation of the player.
    Contains the player's piece color located in variable piece.
	Contains the amount of pieces the player has at the beginning located in variable pieces_amount.
    """

    def __init__(self, piece, piece_count):
        """Initiates the Player's piece as the given piece.

        Keyword arguments:
        piece - The piece the Player will be.
        return -- Returns nothing. Initiates the Player's piece as the given piece.
        """
        self.piece = piece
        self.pieces_amount = piece_count
        self.latest_mill = [0] * Board.position_count
        self.previous_move = [0]*3

    def increase_position_move_count(self):
        """ Increases the position move count on every positions on the board

        return -- nothing
        """
        for position in range(Board.position_count):
            self.latest_mill[position] += 1
