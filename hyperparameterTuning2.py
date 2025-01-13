from itertools import product
from gameRunner import gameloop_testing

WEIGHTOPTIONS = {'empty_tiles': [.5, 1, 1.5], 
            'max_tile': [.5, 1, 1.5], 
            'smoothness': [.5, 1, 1.5], 
            'monotonicity': [.5, 1, 1.5], 
            'corner_max': [.5, 1, 1.5], 
            'merge_penalty': [.5, 1, 1.5],
            'snake_pattern': [.5, 1, 1.5]}
all_combinations = list(product(*WEIGHTOPTIONS.values()))

print(len(all_combinations))

num_iters = 4
best_score = 0
best_weights = all_combinations[0]
iter_index = 1
for combination in all_combinations:
    weights = {'empty_tiles': combination[0], 
            'max_tile': combination[1], 
            'smoothness': combination[2], 
            'monotonicity': combination[3], 
            'corner_max': combination[4], 
            'merge_penalty': combination[5],
            'snake_pattern': combination[6]}
    score = 0
    for i in range(num_iters):
        score += gameloop_testing("ai", "expectimax", weights)
    score = score/num_iters
    if score > best_score:
        best_score = score
        best_weights = combination
    print(str(iter_index) + "/" + str(len(all_combinations)) + ":" + str(score))
    iter_index += 1

print(combination)

