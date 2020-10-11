import unittest
from src.game_platform import Game, Piece

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


if __name__ == '__main__':
    unittest.main()