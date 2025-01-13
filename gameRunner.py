import random
from gameLogic import (
    instantiateBoard, isGameOver, move, printBoard, 
    generateNewTile
)
from model import applyModel

def getModelInput(board, modelType):
    return applyModel(board, modelType, move, isGameOver)

def getModelInputTesting(board, modelType, weights):
    return applyModel(board, modelType, move, isGameOver, weights)

def gameloop(gameType, modelType):
    board = instantiateBoard()
    while not isGameOver(board):
        printBoard(board)
        print("1 = UP | 2 = RIGHT | 3 = DOWN | 4 = LEFT")
        if gameType == "player":
            playerInput = input("Enter move: ")
        if gameType == "ai":
            playerInput = getModelInput(board, modelType)
        if gameType == "random":
            playerInput = random.choice([1, 2, 3, 4])
        moves = {1: "up", 2: "right", 3: "down", 4: "left"}
        board_before_move = [row[:] for row in board]
        board = move(board, moves[int(playerInput)])
        print(moves[int(playerInput)])
        if board != board_before_move:
            board = generateNewTile(board)
    printBoard(board)
    print("GAME OVER")

def gameloop_testing(gameType, modelType, weights):
    board = instantiateBoard()
    while not isGameOver(board):
        if gameType == "player":
            playerInput = input("Enter move: ")
        if gameType == "ai":
            playerInput = getModelInputTesting(board, modelType, weights)
        if gameType == "random":
            playerInput = random.choice([1, 2, 3, 4])
        moves = {1: "up", 2: "right", 3: "down", 4: "left"}
        board_before_move = [row[:] for row in board]
        board = move(board, moves[int(playerInput)])
        if board != board_before_move:
            board = generateNewTile(board)
    return max([max(row) for row in board])

#Uncomment line below to run game
w1 = {'empty_tiles': 1, 'max_tile': 1.5, 'smoothness': 0.5, 'monotonicity': 1, 'corner_max': 0.5, 'merge_penalty': 1, 'snake_pattern': 0.5}
w2 = {'empty_tiles': 1, 'max_tile': 1, 'smoothness': 1, 'monotonicity': 1, 'corner_max': 1, 'merge_penalty': 1, 'snake_pattern': 1}

#gameloop("ai", "expectimax")