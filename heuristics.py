import math
def count_empty_tiles(grid):
    return sum(row.count(0) for row in grid)

def max_tile(grid):
    return max(max(row) for row in grid)

def smoothness(grid):
    smoothness_score = 0
    for r in range(len(grid)):
        for c in range(len(grid[0]) - 1):  # Compare horizontally
            smoothness_score -= abs(grid[r][c] - grid[r][c + 1])
    for r in range(len(grid) - 1):  # Compare vertically
        for c in range(len(grid[0])):
            smoothness_score -= abs(grid[r][c] - grid[r + 1][c])
    return smoothness_score

def monotonicity(grid):
    mono_score = 0
    for row in grid:
        if all(row[i] <= row[i + 1] for i in range(len(row) - 1)):
            mono_score += 1
        elif all(row[i] >= row[i + 1] for i in range(len(row) - 1)):
            mono_score += 1
    for col in zip(*grid):  # Columns as rows
        if all(col[i] <= col[i + 1] for i in range(len(col) - 1)):
            mono_score += 1
        elif all(col[i] >= col[i + 1] for i in range(len(col) - 1)):
            mono_score += 1
    return mono_score

def corner_max(grid):
    max_val = max_tile(grid)
    corners = [grid[0][0], grid[0][-1], grid[-1][0], grid[-1][-1]]
    return max_val if max_val in corners else 0

def merge_penalty(grid):
    penalty = 0
    for r in range(len(grid)):
        for c in range(len(grid[0]) - 1):  # Check horizontally
            if grid[r][c] != grid[r][c + 1]:
                penalty += 1
    for r in range(len(grid) - 1):  # Check vertically
        for c in range(len(grid[0])):
            if grid[r][c] != grid[r + 1][c]:
                penalty += 1
    return -penalty

def snake_pattern_bonus(grid):
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

def heuristic(grid, weights):
    normalization = {
        'empty_tiles': 10,   # Scale for 0-16 empty tiles
        'max_tile': 1,    # Scale for potentially large numbers
        'smoothness': .1,    # Adjusted for typical smoothness values
        'monotonicity': 1,  # Scale for 0-8 monotonic lines
        'corner_max': 1,  # Scale for high value tiles
        'merge_penalty': 1,  # Scale for typical penalty values
        'snake_pattern': 1
    }   

    score = (
        weights['empty_tiles'] * normalization['empty_tiles'] * count_empty_tiles(grid)
        + weights['max_tile'] * normalization['max_tile'] * max_tile(grid)
        + weights['smoothness'] * normalization['smoothness'] * smoothness(grid)
        + weights['monotonicity'] * normalization['monotonicity'] * monotonicity(grid)
        + weights['corner_max'] * normalization['corner_max'] * corner_max(grid)
        + weights['merge_penalty'] * normalization['merge_penalty'] * merge_penalty(grid)
        + weights['snake_pattern'] * normalization['snake_pattern'] * snake_pattern_bonus(grid)
    )

    max_val = max_tile(grid)
    if max_val > 64:  # Only care about position for higher values
        if grid[0][0] != max_val and grid[0][3] != max_val and grid[3][0] != max_val and grid[3][3] != max_val:  # If max value isn't in top corners
            score *= 0.8  # Apply penalty

    
    print(weights['empty_tiles'] * normalization['empty_tiles'] * count_empty_tiles(grid)
        , weights['max_tile'] * normalization['max_tile'] * max_tile(grid)
        , weights['smoothness'] * normalization['smoothness'] * smoothness(grid)
        , weights['monotonicity'] * normalization['monotonicity'] * monotonicity(grid)
        , weights['corner_max'] * normalization['corner_max'] * corner_max(grid)
        , weights['merge_penalty'] * normalization['merge_penalty'] * merge_penalty(grid)
        , weights['snake_pattern'] * normalization['snake_pattern'] * snake_pattern_bonus(grid))
    
    return score