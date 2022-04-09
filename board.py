from utils import *

class Action:
    '''
    Action to be played on the board.
    :attribute row: row_idx to play the action on
    :attribute col: None if offset or col_idx to play on
    :attribute direction: None if placement or either LEFT or RIGHT
    '''
    def __init__(self, row, col=None, direction=None):
        '''
        Constructor of class `Action`.
        :param row: row_idx to play the action on
        :param col: None if offset or col_idx to play on
        :param direction: None if placement or either LEFT or RIGHT
        '''
        self.row = row
        self.col = col
        self.direction = direction
        if not (self.direction in (None, LEFT, RIGHT) and \
                self.row in range(4) and \
                (self.col in range(4) or self.col is None) and \
                col is not None or direction is not None):
            raise InvalidActionException()

    def is_offset(self):
        '''
        :return: True if action is an offset
        '''
        return not self.is_placement()

    def is_placement(self):
        '''
        :return: True if action is a placement
        '''
        return self.direction is None

    def __eq__(self, other):
        return self.row == other.row and \
               self.col == other.col and \
               self.direction == other.direction

    def __str__(self):
        if self.is_offset():
            return f'{"-+"[(self.direction+1)//2]}{self.row}'
        else:
            return f'{"4321"[self.row]}{"ABCD"[self.col]}'

    def __repr__(self):
        return str(self)


class Board:
    '''
    Game board representing the state of the game.
    :attribute offset: list of integers representing the offset of each row
    :attribute grid: list of list (matrix) with the players' colors
    :attribute last_actions: stack of actions taken so far
    '''
    def __init__(self):
        '''
        Constructor of class `Board`
        '''
        self.reset()

    def reset(self):
        '''
        Reset the board by re-centering all rows and emptying all cells.
        '''
        self.offset = [0 for y in range(4)]
        self.grid = [[0 for x in range(4)] for y in range(4)]
        self.last_actions = list()

    def get_grid(self):
        '''
        Get the current state of the board
        '''
        return self.grid

    def get_offset(self):
        '''
        Get the current offset
        '''
        return self.offset

    def get_valid_actions(self, player):
        '''
        Gives all possible actions on the current state of the board.
        :param player: the id of the player who wants to take an action
        :return: list of actions
        '''
        columns = rows = range(4)
        # all possible placements
        actions = [Action(row, col) for col in columns for row in rows if self.grid[row][col] != player]
        # and all possible offsets
        actions += [Action(row, None, direction=direction) for row in rows for direction in (LEFT, RIGHT) \
                        if -3 <= self.offset[row]+direction <= +3]
        # Remove the inverse of the last action taken
        if self.last_actions:
            last_action = self.last_actions[-1][0]
            if last_action.is_placement():
                if last_action in actions:
                    actions.remove(last_action)
            else:
                actions.remove(Action(last_action.row, col=None, direction=-last_action.direction))
        return actions

    def act(self, action, player):
        '''
        Execute an action on the board.
        :param action: instance of the class `Action` containing the action to be executed
        :param player: the id of the player who wants to play
        :raise: `InvalidActionException` if action is not valid
        '''
        if action not in self.get_valid_actions(player):
            raise InvalidActionException()
        if action.is_placement():
            self.last_actions.append((action, self.grid[action.row][action.col]))
            self.grid[action.row][action.col] = player
        else:
            self.last_actions.append((action, None))
            self.offset[action.row] += action.direction

    def undo(self):
        '''
        Undo the last action taken.
        '''
        last_action, color = self.last_actions.pop()
        if last_action.is_placement():
            self.grid[last_action.row][last_action.col] = color
        else:
            self.offset[last_action.row] -= last_action.direction

    @staticmethod
    def find_all_winners(dico):
        '''
        Get the list of potential winners given in the values of dico
        :param dico: a dict whose keys are ignored and whose values are lists of integers
        '''
        return list(map(set, filter(lambda seq: len(seq) == 4 and 0 not in seq, dico.values())))

    def winner(self):
        '''
        Find the winner of the current board.
        :return: a (possibly empty) list of winners.
        '''
        min_index = max(self.offset)
        max_index = min(self.offset) + 3
        columns = {i: list() for i in range(min_index, max_index+1)}
        rows = {i: self.grid[i] for i in range(4)}
        diagonals, skew_diagonals = self.extract_diagonals()

        for col in range(min_index, max_index+1):
            for row in range(4):
                columns[col].append(self.grid[row][col-self.offset[row]])

        potential_winners = \
            Board.find_all_winners(columns) + \
            Board.find_all_winners(rows) + \
            Board.find_all_winners(diagonals) + \
            Board.find_all_winners(skew_diagonals)

        winners = list({seq.pop() for seq in potential_winners if len(seq) == 1 and seq != {0}})
        return winners

    def extract_diagonals(self):
        '''
        Isolate all the k-diagonals and k-skew-diagonals on the board.
        :return: a tuple (diagonals, skew_diagonals) of dictionaries.

        For k in range(offset[0], offset[0]+4):
            diagonals[k] is a list containing the k-diagonal
            skew_diagonals[k] is a list containing the k-skew-diagonal
        Note that the length of these diagonals lies between 1 and 4.
        '''
        min_index = self.offset[0]
        max_index = 3 + self.offset[0]
        diagonals = {i: list() for i in range(min_index, max_index + 1)}
        skew_diagonals = {i: list() for i in range(min_index, max_index + 1)}

        for col in range(min_index, max_index + 1):
            for i in range(4):
                for j in range(4):
                    # Are we currently on the appropriate diagonal
                    if j + self.offset[i] == col + i:
                        diagonals[col].append(self.grid[i][j])
                    # Are we currently on the appropriate skew-diagonal
                    if j + self.offset[i] == col - i:
                        skew_diagonals[col].append(self.grid[i][j])
        return diagonals, skew_diagonals

