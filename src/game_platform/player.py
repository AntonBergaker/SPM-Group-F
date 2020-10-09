from .board import Board, Piece


class Player:
    """A representation of the player.
    Contains the player's piece color located in variable piece.
	Contains the amount of pieces the player has at the beginning located in variable pieces_amount.
    """

    def __init__(self, piece):
        """Initiates the Player's piece as the given piece.

        Keyword arguments:
        piece - The piece the Player will be.
        return -- Returns nothing. Initiates the Player's piece as the given piece.
        """
        self.piece = piece
        self.pieces_amount = 12
        self.latest_mill = Board.lines[0]
        self.turns_since_last_mill = 0
