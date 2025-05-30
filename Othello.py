# Author: Nate Harper
# GitHub username: Miatadaddy
# Date: 6/2/2023
# Description: Final Portfolio - Othello Game

class Player:
    """class for a Player in the othello game"""

    def __init__(self, name, color):
        """initializes the player class with a name and color"""
        self._name = name
        self._color = color

    def get_name(self):
        """gets the name of player"""
        return self._name

    def get_color(self):
        """gets the color of player pieces"""
        return self._color


class Othello:
    """class for the othello game"""

    def __init__(self):
        """initializes the Othello game board """
        self._board = [['.' for _ in range(10)] for _ in range(10)]
        self._players = []
        self._board[4][4] = 'O'
        self._board[4][5] = 'X'
        self._board[5][4] = 'X'
        self._board[5][5] = 'O'
        self._players_pieces = {'black': 'X', 'white': 'O'}
        self._opponent_pieces = {'black': 'O', 'white': 'X'}

    def print_board(self):
        """prints the othello game board"""
        print('   0 1 2 3 4 5 6 7 8 9')
        print(' ' + ' *'*12)
        for row in range(10):
            print(row, '*', end=' ')
            for col in range(10):
                print(self._board[row][col], end=' ')
            print('*')
        print(' ' + ' *'*12)

    def create_player(self, player_name, color):
        """creates a player and assigns a name and color"""
        player = Player(player_name, color)
        self._players.append(player)

    def return_winner(self):
        """returns the winner of the game"""
        black_count = sum(row.count('X') for row in self._board)
        white_count = sum(row.count('O') for row in self._board)
        if black_count > white_count:
            return f"Winner is black player: {self._players[0].get_name()}"
        elif black_count < white_count:
            return f"Winner is white player: {self._players[1].get_name()}"
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """returns the available positions for a player to make"""
        available_positions = []
        for i in range(10):
            for j in range(10):
                if self._board[i][j] == '.' and self.is_valid_move(i, j, color):
                    available_positions.append((i, j))
        return available_positions

    def make_move(self, color, piece_position):
        """makes a move for a given piece of a players color"""
        row, col = piece_position
        self._board[row][col] = self._players_pieces[color]
        self.flip_pieces(row, col, color)
        return self._board

    def flip_pieces(self, row, col, color):
        """flips color of an overtaken piece on the game board"""
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            horizontal, vertical = direction
            x, y = row + horizontal, col + vertical
            flipped_pieces = []
            while 0 <= x < 10 and 0 <= y < 10 and self._board[x][y] == self._opponent_pieces[color]:
                flipped_pieces.append((x, y))
                x += horizontal
                y += vertical
            if 0 <= x < 10 and 0 <= y < 10 and self._board[x][y] == self._players_pieces[color]:
                for piece in flipped_pieces:
                    self._board[piece[0]][piece[1]] = self._players_pieces[color]

    def play_game(self, color, position):
        """plays the othello game"""
        if not self.is_valid_move(position[0], position[1], color):
            valid_moves = self.return_available_positions(color)
            print("Invalid move")
            print("Here are the valid moves:", valid_moves)
            return "Invalid move"
        self.make_move(color, position)
        self.print_board()
        if self.is_game_ended():
            print(f"Game is ended. White piece: {self.count_pieces('white')} Black piece: {self.count_pieces('black')}")
            print(self.return_winner())
        else:
            opponent_color = self.get_opponent_color(color)
            valid_moves = self.return_available_positions(opponent_color)
            if not valid_moves:
                print("No valid moves. Game is ended.")
                print(f"White piece: {self.count_pieces('white')} Black piece: {self.count_pieces('black')}")
                print(self.return_winner())

    def get_player_by_color(self, color):
        """returns the player name based on given color"""
        for player in self._players:
            if player.get_color() == color:
                return player

    def get_opponent_color(self, color):
        """returns the opponents piece color"""
        if color == "black":
            return "white"
        else:
            return "black"

    def is_valid_move(self, row, col, color):
        """defines if a move is valid on the game board"""
        if self._board[row][col] != '.':
            return False
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            horizontal, vertical = direction
            x, y = row + horizontal, col + vertical
            found_opp_piece = False
            while 0 <= x < 10 and 0 <= y < 10 and self._board[x][y] == self._opponent_pieces[color]:
                x += horizontal
                y += vertical
                found_opp_piece = True
            if 0 <= x < 10 and 0 <= y < 10 and self._board[x][y] == self._players_pieces[color] and found_opp_piece:
                return True
        return False

    def is_game_ended(self):
        """returns if the game is completed or not"""
        return len(self.return_available_positions('black')) == 0 and len(self.return_available_positions('white')) == 0

    def count_pieces(self, color):
        """counts the number of pieces on the board for given color"""
        return sum(row.count(self._players_pieces[color]) for row in self._board)