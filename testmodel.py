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
WEIGHTS = {
    'empty_tiles': 10,    # Increased to encourage keeping spaces open
    'max_tile': 2.0,      # Reward higher values
    'smoothness': 4.0,    # Increased to encourage mergeable tiles
    'monotonicity': 8.0,  # Reduced but still important
    'corner_max': 5.0,    # Keeping high values in corners
    'merge_penalty': 1.0  # Reduced penalty for different adjacent tiles
}

def create_grid():
    return [[0] * 4 for _ in range(4)]

def spawn_tile(grid):
    empty_tiles = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        val =  2 if random.random() < 0.9 else 4
        grid[r][c] = val
    return r, c, val

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

def snake_pattern_bonus(grid):
    """Reward snake-like patterns that are good for merging"""
    score = 0
    # Check snake pattern: top row left to right, second row right to left, etc.
    pattern_multiplier = 1.0
    for r in range(len(grid)):
        row = grid[r] if r % 2 == 0 else grid[r][::-1]
        prev = None
        for val in row:
            if prev is not None and val != 0:
                if val >= prev:
                    score += math.log2(val) * pattern_multiplier
            prev = val
        pattern_multiplier *= 0.5  # Lower rows are less important
    return score

def heuristic(grid, weights=WEIGHTS):

    normalization = {
        'empty_tiles': 0.1,   # Scale for 0-16 empty tiles
        'max_tile': 0.001,    # Scale for potentially large numbers
        'smoothness': 0.1,    # Adjusted for typical smoothness values
        'monotonicity': 0.5,  # Scale for 0-8 monotonic lines
        'corner_max': 0.001,  # Scale for high value tiles
        'merge_penalty': 0.1  # Scale for typical penalty values
    }   

    score = (
        weights['empty_tiles'] * normalization['empty_tiles'] * count_empty_tiles(grid)
        + weights['max_tile'] * normalization['max_tile'] * max_tile(grid)
        + weights['smoothness'] * normalization['smoothness'] * smoothness(grid)
        + weights['monotonicity'] * normalization['monotonicity'] * monotonicity(grid)
        + weights['corner_max'] * normalization['corner_max'] * corner_max(grid)
        + weights['merge_penalty'] * normalization['merge_penalty'] * merge_penalty(grid)
    )

    snake_bonus = snake_pattern_bonus(grid) * 2.0
    max_val = max_tile(grid)
    if max_val > 64:  # Only care about position for higher values
        if grid[0][0] != max_val and grid[0][3] != max_val:  # If max value isn't in top corners
            score *= 0.8  # Apply penalty
    
    return score + snake_bonus

    '''
    print(weights['empty_tiles'] * normalization['empty_tiles'] * count_empty_tiles(grid)
        , weights['max_tile'] * normalization['max_tile'] * max_tile(grid)
        , weights['smoothness'] * normalization['smoothness'] * smoothness(grid)
        , weights['monotonicity'] * normalization['monotonicity'] * monotonicity(grid)
        , weights['corner_max'] * normalization['corner_max'] * corner_max(grid)
        , weights['merge_penalty'] * normalization['merge_penalty'] * merge_penalty(grid))
    '''
    return score


def best_move(grid, weights=WEIGHTS):
    moves = ['up', 'down', 'left', 'right']
    best_score = -10000
    best_direction = None

    for move_dir in moves:
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid != grid:  # Check if the move changes the grid
            score = heuristic(new_grid, weights)
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

def best_move_with_lookahead(grid, weights=WEIGHTS):
    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = None

    for move_dir1 in moves:
        # Simulate the first move
        new_grid1 = move([row[:] for row in grid], move_dir1)
        if new_grid1 == grid:  # If the first move doesn't change the grid, skip it
            continue

        # Evaluate the first move's immediate score
        immediate_score = heuristic(new_grid1, weights)

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

def best_move_with_n_lookahead(grid, n, weights=WEIGHTS):
    moves = ['up', 'down', 'left', 'right']
    best_score = -float('inf')
    best_direction = None

    for move_dir in moves:
        # Simulate the first move
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid == grid:  # If the move doesn't change the grid, skip it
            continue

        # Evaluate this move recursively up to depth `n`
        score = lookahead_score(new_grid, n - 1, weights)
        if score > best_score:
            best_score = score
            best_direction = move_dir

    return best_direction


def lookahead_score(grid, depth, weights=WEIGHTS):
    if depth == 0 or is_game_over(grid):
        return heuristic(grid, weights)

    moves = ['up', 'down', 'left', 'right']
    max_score = -float('inf')

    for move_dir in moves:
        # Simulate the move
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid != grid:  # Only consider moves that change the grid
            score = lookahead_score(new_grid, depth - 1, weights)
            max_score = max(max_score, score)

    return max_score


def best_move_with_expectimax(grid, depth=3):
    """Implement expectimax search to consider random tile spawns"""
    moves = ['up', 'down', 'left', 'right']
    best_score = float('-inf')
    best_move = None
    
    for move_dir in moves:
        new_grid = move([row[:] for row in grid], move_dir)
        if new_grid != grid:
            score = expectimax(new_grid, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = move_dir
                
    return best_move

def expectimax(grid, depth, is_max):
    if depth == 0 or is_game_over(grid):
        return heuristic(grid)
    
    if is_max:
        # AI's turn - try all moves
        max_score = float('-inf')
        moves = ['up', 'down', 'left', 'right']
        for move_dir in moves:
            new_grid = move([row[:] for row in grid], move_dir)
            if new_grid != grid:
                score = expectimax(new_grid, depth-1, False)
                max_score = max(max_score, score)
        return max_score if max_score != float('-inf') else improved_heuristic(grid)
    else:
        # Random tile spawn turn - average all possibilities
        empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
        if not empty_cells:
            return heuristic(grid)
            
        avg_score = 0
        for i, j in empty_cells:
            # Try spawning a 2 (90% probability)
            new_grid = [row[:] for row in grid]
            new_grid[i][j] = 2
            score_with_2 = expectimax(new_grid, depth-1, True)
            
            # Try spawning a 4 (10% probability)
            new_grid[i][j] = 4
            score_with_4 = expectimax(new_grid, depth-1, True)
            
            # Weighted average based on spawn probabilities
            avg_score += (0.9 * score_with_2 + 0.1 * score_with_4) / len(empty_cells)
            
        return avg_score

def main(window=WINDOW):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()
    grid = get_grid(tiles)
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Create a grid representation for the AI
        grid = get_grid(tiles)

        # Get the best move from the AI
        direction = best_move_with_expectimax(grid, depth=3)
        if direction is None:
            max_tile = max(max(row) for row in grid)
            print(max_tile)
            print("Game Over!")
            break

        # Execute the AI's move
        move_tiles(window, tiles, clock, direction)
        end_move(tiles)

        draw(window, tiles)

    pygame.quit()

main()
