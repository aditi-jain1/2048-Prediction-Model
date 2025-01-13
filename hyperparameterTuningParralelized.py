from itertools import product
from multiprocessing import Pool, cpu_count
from gameRunner import gameloop_testing
from functools import partial

def evaluate_weights(combination, num_iters):
    """Evaluate a single combination of weights"""
    weights = {
        'empty_tiles': combination[0],
        'max_tile': combination[1],
        'smoothness': combination[2],
        'monotonicity': combination[3],
        'corner_max': combination[4],
        'merge_penalty': combination[5],
        'snake_pattern': combination[6]
    }
    
    score = 0
    for _ in range(num_iters):
        score += gameloop_testing("ai", "expectimax", weights)
    return score / num_iters, combination

def main():
    WEIGHTOPTIONS = {
        'empty_tiles': [.5, 1, 1.5],
        'max_tile': [.5, 1, 1.5],
        'smoothness': [.5, 1, 1.5],
        'monotonicity': [.5, 1, 1.5],
        'corner_max': [.5, 1, 1.5],
        'merge_penalty': [.5, 1, 1.5],
        'snake_pattern': [.5, 1, 1.5]
    }
    
    all_combinations = list(product(*WEIGHTOPTIONS.values()))
    print(f"Total combinations to evaluate: {len(all_combinations)}")
    
    num_iters = 4
    num_processes = cpu_count()  # Use all available CPU cores
    
    # Create a partial function with fixed num_iters
    eval_partial = partial(evaluate_weights, num_iters=num_iters)
    
    best_score = 0
    best_weights = all_combinations[0]
    
    # Create a process pool
    with Pool(processes=num_processes) as pool:
        # Use imap_unordered to get results as they complete
        for i, (score, combination) in enumerate(pool.imap_unordered(eval_partial, all_combinations), 1):
            print(f"{i}/{len(all_combinations)}: {score}")
            
            if score > best_score:
                best_score = score
                best_weights = combination
    
    print("\nBest weights found:")
    print(f"Score: {best_score}")
    print("Weights:", {
        'empty_tiles': best_weights[0],
        'max_tile': best_weights[1],
        'smoothness': best_weights[2],
        'monotonicity': best_weights[3],
        'corner_max': best_weights[4],
        'merge_penalty': best_weights[5],
        'snake_pattern': best_weights[6]
    })

if __name__ == '__main__':
    main()