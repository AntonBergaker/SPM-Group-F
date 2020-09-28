from game import Game
import sys
from board import Piece

class CommandLine:
    game = None

    def __init__(self, game : Game):
        self.game = game
        self.menu()

    def print_board(self):
      board = [""] * 24
      for x in range(24):
        if (self.game.board[x] == Piece.Empty):
          board[x] = ' '
        elif (self.game.board[x] == Piece.Black):
          board[x] = 'B'
        else:
          board[x] = 'W'

      print("  1                             2                            3")
      print("  "+board[0]+"-----------------------------"+board[1]+"-----------------------------"+board[2])
      print("  |⟍                            |                           ⟋ |")
      print("  |  ⟍                          |                         ⟋   |")
      print("  |    ⟍                        |                       ⟋     |")
      print("  |      ⟍ 4                  5 |                    6⟋       |")
      print("  |        "+board[3]+"--------------------"+board[4]+"--------------------"+board[5]+"        |")
      print("  |        | ⟍                  |                 ⟋  |        |")
      print("  |        |   ⟍                |               ⟋    |        |")
      print("  |        |     ⟍              |             ⟋      |        |")
      print("  |        |       ⟍ 7        8 |          9⟋        |        |")
      print("  |        |         "+board[6]+"----------"+board[7]+"----------"+board[8]+"         |        |")
      print("  |        |         |                     |         |        |")
      print("  |        |         |                     |         |        |")
      print("10|     11 |      12 |                  13 |      14 |     15 |")
      print("  "+board[9]+"--------"+board[10]+"---------"+board[11]+"                     "+board[12]+"---------"+board[13]+"--------"+board[14])
      print("  |        |         |                     |         |        |")
      print("  |        |      16 |         17       18 |         |        |")
      print("  |        |         "+board[15]+"----------"+board[16]+"----------"+board[17]+"         |        |")
      print("  |        |       ⟋            |            ⟍       |        |")
      print("  |        |     ⟋              |              ⟍     |        |")
      print("  |        |   ⟋                |                ⟍   |        |")
      print("  |     19 | ⟋               20 |                  ⟍ | 21     |")
      print("  |        "+board[18]+"--------------------"+board[19]+"--------------------"+board[20]+"        |")
      print("  |      ⟋                      |                      ⟍      |")
      print("  |    ⟋                        |                        ⟍    |")
      print("  |  ⟋                          |                          ⟍  |")
      print("22|⟋                         23 |                          24⟍|")
      print("  "+board[21]+"-----------------------------"+board[22]+"-----------------------------"+board[23]+"  ")


    def identify_piece(self, turn):
      if turn == 1:
        return str('Black')
      if turn == 2:
        return str('White')

    def eliminate(self):
      turn = self.game.turn
      self.print_board()
      print(self.identify_piece(turn) + ' player has three in a row!')
      position = int(input('Choose a piece to eliminate: '))-1

      if self.game.eliminate_piece(position) == False :
        print('Can not eliminate piece! Try again!')
        self.eliminate()
              
      else :
        self.game.eliminate_piece(position)

    def place_piece_on_board(self):
      turn = self.game.turn
      print('Its '+ self.identify_piece(turn) + ' player turn to play')
      position = int(input('Choose a spot: '))-1

      result = self.game.place_piece(self.game.turn, position)
      if result == 1:
        self.game.place_piece(self.game.turn, position)
      
      if result == -1:
        position = int(input('Could not place! Choose a free spot: '))-1

      if result == 2:
        self.eliminate()

    def play(self):
      turn = self.game.turn
      print('Its '+ self.identify_piece(turn) + ' player turn to play')
      user_input = int(input('Input [1] for placing a piece, input [2] for moving a piece: '))
      
      if user_input == 1:
        turn = self.game.turn
        print('Its '+ self.identify_piece(turn) + ' player turn to play')
        position = int(input('Choose a spot: '))-1

        result = self.game.place_piece(self.game.turn, position)
        if result == 1:
          self.game.place_piece(self.game.turn, position)
      
        if result == -1:
          position = int(input('Could not place! Choose a free spot: '))-1

        if result == 2:
          self.eliminate()

      if user_input == 2:
        position = int(input('Which piece would you like to move?: '))-1
        new_position = int(input('To what position would you like to move?: '))-1
        result = self.game.move_piece(position, new_position)
        if result == 1:
          self.game.move_piece(position, new_position)
        if result == -1:
          print('Invalid move! Please, try again ')
          position = int(input('Which piece would you like to move?: '))-1
          new_position = int(input('On what position would you like to move your piece?: '))-1
          self.game.move_piece(position, new_position)
        if result == 2:
          self.eliminate()

    def menu(self):
      print('### UU-GAME ###')
      print('1. Play a new game')
      print('2. How to play')
      print('3. Quit')
    
      user_input = input('Please enter your choice from the menu and press enter: ')
      if user_input in ['1', '2']:

        if user_input == '1':  
          turn = self.game.turn
          while(turn <= 20):
            self.print_board()
            #self.place_piece_on_board()
            self.play()
            turn = turn + 1

        if user_input == '2':
          print("\033c")
          print("This is how you play....")
          print("TBA")
          menu_input = input('<- Back to main menu, input 1 and press enter: ')
          if menu_input == '1':
            print("\033c")
          self.menu();  

        if user_input == '3':
          exit()
                
      else:
        self.menu()
