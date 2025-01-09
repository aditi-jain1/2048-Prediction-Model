import random
from gameLogic import (
    instantiateBoard, isGameOver, move, printBoard, 
    generateNewTile
)
from model import applyModel

def getModelInput(board, modelType):
    return applyModel(board, modelType, move, isGameOver)

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
        if board != board_before_move:
            board = generateNewTile(board)
    printBoard(board)
    print("GAME OVER")


gameloop("ai", "lookahead")