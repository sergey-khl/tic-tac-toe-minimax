from math import inf as infinity
from random import choice
from random import seed as randomseed
import platform
import time
from os import system
"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)

Sergey Khlynovskiy
CCID: khlynovs
"""


class Game():
    def __init__(self):
        """Constructs necessary attributes for the Game class.

        Arguments: self: Represents instance of Game()

        Return: None
        """
        # self.board (nested list): How the tic-tac-toe board looks.
        self.board = [
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      ]
        # self.HUMAN (int): Value to represent a human.
        self.HUMAN = -1
        # self.COMP (int): Value to represent computer.
        self.COMP = 1
        # self.state (nested list): Current state of the board.
        self.set_state(self.board)

    def __str__(self):
        """Informal string representation of Game().

        Arguments: self: Represents instance of Game().

        Return: Informal string representing Game().
        """
        return """A tic-tac-toe game with a current board of {} and state of
         {}. Where {} represents a human and {} a computer""".format(
                self.get_board(),
                self.get_state(),
                self.get_HUMAN(),
                self.get_COMP())

    def __repr__(self):
        """Formal string representation of Game().

        Arguments: self: Represents instance of Game().

        Return: Formal string representing Game().
        """
        return id(self) + self.__class__

    def set_state(self, state):
        """Setting current state of the game.

        Arguments:
        self: Represents instance of Game().
        state (nested list): Current state of the game.

        Return: None
        """
        # self.state (nested list): Construction of state.
        self.state = state

    def get_state(self):
        """Getting the current state of the game.

        Arguments:
        self: Represents instance of Game().

        Return: self.state (nested list): Current state of the game
        """
        return self.state

    def get_HUMAN(self):
        """Getting value that represents a human.

        Arguments:
        self: Represents instance of Game().

        Return: self.HUMAN (int): value that represents a human.
        """
        return self.HUMAN

    def get_COMP(self):
        """Getting value that represents a computer.

        Arguments:
        self: Represents instance of Game().

        Return: self.COMP (int): value that represents a computer.
        """
        return self.COMP

    def get_board(self):
        """Getting what the board currently looks like.

        Arguments:
        self: Represents instance of Game().

        Return: self.board (nested list): What the board looks like.
        """
        return self.board

    def evaluate(self):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(self.COMP):
            score = +1
        elif self.wins(self.HUMAN):
            score = -1
        else:
            score = 0

        return score

    def wins(self, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [self.state[0][0], self.state[0][1], self.state[0][2]],
            [self.state[1][0], self.state[1][1], self.state[1][2]],
            [self.state[2][0], self.state[2][1], self.state[2][2]],
            [self.state[0][0], self.state[1][0], self.state[2][0]],
            [self.state[0][1], self.state[1][1], self.state[2][1]],
            [self.state[0][2], self.state[1][2], self.state[2][2]],
            [self.state[0][0], self.state[1][1], self.state[2][2]],
            [self.state[2][0], self.state[1][1], self.state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(self.HUMAN) or self.wins(self.COMP)

    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        cells = []

        for x, row in enumerate(self.state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            self.state[x][y] = player
            score = self.minimax(depth - 1, -player)
            self.state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def ai_turn(self, c_choice, h_choice):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        # term (object): Instance of Console() class so its methods
        # can be used.
        term = Console()
        term.clean()
        print(f'Computer turn [{c_choice}]')
        term.render(self.get_state(), c_choice, h_choice)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, self.COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, self.COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)

    def human_turn(self, c_choice, h_choice):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        # term (object): Instance of Console() class so its methods
        # can be used.
        term = Console()
        term.clean()
        print(f'Human turn [{h_choice}]')
        term.render(self.get_state(), c_choice, h_choice)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.set_move(coord[0], coord[1], self.HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.empty_cells():
            return True
        else:
            return False

    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        else:
            return False


class Console():
    def __init__(self):
        """Constructs necessary attributes for the Console class.

        Arguments: self: Represents instance of Console()

        Return: None
        """
        # self.basic_string (string): Most simple string able to be printed
        # to console.
        self.basic_string = ""

    def get_basic_string(self):
        """Getting what the board currently looks like.

        Arguments:
        self: Represents instance of Game().

        Return: self.board (nested list): What the board looks like.
        """
        return self.basic_string

    def __str__(self):
        """Informal string representation of Console().

        Arguments: self: Represents instance of Console().

        Return: Informal string representing Console().
        """
        return """A representation of the console
         with a basic string of {}""".format(self.get_basic_string())

    def __repr__(self):
        """Formal string representation of Console().

        Arguments: self: Represents instance of Console().

        Return: Formal string representing Console().
        """
        return id(self) + self.__class__

    def clean(self):
        """
        Clears the console
        """
        # Paul Lu.  Do not clear screen to keep output human readable.
        print()
        return

        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

    def render(self, state, c_choice, h_choice):
        """
        Print the board on console
        :param state: current state of the board
        """

        chars = {
            -1: h_choice,
            +1: c_choice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in state:
            for cell in row:
                symbol = chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)


def main():
    """
    Main function that calls all functions
    """
    # game (object): Instance of the class Game.
    game = Game()
    # term (object): Instance of the class Console.
    term = Console()
    # Paul Lu.  Set the seed to get deterministic behaviour for each run.
    #       Makes it easier for testing and tracing for understanding.
    randomseed(274 + 2020)

    term.clean()

    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    term.clean()

    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(game.empty_cells()) > 0 and not game.game_over():
        if first == 'N':
            game.ai_turn(c_choice, h_choice)
            first = ''

        game.human_turn(c_choice, h_choice)
        game.ai_turn(c_choice, h_choice)

    # Game over message
    if game.wins(game.get_HUMAN()):
        term.clean()
        print(f'Human turn [{h_choice}]')
        term.render(game.get_state(), c_choice, h_choice)
        print('YOU WIN!')
    elif game.wins(game.get_COMP()):
        term.clean()
        print(f'Computer turn [{c_choice}]')
        term.render(game.get_state(), c_choice, h_choice)
        print('YOU LOSE!')
    else:
        term.clean()
        term.render(game.get_state(), c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
