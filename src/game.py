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
    PlaceResultFailed = -1
    PlaceResultPlaced = 1
    PlaceResultGotThree = 2
    def place_piece(self, piece, position):
        if (self.can_place_piece(piece, position) != self.PlaceOk):
            return self.PlaceResultFailed

        self.board[position] = piece
        player = self.get_player_from_piece(self.turn)
        player.pieces_amount -= 1
        
        if (self.players[0].pieces_amount == 0 and self.players[1].pieces_amount == 0):
            self.state = self.StateMoving

        if (self.board.has_three_at_position(piece, position)):
            self.eliminating = True
            return self.PlaceResultGotThree
        
        self.turn = self.board.get_other_piece(self.turn)
        return self.PlaceResultPlaced

    PlaceOk = 1
    PlaceOccupied = -1
    PlaceWrongPiece = -2
    PlaceWrongState = -3
    def can_place_piece(self, piece, position):
        if (self.turn != piece):
            return self.PlaceWrongPiece
        if (self.board[position] != Piece.Empty):
            return self.PlaceOccupied
        if (self.eliminating):
            return self.PlaceWrongState
        return self.PlaceOk

    def eliminate_piece(self, position):
        if (self.can_eliminate_piece(position) != self.EliminateOk):
            return False
        self.board[position] = Piece.Empty
        return True
    
    EliminateOk = 1
    EliminateNoPiece = -1
    EliminateTargetAreThrees = -2
    EliminateWrongPiece = -3
    EliminateWrongState = -4
    def can_eliminate_piece(self, position):
        if (self.board[position] == Piece.Empty):
            return self.EliminateNoPiece
        if (self.board[position] == self.turn):
            return self.EliminateWrongPiece
        if (self.eliminating == False):
            return self.EliminateWrongState
        if (self.board.has_three_at_position(self.board.get_other_piece(self.turn) ,position)):
            return self.EliminateTargetAreThrees
        return self.EliminateOk
    