from .board import Piece

class Player:
    piece = Piece.Empty
    pieces_amount = 12

    def __init__(self, piece):
        self.piece = piece