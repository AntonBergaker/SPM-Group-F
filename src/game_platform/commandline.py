from .game import Game
from .board import Piece
import sys
import os

# Taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console, clears the console for all platforms
def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name=='nt' else 'clear')

class CommandLine:
    """Handles the GUI and the user's input. Contains a game in the variable game."""
    game = None

    def input_number(self, prompt):
      """Checks if the user's given input is an integer. If the user's input is q or Q the program will exit.
        It will keep asking the user for an input until it is valid.

        Keyword arguments:
        prompt -- The message to be printed to the user.
        return -- Exits the program if the user's input is q or Q. Otherwise the users input if it is an integer.
      """
      while True:
        result = input(prompt)
        if (result == 'q' or result == 'Q'):
          sys.exit()
        if result.isdigit():
          return int(result)

    def __init__(self):
        """Initializes the given game into class variable game and starts the main menu."""
        self.menu()

    def print_board(self):
      """Prints the board and the pieces on the board. It also prints how many pieces each player has.

        Keyword arguments:
        return -- Prints out the board.
      """
      board = [""] * 24
      for x in range(24):
        if (self.game.board[x] == Piece.Empty):
          board[x] = ' '
        elif (self.game.board[x] == Piece.Black):
          board[x] = 'B'
        else:
          board[x] = 'W'

      clear_screen()
      print(" 1                            2                             3")
      print("  "+board[0]+"-----------------------------"+board[1]+"-----------------------------"+board[2])
      print("  |\\                            |                           / |")
      print("  |  \\                          |                         /   |")
      print("  |    \\                        |                       /     |")
      print("  |      \\ 4                  5 |                   6 /       |")
      print("  |        "+board[3]+"--------------------"+board[4]+"--------------------"+board[5]+"        |")
      print("  |        | \\                  |                 /  |        |")
      print("  |        |   \\                |               /    |        |")
      print("  |        |     \\              |             /      |        |")
      print("  |        |       \\ 7        8 |         9 /        |        |")
      print("  |        |         "+board[6]+"----------"+board[7]+"----------"+board[8]+"         |        |")
      print("  |        |         |                     |         |        |")
      print("  |        |         |                     |         |        |")
      print("10|     11 |      12 |                  13 |      14 |     15 |")
      print("  "+board[9]+"--------"+board[10]+"---------"+board[11]+"                     "+board[12]+"---------"+board[13]+"--------"+board[14])
      print("  |        |         |                     |         |        |")
      print("  |        |      16 |         17       18 |         |        |")
      print("  |        |         "+board[15]+"----------"+board[16]+"----------"+board[17]+"         |        |")
      print("  |        |       /            |            \\       |        |")
      print("  |        |     /              |              \\     |        |")
      print("  |        |   /                |                \\   |        |")
      print("  |     19 | /               20 |                  \\ | 21     |")
      print("  |        "+board[18]+"--------------------"+board[19]+"--------------------"+board[20]+"        |")
      print("  |      /                      |                      \\      |")
      print("  |    /                        |                        \\    |")
      print("  |  /                          |                          \\  |")
      print("22|/                         23 |                          24\\|")
      print("  "+board[21]+"-----------------------------"+board[22]+"-----------------------------"+board[23]+"  ")
      #if (self.game.state == Game.GameState.Placing):
        #print("Pieces left                Black: " + str(self.game.players[0].pieces_amount) + "                White: " + str(self.game.players[1].pieces_amount))
      pieces_presentation = [' '] * 63
      for i in range(self.game.players[0].pieces_amount):
        pieces_presentation[i] = 'B'
      for i in range(self.game.players[1].pieces_amount):
        pieces_presentation[62-i] = 'W'
      print("".join(pieces_presentation))


    def identify_piece(self, turn):
      """ Identifies which player's turn it is.

        Keyword arguments:
        turn -- The current turn of the game.
        return -- Returns Black if the given turn is 1 or White if the given turn is 2.
      """
      if turn == 1:
        return 'Black'
      if turn == 2:
        return 'White'

    def eliminate(self):
      """Gets the user's input on which opponent piece it wants to eliminate when the user has created a mill.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid opponent piece, the opponent piece will be removed.
        Prints out different messages depending on the user's input and updates the board accordingly.

        Keyword arguments:
      """
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


    def place(self):
        """Gets the user's input on where to place.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid position, a piece will be placed.
        Prints out different messages depending on the user's input and updates the board accordingly.

        Keyword arguments:
        """
        print('Its '+ self.identify_piece(self.game.turn) + ' player\'s turn to play')
        while True:
          position = self.input_number('Choose a spot to place: ')-1

          result = self.game.can_place_piece(self.game.turn, position)
          if result == Game.CanPlaceResults.Ok:
            self.game.place_piece(self.game.turn, position)
            break
          elif result == Game.CanPlaceResults.Occupied:
            print("There is already something at this position.")
          elif result == Game.CanPlaceResults.WrongPiece:
            print("Wrong turn (this shouldn't be possible to happen).")
          elif result == Game.CanPlaceResults.WrongState:
            print("Placing is not allowed at this time (this shouldn't be possible to happen).")
            return # Safety return here. Wrong state means no placement can happen
          elif result == Game.CanPlaceResults.OutsideBoard:
            print("Position is outside the board.")
          else:
            print("Something went wrong.")

    def move(self):
        """Gets the user's input on where to move.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid position, a piece will be moved.
        Prints out different messages depending on the user's input and updates the board accordingly.

        Keyword arguments:
        """
        while True:
          position = self.input_number('Which piece would you like to move?: ')-1
          new_position = self.input_number('To what position would you like to move?: ')-1
          result = self.game.can_move_piece(position, new_position)
          if result == Game.CanMoveResults.Ok:
            self.game.move_piece(position, new_position)
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
            return # Safety return here. Wrong state means no moving can happen
          else:
            print("Something went wrong.")

    def play(self):
      """It checks first which game state the game is in. If the game state is on state Placing then it will ask the user which position it wants to place its piece.
        Depending on the user's input, different messages will be printed out. If the user places a piece on which it creates a mill, the user will be asked which
        opponent piece it wants to eliminate. If the game state is on s1
        tate Moving then it will ask the user which one of its pieces it wants to move. Depending on the
        user's input, different messages will be printed out. If the user moves its piece on another valid position which it creates a mill, the user will be
        asked which opponent piece it wants to eliminate.

        Keyword arguments:
        return -- Prints out different messages depending on the user's input and updates the board accordingly.
      """

      if (self.game.eliminating == True):
        self.eliminate()
      elif self.game.state == Game.GameState.Placing:
        self.place()
      elif self.game.state == Game.GameState.Moving:
        self.move()

    def menu(self):
      """Prints out the menu and gets the user's input.
        If the input is 1, it will start the game. It will check after every turn if any player has won. If a player has won, it will print who won and the menu again.
        If the input is 2, it will describe how to play the game.
        If the input is 3, it will quit the program.

        Keyword arguments:
        return -- Prints out the menu which the user can choose from.
      """
      while True:
        print('### UU-GAME ###')
        print('1. Play a new game')
        print('2. How to play')
        print('3. Quit')
        
        user_input = input('Please enter your choice from the menu and press enter: ')
        if user_input == '1':
          # Creates a new game and plays it
          self.game = Game() 
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