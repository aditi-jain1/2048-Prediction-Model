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

all_combinations = list(product(*WEIGHTOPTIONS.values()))
print(len(all_combinations))
print(all_combinations[1])

def simulate_game(weights):
    grid = create_grid()
    spawn_tile(grid)  
    spawn_tile(grid)

    while not is_game_over(grid):
        move_dir = best_move(grid, weights)

        if move_dir in ['up', 'down', 'left', 'right']:
            grid = move(grid, move_dir)  
            spawn_tile(grid)  
    max_tile = max(max(row) for row in grid)
    return max_tile
'''
def simulate_game(weights):
    tiles = generate_tiles()
    grid = get_grid(tiles)
    while not is_game_over(grid):
        grid = get_grid(tiles)
        direction = best_move_with_n_lookahead(grid, 3, WEIGHTS)
        # Execute the AI's move
        if direction == None:
            break
        move_tiles_immediate(tiles, direction)
        end_move(tiles)
    max_tile = max(max(row) for row in grid)
    return max_tile
'''




results = []
i = 0

for combination in all_combinations:
    weights = {
        'empty_tiles': combination[0],
        'max_tile': combination[1],
        'smoothness': combination[2],
        'monotonicity': combination[3],
        'corner_max': combination[4],
        'merge_penalty': combination[5],
    }

    #print(f"Testing weights: {weights}")
    scores = [simulate_game(weights) for _ in range(4)]  # Simulate multiple games
    average_score = sum(scores) / len(scores)
    print(str(i) + "/" + str(len(all_combinations)) + str(average_score))
    results.append((weights, average_score))
    i += 1
    #print(f"Average score: {average_score}")

# Select the best weights based on average score
best_weights, best_score = max(results, key=lambda x: x[1])

print("\nBest Weights:")
print(best_weights)
print(f"Best Average Score: {best_score}")





