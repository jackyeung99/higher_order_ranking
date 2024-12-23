import os
import sys
from concurrent.futures import ProcessPoolExecutor
import pandas as pd


repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(repo_root)

from src import split_weighted_dataset, run_models, read_edge_list


def process_rep(rep, data, pi_values, out_file_dir, dataset_id): 
     training_set, testing_set = split_weighted_dataset(data)
     model_performance = run_models(training_set, testing_set, pi_values)
     file_path = os.path.join(out_file_dir, f'dataset-{dataset_id}_rep-{rep+1}.csv')
     model_performance.to_csv(file_path, index=False)

def process_file(file, dataset_file_path, repetitions, out_file_dir):
    file_path = os.path.join(dataset_file_path, file)
    data, pi_values = read_edge_list(file_path)
    dataset_id = int(file.split('_')[0])
    
    if dataset_id not in [10, 11, 15, 41, 43, 44, 46, 47, 48, 49, 50, 51, 54, 55, 56, 58, 101]:
        print(file)
        futures = []
        with ProcessPoolExecutor(max_workers=32) as executor:
            for rep in range(repetitions):
                futures.append(executor.submit(process_rep, rep, data, pi_values, out_file_dir, dataset_id))
               

def run_experiment(dataset_file_path, repetitions, out_file_directory):
    os.makedirs(out_file_directory, exist_ok=True)

    for file in os.listdir(dataset_file_path):
        if file.endswith('_edges.txt'):
            process_file(file, dataset_file_path, repetitions, out_file_directory)

            


if __name__ == '__main__':
    # Run From ex03_realdata directory
    # rsync -zaP burrow:multi-reactive_rankings/higher_order_ranking/exp/ex02/data ~/senior_thesis/higher_order_ranking/exp/ex02/

    base_path = os.path.dirname(__file__)
    dataset_file_path = os.path.join(repo_root, 'datasets', 'processed_data')
    out_file = os.path.join(base_path, 'data')

    run_experiment(dataset_file_path, 50, out_file_directory=out_file) 
