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

if __name__ == '__main__':
    unittest.main()