from abc import ABCMeta, abstractmethod
import random

from PyQt5.QtGui import QMouseEvent

from utils import *
from board import Action

class Player(metaclass=ABCMeta):
    '''
    Abstract base class for players.
    :attribute player: the id of the player
    :attribute board: the board on which players acts
    :attribute is_playing: True during player's turn and False otherwise
    '''
    def __init__(self, player, board):
        '''
        Constructor of `Player`
        :param player: the id of the instanciated player
        :param board: the board on which the player shall act
        '''
        self.player = player
        self.board = board
        self.not_your_turn()

    def your_turn(self):
        '''
        Tell the player it is their turn
        '''
        self.is_playing = True

    def not_your_turn(self):
        '''
        Tell the player it is not their turn anymore
        '''
        self.is_playing = False

    def is_currently_playing(self):
        '''
        Tell whether it is the player's turn
        :return: True if it is player's turn and False otherwise
        '''
        return self.is_playing

    @abstractmethod
    def play(self, event):
        pass

class HumanPlayer(Player):
    '''
    PyQt-related class for a human player.
    '''
    def __init__(self, player, board):
        '''
        Constructor of class `HumanPlayer`
        '''
        super().__init__(player, board)

    def play(self, event, offset=None):
        '''
        Callback for Clicked event on board canvas.
        Play the demanded action on the board.
        :param event:  QMouseEvent generated when clicked on Canvas
        :param offset: None if action is placement or tuple (direction, row)
        :raise: `InvalidActionException` if player cannot play or if action is invalid
        '''
        if not self.is_currently_playing():
            raise InvalidActionException()
        if isinstance(event, QMouseEvent):
            self._play_placement(event)
        else:
            self._play_offset(offset)

    @staticmethod
    def pos2rowcol(x, y):
        '''
        Transform a (x, y) position on the canvas into a cell number.
        :param x: x position on the canvas
        :param y: y position on the canvas
        :return: tuple (row_id, col_idx)
        '''
        return y // (CELL_SIZE + OFFSET), x // (CELL_SIZE + OFFSET)

    def _play_placement(self, event):
        '''
        Convert the QMouseEvent into a playable action.
        :param event: see HumanPlayer.play
        :raise:       see HumanPlayer.play
        '''
        x = event.x()
        y = event.y()
        row, col = HumanPlayer.pos2rowcol(x, y)
        col -= 3 + self.board.get_offset()[row]
        if col < 0 or col >= 4:
            raise InvalidActionException()
        # clicked on self.board.grid[col][row]
        action = Action(row, col)
        self.board.act(action, self.player)

    def _play_offset(self, offset):
        '''
        Convert the provided tuple into a playable action.
        :param offset: see HumanPlayer.play
        :raise:        see HumanPlayer.play
        '''
        if not isinstance(offset, tuple) or len(offset) != 2:
            raise InvalidActionException()
        direction, row = offset
        action = Action(row, col=None, direction=direction)
        self.board.act(action, self.player)

class AIPlayer(Player):
    '''
    Base class for any AI Player.
    '''
    def __init__(self, player, board):
        super().__init__(player, board)
        self.other_player = PLAYER_1 if self.player == PLAYER_2 else PLAYER_2

    def your_turn(self):
        '''
        Redefine `Player.your_turn` by making AIPlayer play on the board
        '''
        self.play(event=None)

class MinimaxPlayer(AIPlayer):
    '''
    Specialised form of AI Player using minimax algorithm.
    '''
    def __init__(self, player, board):
        super().__init__(player, board)

    def play(self, event=None):
        '''
        Play the best action according to the minimax tree.
        :param event: ignored
        '''
        action = self.minimax()[0]
        self.board.act(action, self.player)

    def minimax(self, depth=2, maximize=True, penalty=0):
        '''
        Minimax tree exploration.
        :param depth:    maximum depth to explore in the tree
        :param maximize: True if selecting action maximizing score (i.e. if selecting the current player's move)
                         and False otherwise (i.e. if selecting the other player's move)
        :param penalty:  integer representing the time induced penalty
        '''
        if depth == 0:
            return (None, DRAW-penalty)
        if maximize:
            best_score = -INF
            player = self.player
        else:
            best_score = +INF
            player = self.other_player
        best_actions = []

        valid_actions = self.board.get_valid_actions(player)
        for action in valid_actions:
            self.board.act(action, player)
            winner = self.board.winner()
            if len(winner) == 0:
                score = self.minimax(depth-1, not maximize, penalty+1)[1]
            else:
                score = WIN-penalty if winner.pop() == self.player else LOSS+penalty
                score -= penalty
            self.board.undo()

            if score > best_score:
                if maximize:
                    best_score = score
                    best_actions = [(action, score)]
            elif score < best_score:
                if not maximize:
                    best_score = score
                    best_actions = [(action, score)]
            else:
                best_actions.append((action, score))
        return random.choice(best_actions)

