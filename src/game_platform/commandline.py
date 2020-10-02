from .game import Game
from .board import Piece
import sys
import os
import colorama

# Taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console, clears the console for all platforms
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

class CommandLine:
    game = None

    def input_number(self, prompt):
      while True:
        result = input(prompt)
        if (result == 'q' or result == 'Q'):
          sys.exit()
        if result.isdigit():
          return int(result)
      

    def __init__(self, game : Game):
        self.game = game
        self.menu()
        colorama.init()

    def print_board(self):
      board = [""] * 24

      reset_code = colorama.Style.RESET_ALL + colorama.Style.DIM
      black_piece = colorama.Fore.MAGENTA +'B' + reset_code
      white_piece = colorama.Style.BRIGHT + 'W' + reset_code

      for x in range(24):
        if (self.game.board[x] == Piece.Empty):
          board[x] = ' '
        elif (self.game.board[x] == Piece.Black):
          board[x] = black_piece
        else:
          board[x] = white_piece


      clear_screen()


      board_text = """ 
1                            2                             3
  A-----------------------------C-----------------------------D
  |)                            |                           / |
  |  )                          |                         /   |
  |    )                        |                       /     |
  |      ) 4                  5 |                   6 /       |
  |        E--------------------F--------------------G        |
  |        | )                  |                 /  |        |
  |        |   )                |               /    |        |
  |        |     )              |             /      |        |
  |        |       ) 7        8 |         9 /        |        |
  |        |         H----------I----------J         |        |
  |        |         |                     |         |        |
  |        |         |                     |         |        |
10|     11 |      12 |                  13 |      14 |     15 |
  K--------L---------M                     N---------O--------P
  |        |         |                     |         |        |
  |        |      16 |         17       18 |         |        |
  |        |         Q----------R----------S         |        |
  |        |       /            |            )       |        |
  |        |     /              |              )     |        |
  |        |   /                |                )   |        |
  |     19 | /               20 |                  ) | 21     |
  |        T--------------------U--------------------V        |
  |      /                      |                      )      |
  |    /                        |                        )    |
  |  /                          |                          )  |
22|/                         23 |                          24)|
  X-----------------------------Y-----------------------------Z  """

      # So the preview looks nice, use ] instead of \\ to make the size match
      board_text = board_text.replace(")", "\\")

      # replace characters with board pieces
      board_positions = "ACDEFGHIJKLMNOPQRSTUVXYZ"

      # replace in two steps, because color codes include characters that might be replaced otherwise
      for i in range(24):
        board_text = board_text.replace(board_positions[i], "pos_" + board_positions[i])

      # replace numbers, also in two steps...
      for i in range(10):
        board_text = board_text.replace(str(i), "num_" + str(i))

      for i in range(24):
        board_text = board_text.replace("pos_" + board_positions[i], board[i])

      for i in range(10):
        board_text = board_text.replace("num_" + str(i), colorama.Fore.YELLOW + str(i) + reset_code)

      print(board_text)
      
      #if (self.game.state == Game.GameState.Placing):
        #print("Pieces left                Black: " + str(self.game.players[0].pieces_amount) + "                White: " + str(self.game.players[1].pieces_amount))
      pieces_presentation = [' '] * 63
      for i in range(self.game.players[0].pieces_amount):
        pieces_presentation[i] = black_piece
      for i in range(self.game.players[1].pieces_amount):
        pieces_presentation[62-i] = white_piece
      print("".join(pieces_presentation))


    def identify_piece(self, turn):
      if turn == 1:
        return 'Black'
      if turn == 2:
        return 'White'

    def eliminate(self):
      self.print_board()
      print(self.identify_piece(self.game.turn) + ' player has three in a row!')
      
      while True:
        position = self.input_number('Choose a piece to eliminate: ')-1
        result = self.game.can_eliminate_piece(position)
        if result == Game.CanElimateResults.Ok:
          self.game.eliminate_piece(position)
          break
        elif result == Game.CanElimateResults.NoPiece:
          print("No piece at that position.")
        elif result == Game.CanElimateResults.TargetAreThrees:
          print("Target are threes and can not be removed.")
        elif result == Game.CanElimateResults.WrongPiece:
          print("You can't eliminate your own piece")
        elif result == Game.CanElimateResults.OutsideBoard:
          print("Position is outside the board")
        else:
          print("Something went wrong")

    def play(self):
      print('Its '+ self.identify_piece(self.game.turn) + ' player\'s turn to play')
      if self.game.state == Game.GameState.Placing:
        while True:
          position = self.input_number('Choose a spot to place: ')-1

          result = self.game.can_place_piece(self.game.turn, position)
          if result == Game.CanPlaceResults.Ok:
            place_result = self.game.place_piece(self.game.turn, position)
            if place_result == Game.PlaceResults.GotThree:
              self.eliminate()
            break
          elif result == Game.CanPlaceResults.Occupied:
            print("There is already something at this position.")
          elif result == Game.CanPlaceResults.WrongPiece:
            print("Wrong turn (this shouldn't be possible to happen).")
          elif result == Game.CanPlaceResults.WrongState:
            print("Placing is not allowed at this time (this shouldn't be possible to happen).")
          elif result == Game.CanPlaceResults.OutsideBoard:
            print("Position is outside the board.")
          else:
            print("Something went wrong.")


      elif self.game.state == Game.GameState.Moving:
        while True:
          position = self.input_number('Which piece would you like to move?: ')-1
          new_position = self.input_number('To what position would you like to move?: ')-1
          result = self.game.can_move_piece(position, new_position)
          if result == Game.CanMoveResults.Ok:
            move_result = self.game.move_piece(position, new_position)
            if move_result == Game.MoveResults.GotThree:
              self.eliminate()
            break
          elif result == Game.CanMoveResults.WrongPiece:
            print("Can't move opponents/empty piece.")
          elif result == Game.CanMoveResults.SamePosition:
            print("Can't move to same position")   
          elif result == Game.CanMoveResults.OutsideBoard:
            print("Position is outside the board.")
          elif result == Game.CanMoveResults.NotAdjacent:
            print("The positions are not nearby.")
          elif result == Game.CanMoveResults.NewPositionOccupied:
            print("The new position is occupied.")
          elif result == Game.CanMoveResults.WrongState:
            print("Moving pieces are not allowed at this time (this shouldn't be possible to happen).")
          else:
            print("Something went wrong.")

    def menu(self):
      while True:
        print('### UU-GAME ###')
        print('1. Play a new game')
        print('2. How to play')
        print('3. Quit')
        
        user_input = input('Please enter your choice from the menu and press enter: ')
        if user_input == '1':  
          while(True):
            self.print_board()
            self.play()

            if (self.game.check_if_piece_won_game(Piece.Black)):
              self.print_board()
              print("Black has won the game")
              break
            if (self.game.check_if_piece_won_game(Piece.White)):
              self.print_board()
              print("White has won the game")
              break

        elif user_input == '2':
          clear_screen()
          print("This is how you play....")
          print("TBA")
          menu_input = input('<- Back to main menu, input 1 and press enter: ')
          if menu_input == '1':
            clear_screen()

        elif user_input == '3':
          return
              
