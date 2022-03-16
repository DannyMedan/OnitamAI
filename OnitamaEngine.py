"""
Main driver file. In charge of handling user input and updating data
"""

from config import *
from Player import Player

import random as rand


class GameState:
    def __init__(self):
        self.board = STARTING_BOARD
        self.blue_turn = True
        self.move_log = []
        self.blue_player = Player('blue')
        self.red_player = Player('red')
        self.middle_card = self.redraw_cards()
        self.winner = None

    def get_piece_at(self, location):
        return self.board[location[0]][location[1]]

    def redraw_cards(self):
        all_cards = rand.sample(list(CARDS.keys()), 5)
        self.blue_player.set_new_cards(all_cards[0:2])
        self.red_player.set_new_cards(all_cards[2:4])
        return all_cards[4]

    def play_card(self, card_name, move):
        curr_player = self.blue_player if self.blue_turn else self.red_player
        card_index = int(curr_player.card_names[1] == card_name)
        self.middle_card = curr_player.replace_card(self.middle_card, card_index)
        self.move_piece(move)
        self.move_log.append(move)
        self.update_winner()
        self.blue_turn = not self.blue_turn

    def undo_move(self):
        # TODO: clear cyrrent player choices (card/piece)
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            print(move)
            self.blue_turn = not self.blue_turn
            player = self.blue_player if self.blue_turn else self.red_player

            card_idx = player.get_card_index_by_name(move.new_card)
            if card_idx == -1:
                self.blue_turn = not self.blue_turn  # Reset state
                raise IndexError("Lost the card from the last move!")
            player.card_names[card_idx] = move.used_card
            self.middle_card = move.new_card

            player.has_won = False  # Just in case, cancel win
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

    def move_piece(self, move):
        if self.board[move.end_row][move.end_col] != EMPTY:
            self.remove_piece(move)
        self.board[move.end_row][move.end_col] = move.piece_moved
        if move.piece_moved == BLUE_SENSEI or RED_SENSEI:
            self.is_sensei_at_enemy_dojo(move)
        self.board[move.start_row][move.start_col] = EMPTY

    def remove_piece(self, move):
        # If removed piece is Sensei, other player wins
        if move.piece_captured == BLUE_SENSEI:
            self.red_player.has_won = True
        elif move.piece_captured == RED_SENSEI:
            self.blue_player.has_won = True
        self.board[move.end_row][move.end_col] = EMPTY

    def is_sensei_at_enemy_dojo(self, move):
        if move.piece_moved == RED_SENSEI and \
                (move.end_row, move.end_col) == BLUE_DOJO:
            self.red_player.has_won = True
        elif move.piece_moved == BLUE_SENSEI and \
                (move.end_row, move.end_col) == RED_DOJO:
            self.blue_player.has_won = True

    def get_valid_moves(self, card_name, curr_location):
        curr_color, direction = (BLUE, 1) if self.blue_turn else (RED, -1)

        if self.get_piece_at(curr_location)[0] != curr_color:
            return []
        available_moves = CARDS[card_name]['MOVES']
        valid_moves = []
        for move in available_moves:
            new_location = curr_location[0] + direction * move[0], curr_location[1] + direction * move[1]
            # Check if new location is in bounds and is not occupied by a friendly piece
            if 0 <= new_location[0] < 5 and 0 <= new_location[1] < 5 and \
                    self.board[new_location[0]][new_location[1]][0] != curr_color:
                valid_moves.append(Move(curr_location, new_location, card_name, self.middle_card, self.board))
        return valid_moves

    def update_winner(self):
        if self.blue_player.has_won:
            self.winner = self.blue_player
        elif self.red_player.has_won:
            self.winner = self.red_player

    def get_cards_dict(self):
        red_cards = self.red_player.card_names
        blue_cards = self.blue_player.card_names
        cards = {
            "UPPER_LEFT": red_cards[1],
            "UPPER_RIGHT": red_cards[0],
            "LOWER_LEFT": blue_cards[0],
            "LOWER_RIGHT": blue_cards[1],
            "SIDE": self.middle_card
        }
        return cards


class Move:
    ranks_to_rows = {'1': 4, '2': 3, '3': 2, '4': 1, '5': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, used_card, new_card, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.used_card = used_card
        self.new_card = new_card
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_chess_notation_even_though_this_is_not_chess(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __repr__(self):
        return f'move: {self.get_chess_notation_even_though_this_is_not_chess()}\n' \
               f'used card: {self.used_card}\n' \
               f'take card: {self.new_card}\n' \
               f'piece moved: {self.piece_moved}\n' \
               f'piece piece captured: {None if self.piece_captured=="--" else self.piece_captured}'

    def __eq__(self, other):
        return (self.start_row == other.start_row and self.start_col == other.start_col and
                self.end_row == other.end_row and self.end_col == other.end_col and
                self.used_card == other.used_card and self.new_card == other.new_card and
                self.piece_moved == other.piece_moved and self.piece_captured == self.piece_captured)
