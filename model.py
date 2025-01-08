from heuristics import *
import numpy as np

WEIGHTS = {'empty_tiles': 1, 
            'max_tile': 1, 
            'smoothness': 1, 
            'monotonicity': 1, 
            'corner_max': 1, 
            'merge_penalty': 1,
            'snake_pattern': 1}

def applyModel(grid, modelType, move_function, isGameOver_fucntion):
    if modelType == "best_move":
        return best_move(grid, WEIGHTS, move_function, isGameOver_fucntion)


def best_move(grid, weights, move_function, isGameOver_function):
    moves = ['up', 'down', 'left', 'right']
    best_score = -10000
    best_direction = None

    for move_dir in moves:
        new_grid = move_function([row[:] for row in grid], move_dir)
        if new_grid != grid and not isGameOver_function(new_grid):  # Check if the move changes the grid
            score = heuristic(new_grid, weights)
            if score > best_score:
                best_score = score
                best_direction = move_dir         
    move_to_num = {"up": 1, "right": 2, "down": 3, "left": 4}
    return move_to_num[best_direction]
