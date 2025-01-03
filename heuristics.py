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
