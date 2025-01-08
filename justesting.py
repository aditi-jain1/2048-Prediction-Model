from testmodel import *
from itertools import product

WEIGHTOPTIONS = {
        'empty_tiles': [0, .25],
        'max_tile': [0, .5, 1, 5],
        'smoothness': [0, 1, 5],
        'monotonicity': [0, 5, 10],
        'corner_max': [10, 20, 30],
        'merge_penalty': [0, .5, 2],
    }
WEIGHTS ={'empty_tiles': 0, 'max_tile': 0.5, 'smoothness': 1, 'monotonicity': 0, 'corner_max': 30, 'merge_penalty': 0}

all_combinations = list(product(*WEIGHTOPTIONS.values()))
print(len(all_combinations))
print(all_combinations[1])

def simulate_game(weights):
    grid = create_grid()
    spawn_tile(grid)  
    spawn_tile(grid)

    while not is_game_over(grid):
        print_grid(grid)
        move_dir = best_move(grid, weights)

        if move_dir in ['up', 'down', 'left', 'right']:
            grid = move(grid, move_dir)  
            spawn_tile(grid)  
    max_tile = max(max(row) for row in grid)
    return max_tile

simulate_game([ [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9] ])