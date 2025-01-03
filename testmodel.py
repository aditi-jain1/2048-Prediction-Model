# HYPERPARAMETER TUNING NEEDED
# HYPERPARAMETERS INCLUDE: n = number of moves to look ahead, relative weights for heurisitics
# we can create a model that at any given instance evaluates all the four possible moves and chooses the move that is most locally optimal
# we can define the heuristic to be a combination of different heiristics as defined in heuristics.py
# instead of looking at which move would optimize the next move, we can recursively look at the next n moves (4^n combinations) to see which immediate move would optimize heuristic in the next 10 moves


import pygame
from main import *
from heuristics import *
import random

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

def create_grid():
    return [[0] * 4 for _ in range(4)]

def spawn_tile(grid):
    empty_tiles = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def print_grid(grid):
    for row in grid:
        print(row)
    print()

def compress(row):
    """Compress a row by removing zeros."""
    new_row = [num for num in row if num != 0]
    return new_row + [0] * (len(row) - len(new_row))

def merge(row):
    """Merge tiles in a row."""
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(grid):
    """Slide all rows to the left."""
    new_grid = []
    for row in grid:
        compressed_row = compress(row)
        merged_row = merge(compressed_row)
        new_grid.append(compress(merged_row))
    return new_grid

def rotate_grid(grid, times):
    """Rotate the grid clockwise."""
    for _ in range(times):
        grid = [list(row) for row in zip(*grid[::-1])]
    return grid

def move(grid, direction):
    """Move the grid in a specified direction."""
    if direction == 'up':
        grid = rotate_grid(grid, 1)
        grid = move_left(grid)
        grid = rotate_grid(grid, 3)
    elif direction == 'down':
        grid = rotate_grid(grid, 3)
        grid = move_left(grid)
        grid = rotate_grid(grid, 1)
    elif direction == 'right':
        grid = rotate_grid(grid, 2)
        grid = move_left(grid)
        grid = rotate_grid(grid, 2)
    elif direction == 'left':
        grid = move_left(grid)
    return grid

def heuristic(grid):
    weights = {
        'empty_tiles': 1.0,
        'max_tile': 1.0,
        'smoothness': 0.5,
        'monotonicity': 1.5,
        'corner_max': 5.0,
        'merge_penalty': 0.2,
    }

    score = (
        weights['empty_tiles'] * count_empty_tiles(grid)
        + weights['max_tile'] * max_tile(grid)
        + weights['smoothness'] * smoothness(grid)
        + weights['monotonicity'] * monotonicity(grid)
        + weights['corner_max'] * corner_max(grid)
        + weights['merge_penalty'] * merge_penalty(grid)
    )
    return score


def best_move(grid):
    moves = ['up', 'down', 'left', 'right']
    best_score = -1
    best_direction = None

    for move_dir in moves:
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid != grid:  # Check if the move changes the grid
            score = heuristic(new_grid)
            if score > best_score:
                best_score = score
                best_direction = move_dir         

    return best_direction

def is_game_over(grid):
    # Check for any empty tiles
    for row in grid:
        if 0 in row:
            return False

    # Check for possible merges
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols and grid[r][c] == grid[r][c + 1]:  # Check horizontally
                return False
            if r + 1 < rows and grid[r][c] == grid[r + 1][c]:  # Check vertically
                return False

    return True

def best_move_with_lookahead(grid):
    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = None

    for move_dir1 in moves:
        # Simulate the first move
        new_grid1 = move([row[:] for row in grid], move_dir1)
        if new_grid1 == grid:  # If the first move doesn't change the grid, skip it
            continue

        # Evaluate the first move's immediate score
        immediate_score = heuristic(new_grid1)

        # Look ahead to the second move
        max_second_score = -float('inf')
        for move_dir2 in moves:
            new_grid2 = move([row[:] for row in new_grid1], move_dir2)
            if new_grid2 != new_grid1:  # If the second move changes the grid
                second_score = heuristic(new_grid2)
                max_second_score = max(max_second_score, second_score)

        # Combine immediate and lookahead scores
        total_score = immediate_score + max_second_score
        if total_score > best_score:
            best_score = total_score
            best_direction = move_dir1

    return best_direction

def best_move_with_n_lookahead(grid, n):
    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = None

    for move_dir in moves:
        # Simulate the first move
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid == grid:  # If the move doesn't change the grid, skip it
            continue

        # Evaluate this move recursively up to depth `n`
        score = lookahead_score(new_grid, n - 1)
        if score > best_score:
            best_score = score
            best_direction = move_dir

    return best_direction


def lookahead_score(grid, depth):
    if depth == 0 or is_game_over(grid):
        return heuristic(grid)

    moves = ['up', 'down', 'left', 'right']
    max_score = -float('inf')

    for move_dir in moves:
        # Simulate the move
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid != grid:  # Only consider moves that change the grid
            score = lookahead_score(new_grid, depth - 1)
            max_score = max(max_score, score)

    return max_score


def main(window=WINDOW):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Create a grid representation for the AI
        grid = [[0] * COLS for _ in range(ROWS)]
        for key, tile in tiles.items():
            grid[tile.row][tile.col] = tile.value

        # Get the best move from the AI
        direction = best_move_with_n_lookahead(grid, 1)

        if direction is None:
            max_tile = max(max(row) for row in grid)
            print(max_tile)
            print("Game Over!")
            break

        # Execute the AI's move
        status = move_tiles(window, tiles, clock, direction)
        if status == "lost":
            max_tile = max(max(row) for row in grid)
            print(max_tile)
            print("Game Over!")
            break

        draw(window, tiles)

    pygame.quit()

main()