import random
import numpy as np
from model import applyModel
import copy
def instantiateBoard():
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(2):
        emptyTile = getEmptyTile(board)
        board[emptyTile[0]][emptyTile[1]] = 2 if random.random() < .75 else 4
    return board

def getEmptyTile(board):
    empty_tiles = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                empty_tiles.append([i, j])
    return random.choice(empty_tiles)

def printBoard(board):
    for row in board:
        print(str(row[0]) + "  " + str(row[1]) + "  " + str(row[2]) + "  " + str(row[3]))

def move(board, direction):
    board = copy.deepcopy(board)
    if direction == "left":
        return moveHelper(board)
    if direction == "up":
        rotateTimes = 3
        for i in range(rotateTimes):
            board = rotateClockwise(board)
        board = moveHelper(board)
        for i in range(4 - rotateTimes):
            board = rotateClockwise(board)
        return board
    if direction == "right":
        rotateTimes = 2
        for i in range(rotateTimes):
            board = rotateClockwise(board)
        board = moveHelper(board)
        for i in range(4 - rotateTimes):
            board = rotateClockwise(board)
        return board
    if direction == "down":
        rotateTimes = 1
        for i in range(rotateTimes):
            board = rotateClockwise(board)
        board = moveHelper(board)
        for i in range(4 - rotateTimes):
            board = rotateClockwise(board)
        return board

def isGameOver(board):
    # check if any block is empty
    for row in board:
        for col in row:
            if col == 0:
                return False
    for row in board:
        for col in range(3):
            if row[col] == row[col + 1]:
                return False
    for col in np.array(board).T:
        for row in range(3):
            if col[row] == col[row + 1]:
                return False
    return True

def moveHelper(board):
    for row in board:
        while 0 in row:
            row.remove(0)
    for row in board:
        for col in range(len(row)-1):
            if row[col] == row[col + 1]:
                row[col] = 2*row[col]
                row[col + 1] = 0
    for row in board:
        while 0 in row:
            row.remove(0)
    for row in board:
        while len(row) != 4:
            row.append(0)
    return board

def rotateClockwise(board):
    return [list(x) for x in list(zip(*board[::-1]))]

def generateNewTile(board):
    emptyTile = getEmptyTile(board)
    board[emptyTile[0]][emptyTile[1]] = 2 if random.random() < .75 else 4
    return board




