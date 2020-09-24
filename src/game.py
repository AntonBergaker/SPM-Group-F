from board import Board, Piece
from player import Player

class Game:
    turn = Piece.Black
    board = Board()
    players = [Player(Piece.Black), Player(Piece.White)]

    StatePlacing = 1
    StateMoving = 2
    state = 0

    eliminating = 0

    def get_player_from_piece(self, piece):
        if (piece == Piece.Black):
            return self.players[0]
        if (piece == Piece.White):
            return self.players[1]
        return None

    # Returns if we got 3 in a row
    class PlaceResults:
        Failed = -1
        Placed = 1
        GotThree = 2
    def place_piece(self, piece, position):
        if (self.can_place_piece(piece, position) != self.CanPlaceResults.Ok):
            return self.PlaceResults.Failed

        self.board[position] = piece
        player = self.get_player_from_piece(self.turn)
        player.pieces_amount -= 1

        if (self.players[0].pieces_amount == 0 and self.players[1].pieces_amount == 0):
            self.state = self.StateMoving

        if (self.board.has_three_at_position(piece, position)):
            self.eliminating = True
            return self.PlaceResults.GotThree

        self.turn = self.board.get_other_piece(self.turn)
        return self.PlaceResults.Placed

    class CanPlaceResults:
        Ok = 1
        Occupied = -1
        WrongPiece = -2
        WrongState = -3
        OutsideBoard = -4
    def can_place_piece(self, piece, position):
        if (position < 0 or position > 23):
            return self.CanPlaceResults.OutsideBoard
        if (self.turn != piece):
            return self.CanPlaceResults.WrongPiece
        if (self.board[position] != Piece.Empty):
            return self.CanPlaceResults.Occupied
        if (self.eliminating):
            return self.CanPlaceResults.WrongState
        return self.CanPlaceResults.Ok

    def eliminate_piece(self, position):
        if (self.can_eliminate_piece(position) != self.CanElimateResults.Ok):
            return False
        self.board[position] = Piece.Empty
        self.eliminating = False
        return True

    class CanElimateResults:
        Ok = 1
        NoPiece = -1
        TargetAreThrees = -2
        WrongPiece = -3
        WrongState = -4
        OutsideBoard = -5
    def can_eliminate_piece(self, position):
        """Checks if a piece can be eliminated
        Returns Ok when it is ok to eliminate the piece
        Returns NoPiece when there is no piece to eliminate at that has_three_at_position
        Returns TargetAreThrees when the target is part of a threes and can not be eliminated
        Returns WrongPiece when the target do not belong to the opponent and can not be eliminated
        Returns WrongState when it is not time to eliminate a piece
        Returns OutsideBoard when the target is outside the board and can not be eliminated

        Keyword arguments:
        position -- The position to check


        """
    if imag == 0.0 and real == 0.0:
        return complex_zero

        """
        if (position < 0 or position > 23):
            return self.CanElimateResults.OutsideBoard
        if (self.board[position] == Piece.Empty):
            return self.CanElimateResults.NoPiece
        if (self.board[position] == self.turn):
            return self.CanElimateResults.WrongPiece
        if (self.eliminating == False):
            return self.CanElimateResults.WrongState
        if (self.board.has_three_at_position(self.board.get_other_piece(self.turn) ,position)):
            return self.CanElimateResults.TargetAreThrees
        return self.CanElimateResults.Ok
