from .game import Game
from .board import Piece
from game_engine import *

import json
import sys
import os
import colorama


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

    def input_number_or_other(self, prompt, other):
      """Checks if the user's given input is an integer or inside other. If the user's input is q or Q the program will exit.
      It will keep asking the user for an input until it is valid.

      Keyword arguments:
      prompt -- The message to be printed to the user.
      other -- Array of other allowed inputs
      return -- Exits the program if the user's input is q or Q. Otherwise the users input if it is an integer.
      """
      while True:
        result = input(prompt)
        if (result == 'q' or result == 'Q'):
          sys.exit()
        if result.isdigit():
          return int(result)  
        if (result in other):
          return result

    def __init__(self):
        """When initialized, it will start the main menu."""
        self.menu()
        colorama.init(True)

    def print_board(self):
      """Prints the board and the pieces on the board. It also prints how many pieces each player has.

        Keyword arguments:
        return -- Prints out the board.
      """
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

      def print_board_ai(self):
          """Prints the board and the pieces on the board. It also prints how many pieces each player has.

            Keyword arguments:
            return -- Prints out the board.
          """
          board = [""] * 24

          reset_code = colorama.Style.RESET_ALL + colorama.Style.DIM
          black_piece = colorama.Fore.MAGENTA + 'B' + reset_code
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

          # if (self.game.state == Game.GameState.Placing):
          # print("Pieces left                Black: " + str(self.game.players[0].pieces_amount) + "                White: " + str(self.game.players[1].pieces_amount))
          pieces_presentation = [' '] * 63
          for i in range(self.game.players[0].pieces_amount):
              pieces_presentation[i] = black_piece
          for i in range(self.game.players[1].pieces_amount):
              pieces_presentation[62 - i] = white_piece
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
        """Ask the user for input on where to place, and then places there.
        Depending on the user's input, different messages will be printed out. If the user chooses a valid position, a piece will be placed.

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

        Keyword arguments:
        """
        print('Its '+ self.identify_piece(self.game.turn) + ' player\'s turn to play')
        while True:
          position = self.input_number('Which piece would you like to move?: ')-1

          result = self.game.can_move_piece_from(position)

          if (result == Game.CanMoveResults.Ok):
            valid_moves = self.game.get_valid_moves_from_position(position)
            str_valid_moves = [str(valid_move+1) for valid_move in valid_moves]
            query = "To what position would you like to move? (" + ", ".join(str_valid_moves) + " or \"back\"): "
            new_position = self.input_number_or_other(query, ["b", "B", "back", "Back"])
            if (isinstance(new_position, int)):
              new_position -= 1
              result = self.game.can_move_piece(position, new_position)
            else:
              continue

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
      elif self.game.state == Game.GameStage.Placing:
        self.place()
      elif self.game.state == Game.GameStage.Moving:
        self.move()

    def translator(self, position):
        if position == 'a1':
            return '21'
        if position == 'a4':
            return '9'
        if position == 'a7':
            return '0'
        if position == 'b2':
            return '18'
        if position == 'b4':
            return '10'
        if position == 'b6':
            return '3'
        if position == 'c3':
            return '15'
        if position == 'c4':
            return '11'
        if position == 'c5':
            return '6'
        if position == 'd1':
            return '22'
        if position == 'd2':
            return '19'
        if position == 'd3':
            return '16'
        if position == 'd5':
            return '7'
        if position == 'd6':
            return '4'
        if position == 'd7':
            return '1'
        if position == 'e3':
            return '17'
        if position == 'e4':
            return '12'
        if position == 'e5':
            return '8'
        if position == 'f2':
            return '20'
        if position == 'f4':
            return '13'
        if position == 'f6':
            return '5'
        if position == 'g1':
            return '23'
        if position == 'g4':
            return '14'
        if position == 'g7':
            return '2'

        if position == '21':
            return 'a1'
        if position == '9':
            return 'a4'
        if position == '0':
            return 'a7'
        if position == '18':
            return 'b2'
        if position == '10':
            return 'b4'
        if position == '3':
            return 'b6'
        if position == '15':
            return 'c3'
        if position == '11':
            return 'c4'
        if position == '6':
            return 'c5'
        if position == '22':
            return 'd1'
        if position == '19':
            return 'd2'
        if position == '16':
            return 'd3'
        if position == '7':
            return 'd5'
        if position == '4':
            return 'd6'
        if position == '1':
            return 'd7'
        if position == '17':
            return 'e3'
        if position == '12':
            return 'e4'
        if position == '8':
            return 'e5'
        if position == '20':
            return 'f2'
        if position == '13':
            return 'f4'
        if position == '5':
            return 'f6'
        if position == '23':
            return 'g1'
        if position == '14':
            return 'g4'
        if position == '2':
            return 'g7'

    def read_from_save_file(self):
        data = None
        ai_move = None
        with open('save_file.json', "r") as f:
            data = json.load(f)
            ai_move = data["data"]["ai_previous_move"][1]
            print(ai_move)

    def write_to_save_file(self, position):
        data = None
        # t_posistion = self.translator(position)


        with open('save_file.json', "w") as f:
            data["map"]["c_nodes"]["c4"] = "X"
            json.dump(data, f)

    def play_against_AI(self, difficulty):
        manage_game.delete_game_file()
        manage_game.create_game_file()
        self.read_from_save_file()
        run_AI(difficulty)





    def menu(self):
      """Prints out the menu and gets the user's input.
        If the input is 1, it will create and start the game. It will check after every turn if any player has won. If a player has won, it will print who won and the menu again.
        If the input is 2, it will describe how to play the game.
        If the input is 3, it will quit the program.

        Keyword arguments:
        return -- Prints out the menu which the user can choose from.
      """
      while True:
        print('### UU-GAME ###')
        print('1. Play Local')
        print('2. Play Online')
        print('3. How to play')
        print('4. Quit')
        
        user_input = input('Please enter your choice from the menu and press enter: ')
        if user_input == '1':  
          print('### LOCAL-GAME ###')
          print('1. Player 1 vs Player 2')
          print('2. Player 1 vs Computer')
          user_input_again = input('Please enter your choice from the menu and press enter: ')
          if user_input_again == '1':
            self.game = Game() 
            while(True):

              self.print_board()
              self.play()

              result = self.game.get_game_winner()

              if (result == Game.WinnerResults.BlackWon):
                self.print_board()
                print("Black has won the game")
                break
              if (result == Game.WinnerResults.WhiteWon):
                self.print_board()
                print("White has won the game")
                break
              if (result == Game.WinnerResults.Tie):
                self.print_board()
                print("It's a draw! Max amount of turns is 200")
                break
          elif user_input_again =='2':

            print('This is where we play against the AI')
            difficulty = input("Choose difficulty level (Easy - 0, Medium - 1, Hard - 2): ")
            self.play_against_AI(difficulty)
            self.read_from_save_file()



            menu_input = input('<- Back to main menu, input 3 and press enter: ')

            if menu_input == '3':
              clear_screen()

        elif user_input == '2':
          print('This is where we play Online')
          #remove these when we add stuff
          menu_input = input('<- Back to main menu, input 1 and press enter: ')
          if menu_input == '1':
            clear_screen()
        elif user_input == '3':
          clear_screen()
          self.game = Game() 
          self.print_board()
          howto_text=f"""
          This is preview of the board.
          Black players pieces are denoted by {colorama.Fore.MAGENTA}B{colorama.Style.RESET_ALL} and white players pieces are denoted by {colorama.Style.BRIGHT}W{colorama.Style.RESET_ALL}.
          The pieces you have not placed yet are represented below the board.
          
          * Both players in the game will have twelve pieces each and have twenty four places to place on the board.
          * The player who starts first will always be black.
          * The board starts empty and each player will have to place their pieces on the board taking turns.
          * You can take your opponents piece out of the board if you have a three in a row.
          * Three in a row can be done horizontally, vertically or even diagonally.
          * Once all the pieces are placed on the board, each player can move their pieces to adjacent empty places along the lines.
          * When a player has three pieces left on the board, the player can move their pieces to any empty place on the board.
          
          A player will win the game if you satisfy any of these two conditions
          1. When their opponent’s pieces are reduced to less than three.
          2. If you can surround your opponent’s pieces making them unable to move or match three in a row.
		  
          The game will end in a draw when the total amount of turns reaches 200.
          """
          print(howto_text)
          menu_input = input('<- Back to main menu, input 1 and press enter: ')
          if menu_input == '1':
            clear_screen()

        elif user_input == '4':
          return