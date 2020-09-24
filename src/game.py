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
        if (position < 0 or position > 23):
            return self.CanElimateResults.OutsideBoard
        if (self.board[position] == Piece.Empty):
            return self.CanElimateResults.NoPiece
        if (self.board[position] == self.turn):
            return self.CanElimateResults.WrongPiece
        if (self.eliminating == False):
            return self.CanElimateResults.WrongState
        
        # If all opponent pieces are three, we can elimate anything
        opponent_piece = self.board.get_other_piece(self.turn)
        all_are_threes = True
        for check_position in range(24):
            pass

        if (self.board.has_three_at_position(opponent_piece ,position)):
            return self.CanElimateResults.TargetAreThrees
        
        return self.CanElimateResults.Ok

    class MoveResults:
        Ok = 1
        GotThree = 2
        Failed = -1
    def move_piece(self, position, new_position):
        """Moves a piece from a position to another.
        Returns a MoveResults containing information about the move.
        Returns Ok if the move was successful.
        Returns GotThree if the resulting move resulted in threes.
        Returns Failed if the move was invalid.

        Keyword arguments:
        position -- the position we move from
        new_position -- the position we move to
        return -- a MoveResults result
        """
        if (self.can_move_piece(position, new_position) != self.CanMoveResults.Ok):
            return self.MoveResults.Failed
        piece_at_old_position = self.board[position]
        self.board[position] = Piece.Empty
        self.board[new_position] = piece_at_old_position
        
        if (self.board.has_three_at_position(piece_at_old_position, new_position)):
            self.eliminating = True
            return self.MoveResults.GotThree
        
        return self.MoveResults.Ok
      
    class CanMoveResults:
        Ok = 1
        WrongPiece = -1
        SamePosition = -2
        OutsideBoard = -3
        NotAdjacent = -4
        NewPositionOccupied = -5,
        WrongState = -6   
    def can_move_piece(self, position, new_position):
        """Checks if a piece at a position can be moved to the given position.
        Returns a CanMoveResults containing information about the move.
        Returns Ok if the move was successful.
        Returns WrongPiece if the piece was not associated with the current turn.
        Returns SamePosition if the position and the new position are the same.
        Returns OutSideBoard if any position was outside the board.
        Returns NotAdjacent if the two positions are not adjacent and adjacent movements are required.
        Returns NewPositionOccupied if there's already a piece at the target location.
        Returns WrongState if the game is not in a movement state

        Keyword arguments:
        position -- the position we move from
        new_position -- the position we move to
        return -- a CanMoveResult result
        """
        if (position < 0 or position > 23 or
            new_position < 0 or new_position > 23):
            return self.CanMoveResults.Ok
        if (self.turn != self.board[position]):
            return self.CanMoveResults.WrongPiece
        if (position == new_position):
            return self.CanMoveResults.SamePosition
        if (self.board[new_position] != Piece.Empty):
            return self.CanMoveResults.NewPositionOccupied
        
        moved_piece = self.board[position]
        total_on_board = self.board.pieces_of_type_on_board(moved_piece)
        # If you have three pieces left you're allowed to fly so the adjacent rule doesn't apply
        if (total_on_board > 3):
            if (self.board.positions_are_adjacent(position, new_position) == False):
                return self.CanMoveResults.NotAdjacent

        return self.CanMoveResults.Ok