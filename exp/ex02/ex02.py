import os
import sys
import logging
from sklearn.model_selection import train_test_split
from concurrent.futures import ProcessPoolExecutor

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(repo_root)

from src import *



def process_fixed_rep(rep, N, M, K1, K2, train_size, file_dir, leadership=False):

    if leadership:
        data, pi_values = generate_leadership_model_instance(N, M, K1, K2)
    else:
        data, pi_values = generate_model_instance(N, M, K1, K2)

    # Split data into training and testing sets
    training_set, testing_set = split_weighted_dataset(data, train_size=train_size, random_state=None)

    model_performance = run_models_synthetic(training_set, testing_set, pi_values)
    file_path = os.path.join(file_dir, f'rep-{rep+1}.csv')
    model_performance.to_csv(file_path)

def evaluate_models_fixed_train_size(N, M, K1, K2, file_dir, leadership=False, repetitions=1000, train_size=0.8):
    os.makedirs(file_dir, exist_ok=True)

    futures = []
    with ProcessPoolExecutor() as executor:
        for rep in range(repetitions):
            futures.append(executor.submit(process_fixed_rep, rep, N, M, K1, K2, train_size, file_dir, train_size))


        
if __name__ == '__main__':

    base_path = os.path.dirname(__file__)
    # standard 
    N, M, K1, K2 = 5000, 10000, 2, 2
    evaluate_models_fixed_train_size(N, M, K1, K2, os.path.join(base_path, 'data','ex02.1'))

    # higher order 
    N, M, K1, K2 = 5000, 10000, 5, 5
    evaluate_models_fixed_train_size(N, M, K1, K2, os.path.join(base_path, 'data', 'ex02.2'))
    
    # higher order leadership
    N, M, K1, K2 = 5000, 10000, 5, 5
    evaluate_models_fixed_train_size(N, M, K1, K2, os.path.join(base_path, 'data', 'ex02.3'), leadership=True)
        