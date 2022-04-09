##### Define some constants

########## Display constants
CELL_SIZE = 100
OFFSET = 10
WIDTH = 10*CELL_SIZE + 11*OFFSET
HEIGHT = 4*CELL_SIZE + 5*OFFSET

########## Set to True to have debug display on the Canvas
GRID_DEBUG = False

########## Game related constants
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
LEFT = -1
RIGHT = +1

INF = float('inf')

########## minimax rewards
WIN  = +10
DRAW =   0
LOSS = -10
# Note: reward is > 1 so that winning quickly is favored over winning later

class InvalidActionException(Exception):
    '''
    Exception raised when an invalid action is either created or played
    '''
    def __init__(self, msg=''):
        super().__init__(msg)
