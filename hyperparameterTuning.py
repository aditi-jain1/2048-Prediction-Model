from testmodel import *
from itertools import product
WEIGHTOPTIONS = {
        'empty_tiles': [.25, .5, 1, 2, 5],
        'max_tile': [.25, .5, 1, 2, 5],
        'smoothness': [.25, .5, 1, 5],
        'monotonicity': [1, 2, 5, 8, 10],
        'corner_max': [1, 5, 10, 20, 30],
        'merge_penalty': [.25, .5, 1, 2, 3],
    }

all_combinations = product(*WEIGHTOPTIONS.values())


def game_loop():
    grid = create_grid()
    spawn_tile(grid)  
    spawn_tile(grid)

    while not is_game_over(grid):
        move_dir = best_move(grid, WEIGHTS)

        if move_dir in ['up', 'down', 'left', 'right']:
            grid = move(grid, move_dir)  
            spawn_tile(grid)  
    max_tile = max(max(row) for row in grid)
    print(max_tile)
    print("Game Over!")
    print_grid(grid)


def game_loop_draw():
    grid = create_grid()
    tiles = {}
    r, c = spawn_tile(grid)  
    tiles[f"{r}{c}"] = Tile(2, r, c)
    r, c = spawn_tile(grid)
    tiles[f"{r}{c}"] = Tile(2, r, c)

    while not is_game_over(grid):
        move_dir = best_move(grid, WEIGHTS)

        if move_dir in ['up', 'down', 'left', 'right']:
            grid = move(grid, move_dir) 
            move_tiles(window, tiles, clock, move_dir) 
            r, c = spawn_tile(grid)
            tiles[f"{r}{c}"] = Tile(2, r, c)  
    max_tile = max(max(row) for row in grid)
    print(max_tile)
    print("Game Over!")
    print_grid(grid)


game_loop()