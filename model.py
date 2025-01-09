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
    if modelType == "lookahead":
        return best_move_with_lookahead(grid, WEIGHTS, move_function)

def best_move(grid, weights, move_function, isGameOver_function):
    moves = ['up', 'down', 'left', 'right']
    best_score = -10000
    best_direction = "up"

    for move_dir in moves:
        new_grid = move_function([row[:] for row in grid], move_dir)
        if new_grid != grid and not isGameOver_function(new_grid):  # Check if the move changes the grid
            score = heuristic(new_grid, weights)
            if score > best_score:
                best_score = score
                best_direction = move_dir         
    move_to_num = {"up": 1, "right": 2, "down": 3, "left": 4}
    return move_to_num[best_direction]

def best_move_with_lookahead(grid, weights, move_function):
    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = "up"

    for move_dir1 in moves:
        new_grid1 = move_function([row[:] for row in grid], move_dir1)
        if new_grid1 == grid:  # If the first move doesn't change the grid, skip it
            continue
        immediate_score = heuristic(new_grid1, weights)
        max_second_score = -float('inf')
        for move_dir2 in moves:
            new_grid2 = move_function([row[:] for row in new_grid1], move_dir2)
            if new_grid2 != new_grid1:  # If the second move changes the grid
                second_score = heuristic(new_grid2, weights)
                max_second_score = max(max_second_score, second_score)
        total_score = immediate_score + max_second_score
        if total_score > best_score:
            best_score = total_score
            best_direction = move_dir1

    move_to_num = {"up": 1, "right": 2, "down": 3, "left": 4}
    return move_to_num[best_direction]