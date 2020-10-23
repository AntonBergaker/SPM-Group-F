import unittest
from src.game_platform import Game, Piece
import json

class TestGame(unittest.TestCase):
    def test_turn_changed(self):
        game = Game()   

        # Black should start
        self.assertEqual(game.turn, Piece.Black)

        game.place_piece(Piece.Black, 0)
        # White comes after a successful placement
        self.assertEqual(game.turn, Piece.White)

        game.place_piece(Piece.White, 0)
        # Still white after an unsucessful placement
        self.assertEqual(game.turn, Piece.White)

    def test_tie(self):
        game = Game()

        # The painful process of making a board
        game.place_piece(game.turn, 0)
        game.place_piece(game.turn, 3)
        game.place_piece(game.turn, 1)
        game.place_piece(game.turn, 4)
        game.place_piece(game.turn, 2)
        game.eliminate_piece(3)
        game.place_piece(game.turn, 3)
        game.place_piece(game.turn, 9)
        game.place_piece(game.turn, 5)
        game.eliminate_piece(9)
        game.place_piece(game.turn, 6)
        game.place_piece(game.turn, 9)
        game.place_piece(game.turn, 7)
        game.place_piece(game.turn, 10)
        game.place_piece(game.turn, 8)
        game.eliminate_piece(10)
        game.place_piece(game.turn, 10)
        game.place_piece(game.turn, 12)
        game.place_piece(game.turn, 11)
        game.eliminate_piece(12)
        game.place_piece(game.turn, 12)
        game.place_piece(game.turn, 13)
        game.place_piece(game.turn, 14)
        game.place_piece(game.turn, 15)
        game.place_piece(game.turn, 16)
        game.place_piece(game.turn, 17)
        game.place_piece(game.turn, 18)
        game.place_piece(game.turn, 19)

        self.assertEqual(Game.GameStage.Moving, game.state) 
        
        # Make sure we're still in a playing state
        self.assertEqual(Game.WinnerResults.GameInProgress, game.get_game_winner())

        #  Makes a board that looks like this:
        #         
        # 1                            2                             3
        #   B-----------------------------B-----------------------------B
        #   |\                            |                           / |
        #   |  \                          |                         /   |
        #   |    \                        |                       /     |
        #   |      \ 4                  5 |                   6 /       |
        #   |        W--------------------W--------------------W        |
        #   |        | \                  |                 /  |        |
        #   |        |   \                |               /    |        |
        #   |        |     \              |             /      |        |
        #   |        |       \ 7        8 |         9 /        |        |
        #   |        |         B----------B----------B         |        |
        #   |        |         |                     |         |        |
        #   |        |         |                     |         |        |
        # 10|     11 |      12 |                  13 |      14 |     15 |
        #   W--------W---------W                     B---------W--------B
        #   |        |         |                     |         |        |
        #   |        |      16 |         17       18 |         |        |
        #   |        |         W----------B----------W         |        |
        #   |        |       /            |            \       |        |
        #   |        |     /              |              \     |        |
        #   |        |   /                |                \   |        |
        #   |     19 | /               20 |                  \ | 21     |
        #   |        B--------------------W--------------------         |
        #   |      /                      |                      \      |
        #   |    /                        |                        \    |
        #   |  /                          |                          \  |
        # 22|/                         23 |                          24\|
        #    ----------------------------- -----------------------------

        # Move back and forth ~200 times
        for i in range(50):
            game.move_piece(18, 21)
            game.move_piece(19, 22)
            game.move_piece(21, 18)
            game.move_piece(22, 19)

        self.assertEqual(Game.WinnerResults.Tie, game.get_game_winner())


    def test_mill_wait(self):
        game = Game(4)

        game.place_piece(game.turn, 0)
        game.place_piece(game.turn, 21)
        game.place_piece(game.turn, 1)
        game.place_piece(game.turn, 22)
        game.place_piece(game.turn, 2)
        game.eliminate_piece(22)
        game.place_piece(game.turn, 22)
        game.place_piece(game.turn, 18)
        game.place_piece(game.turn, 19)

        self.assertEqual(Game.GameStage.Moving, game.state)

        # Moves black down
        game.move_piece(0, 3)

        # Waste a turn on white
        game.move_piece(19, 20)

        # Move black back
        game.move_piece(3, 0)

        self.assertEqual(False, game.eliminating)

        # Waste 2 turns
        game.move_piece(20, 19)
        game.move_piece(0, 3)
        game.move_piece(19, 20)
        game.move_piece(18, 10)
        game.move_piece(20, 19)
        
        game.move_piece(3, 0)
        self.assertEqual(True, game.eliminating)

    def test_serialization(self):
        game = Game(5)
        game.place_piece(game.turn, 0)
        game.place_piece(game.turn, 1)
        game.place_piece(game.turn, 2)

        game_json = json.dumps(game.serialize())
        new_game = Game.deserialize( json.loads(game_json) )

        self.assertEqual(game.turn, new_game.turn)
        self.assertEqual(game.state, new_game.state)
        self.assertEqual(game.players[0].pieces_amount, new_game.players[0].pieces_amount)
        self.assertEqual(game.players[1].pieces_amount, new_game.players[1].pieces_amount)
        self.assertEqual(game.total_turns, new_game.total_turns)

        for i in range(game.board.position_count):
            self.assertEqual(game.board[i], new_game.board[i])

        print(game_json)


if __name__ == '__main__':
    unittest.main()