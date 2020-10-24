from .game import Game
from .game import *
from .board import Piece
from game_engine import *


import json
import sys
import os
import colorama

class AI_Player:
    def __init__(self, game):
        self.game = game


    def ai_eliminate(self, eliminate_position):
        """ Takes the translated AIs position (int) of the piece the AI wanted
            to eliminate and eliminate the piece on the players board.
        """
        position = eliminate_position
        print("Position_ai: " + str(position))
        self.game.eliminate_piece(position)

    def ai_place(self, ai_position):
        """ Takes the translated AIs position (int) to the piece the AI places and
            places it on the players board.
        """
        while True:
            position = ai_position
            print("Pos " + str(position))
            self.game.place_piece(self.game.turn, position)
            break

    def ai_move(self, ai_position_from, ai_position_to):
        """ Takes the translated AIs positions (ints) on where the AI moved from
            and where the AI moved to and moves the piece on the players board.
        """
        old_position = ai_position_from
        new_position = ai_position_to
        self.game.move_piece(old_position, new_position)

    def ai_eliminating(self):
        data = None
        eliminate_state = None
        with open('save_file.json', "r") as f:
            data = json.load(f)
            eliminate_state = data["data"]["ai_previous_move"][2]
            print("Eli - state: " + str(eliminate_state))
            return eliminate_state

    def ai_play(self):
        """ This function translates the moves the AI made on its board and
            implements them on the players board as well. This is the function
            to call after the AIs turn.
        """


        if self.game.state == Game.GameStage.Placing:
            ai_place = self.ai_moves_to()
            print("Tjabba: " + str(ai_place))
            self.ai_place(self.translator(str(ai_place)))
            if (self.ai_eliminating() == True):
                wants_to_eliminate = self.ai_wants_to_eliminate()
                self.ai_eliminate(self.translator(wants_to_eliminate))
        elif self.game.state == Game.GameStage.Moving:
            ai_place = self.ai_moves_to()
            ai_move = self.ai_moves_from()
            self.ai_move(self.translator(str(ai_move)), self.translator(str(ai_place)))
            if self.ai_eliminating():
                wants_to_eliminate = self.ai_wants_to_eliminate()
                self.ai_eliminate(self.translator(wants_to_eliminate))

    def translator(self, position):
        """ This function takes a position (string) and returnes the corresponding
            position on the other board. Player -> AI and AI -> Player.
            The positions corresponding on the players board are retuned as int
            and the positions corresponding on the AIs board are returned as strings.
        """
        print("in_trans :" + str(position) )
        if position == 'a1':
            return 21
        if position == 'a4':
            return 9
        if position == 'a7':
            return 0
        if position == 'b2':
            return 18
        if position == 'b4':
            return 10
        if position == 'b6':
            return 3
        if position == 'c3':
            return 15
        if position == 'c4':
            return 11
        if position == 'c5':
            return 6
        if position == 'd1':
            return 22
        if position == 'd2':
            return 19
        if position == 'd3':
            return 16
        if position == 'd5':
            return 7
        if position == 'd6':
            return 4
        if position == 'd7':
            return 1
        if position == 'e3':
            return 17
        if position == 'e4':
            return 12
        if position == 'e5':
            return 8
        if position == 'f2':
            return 20
        if position == 'f4':
            return 13
        if position == 'f6':
            return 5
        if position == 'g1':
            return 23
        if position == 'g4':
            return 14
        if position == 'g7':
            return 2

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

    def ai_moves_to(self):
        """ This function reads where the AI moved to, in the save_file.json
            in ai_previous_move[1] and returns the position (string).
        """
        data = None
        ai_move = None
        with open('save_file.json', "r") as f:
            data = json.load(f)
            ai_move = data["data"]["ai_previous_move"][1]
            return ai_move

    def ai_moves_from(self):
        """ This function reads where the AI moved from, in the save_file.json
            in ai_previous_move[0] and returns the position (string).
        """
        data = None
        ai_move = None
        with open('save_file.json', "r") as f:
            data = json.load(f)
            ai_move = data["data"]["ai_previous_move"][0]
            return ai_move

    def ai_wants_to_eliminate(self):
        """ This function will return the position (string) of the piece the
            AI eliminates.
        """
        data = None
        ai_eliminate_piece = None
        with open('save_file.json', "r") as f:
            data = json.load(f)
            ai_eliminate_piece = data["data"]["ai_previous_move"][3]
            print("AI_eli_piece"+ai_eliminate_piece)
            return ai_eliminate_piece

    def player_to_ai_board(self):
        """ This function implements the changes on the players board on to
            the AIs board as well. This is the function to call after the
            players turn.
        """
        data = None
        player = self.game.get_player_from_piece(self.game.turn)
        if self.game.ai_eliminated:
            eliminate = player.previous_move[2]
            t_eliminate = self.translator(str(eliminate))
            print("T-el" + t_eliminate)
            self.write_to_save_file(t_eliminate, "-")
            self.game.ai_eliminated = False

        elif self.game.state == Game.GameStage.Placing:
            move_to = player.previous_move[1]
            t_move_to = self.translator(str(move_to))
            print(t_move_to)
            print(move_to)
            self.write_to_save_file(t_move_to, "X")
            #self.decrease_markers_left()

        elif self.game.state == Game.GameStage.Moving:
            move_from = player.previous_move[0]
            move_to = player.previous_move[1]
            t_move_from = self.translator(str(move_from))
            t_move_to = self.translator(str(move_to))
            self.write_to_save_file(t_move_from, "-")
            self.write_to_save_file(t_move_to, "X")

    def write_to_save_file(self, position, type):
        """ This function takes the transladet position (string) that should get
            changed on the AIs board and the type that the position should be
            change to.

            Example: position = "a7", type = "-" if the player eliminated
            the AIs piece on position 0 (the player sees that as position 1).
        """
        data = None
        print(position)
        node = str(position[0]) + "_nodes"
        print(node)
        with open('save_file.json', "r") as f:
            data = json.load(f)
            f.close()
        with open('save_file.json', "w") as f:
            data["map"][node][position] = str(type)
            json.dump(data, f)
            f.close()

    def the_ai_turn(self, difficulty):
        self.player_to_ai_board()
        run_AI(difficulty)
        self.ai_play()