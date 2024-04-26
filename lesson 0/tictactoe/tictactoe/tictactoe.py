"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    for row in board:
        for cell in row:
            if cell == X:
                countX = countX + 1
            elif cell == O:
                countO = countO + 1

    if countX == countO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(0, len(board)):
        for cell in range(0, len(board[row])):
            if board[row][cell] == EMPTY:
                actions.add((row, cell))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    XorO = player(board)
    newBoard = copy.deepcopy(board)
    if board[action[0]][action[1]] != EMPTY:
        raise IndexError
    else: 
        newBoard[action[0]][action[1]] = XorO

    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #ROWS
    if board[0][0] == board[0][1] and board[0][0] == board[0][2]:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][0] == board[1][2]:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][0] == board[2][2]:
        return board[2][0]
    #COLUMNS
    elif board[0][0] == board[1][0] and board[0][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[0][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[0][2] == board[2][2]:
        return board[0][2]
    #DIAGONALS
    elif board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]
    else:
        return None

def helperBoardFull(board):
    """
    Returns True if board is full, False otherwise.
    """
    for row in range(0, len(board)):
        for cell in range(0, len(board[row])):
            if board[row][cell] == EMPTY:
                return False

    return True

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    elif helperBoardFull(board) == True:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None

    if player(board) == X:
        value, move = maxVal(board)
        return move
    
    elif player(board) == O:
        value, move = minVal(board)
        return move

def maxVal(board):
    if terminal(board) == True:
        return utility(board), None
    
    v = float('-inf')
    actionList = actions(board)
    move = None

    for action in actionList:
        value, moveAction = minVal(result(board, action))
        if value > v:
            move = action
            #skip steps if this is optimal
            if v == 1:
                return v, move
        
    return v, move

def minVal(board):
    if terminal(board) == True:
        return utility(board), None
    
    v = float('inf')
    actionList = actions(board)
    move = None

    for action in actionList:
        value, moveAction = maxVal(result(board, action))
        if value < v:
            move = action
            #skip steps if this is optimal
            if v == -1:
                return v, move
        
    return v, move
