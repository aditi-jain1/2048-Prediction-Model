from heuristics import *
import numpy as np
import copy
import random

WEIGHTS = {'empty_tiles': 1, 'max_tile': 1.5, 'smoothness': 0.5, 'monotonicity': 1, 'corner_max': 0.5, 'merge_penalty': 1, 'snake_pattern': 0.5}

N = 4
DEPTH = 4
def applyModel(grid, modelType, move_function, isGameOver_fucntion, weights=WEIGHTS):
    if modelType == "best_move":
        return best_move2(grid, weights, move_function, isGameOver_fucntion)
    if modelType == "lookahead":
        return best_move_with_lookahead(grid, weights, move_function)
    if modelType == "nlookahead":
        return best_move_with_n_lookahead(grid, N, weights, move_function, isGameOver_fucntion)
    if modelType == "expectimax":
        move_map = {'up': 1, 'right': 2, 'down': 3, 'left': 4}
        valid_moves = []
        for move in ['up', 'down', 'left', 'right']:
            test_grid = copy.deepcopy(grid)
            new_grid = move_function(test_grid, move)
            if new_grid != test_grid:
                valid_moves.append(move)
        if not valid_moves:
            return random.choice([1, 2, 3, 4])
        best_move, _ = expectimax(grid, weights, DEPTH, move_function, isGameOver_fucntion, True)
        if best_move is None:
            print("No move found by expectimax, choosing random valid move")
            return move_map[random.choice(valid_moves)]
        return move_map[best_move]

def best_move2(grid, weights, move_function, isGameOver_function):
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

def best_move_with_n_lookahead(grid, n, weights, move_function, isGameOver_fucntion):
    def lookahead_score(grid, depth, weights=WEIGHTS):
        if depth == 0 or isGameOver_fucntion(grid):
            return heuristic(grid, weights)
        moves = ['up', 'down', 'left', 'right']
        max_score = -float('inf')
        for move_dir in moves:
            # Simulate the move
            new_grid = move_function([row[:] for row in grid], move_dir)
            if new_grid != grid:  # Only consider moves that change the grid
                score = lookahead_score(new_grid, depth - 1, weights)
                max_score = max(max_score, score)
        return max_score

    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = None

    for move_dir in moves:
        new_grid = move_function([row[:] for row in grid], move_dir)
        if new_grid == grid:  
            continue
        score = lookahead_score(new_grid, n - 1, weights)
        if score > best_score:
            best_score = score
            best_direction = move_dir

    move_to_num = {"up": 1, "right": 2, "down": 3, "left": 4}
    return move_to_num[best_direction]

def expectimax(grid, weights, depth, move_function, isGameOver_function, is_player_turn):
    def get_empty_cells(grid):
        empty = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    empty.append((i, j))
        return empty
    def get_all_possible_new_tiles(grid):
        empty_cells = get_empty_cells(grid)
        possibilities = []
        cell_prob = 1 / len(empty_cells)
        for (i, j) in empty_cells:
            new_grid_2 = copy.deepcopy(grid)
            new_grid_2[i][j] = 2
            new_grid_2_prob = cell_prob * .75
            possibilities.append((new_grid_2, new_grid_2_prob))

            new_grid_4 = copy.deepcopy(grid)
            new_grid_4[i][j] = 4
            new_grid_4_prob = cell_prob * .25
            possibilities.append((new_grid_4, new_grid_4_prob))
        return possibilities
    if depth == 0:
        return None, heuristic(grid, weights)
    if is_player_turn:
        moves = ['up', 'down', 'left', 'right']
        best_score = float('-inf')
        best_move = None
        for move in moves:
            new_grid = move_function([row[:] for row in grid], move)
            if new_grid == grid:
                continue
            _, score = expectimax(new_grid, weights, depth - 1, move_function, isGameOver_function, False)

            if score > best_score:
                best_score = score
                best_move = move
        if best_move is None:
            return None, -10000
        return best_move, best_score
    else:
        possibilities = get_all_possible_new_tiles(grid)
        if not possibilities:  # Game over
            return None, heuristic(grid, weights)
        expected_score = 0
        for new_grid, probability in possibilities:
            _, score = expectimax(new_grid, weights, depth - 1, move_function, isGameOver_function, True)
            expected_score += score * probability
        return None, expected_score

