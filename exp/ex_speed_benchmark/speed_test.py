import os
import sys
import time
import pandas as pd
import numpy as np

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(repo_root)

from src.models import *
from exp.ex_speed_benchmark.models.parallel_BT import parallel_ho, parallel_hol, parallel_std_leadership, parrallel_std
from exp.ex_speed_benchmark.models.numpy_BT import numpy_ho, numpy_hol, numpy_std, numpy_std_leadership
from tst.tst_weight_conversion.old_newman import compute_predicted_ratings_BT_leadership_old, compute_predicted_ratings_BT_old, compute_predicted_ratings_HO_BT_old, compute_predicted_ratings_HOL_BT_old
from src.utils import generate_model_instance, convert_games_to_dict

def run_all_newman(weighted_data, pi_values):
    
    start = time.perf_counter() 
    compute_predicted_ratings_BT(weighted_data, pi_values)
    compute_predicted_ratings_BT_leadership(weighted_data, pi_values)
    compute_predicted_ratings_HO_BT(weighted_data, pi_values)
    compute_predicted_ratings_HOL_BT(weighted_data, pi_values)
    end = time.perf_counter()
    tot_time  = end - start
    return tot_time

    
def run_all_newman_old(data, pi_values):
    start = time.perf_counter()
    compute_predicted_ratings_BT_old(data, pi_values)
    compute_predicted_ratings_BT_leadership_old(data, pi_values)
    compute_predicted_ratings_HO_BT_old(data, pi_values)
    compute_predicted_ratings_HOL_BT_old(data, pi_values)
    end = time.perf_counter()
    tot_time = end - start

    return tot_time

def run_all_parrallel(data, pi_values):
    start = time.perf_counter()
    parrallel_std(data, pi_values)
    parallel_std_leadership(data, pi_values)
    parallel_ho(data, pi_values)
    parallel_hol(data, pi_values)
    end = time.perf_counter()
    tot_time = end - start

    return tot_time


def run_all_numpy(weighted_data, pi_values): 

    start = time.perf_counter()
    numpy_std(weighted_data, pi_values)
    numpy_std_leadership(weighted_data, pi_values)
    numpy_ho(weighted_data, pi_values)
    numpy_hol(weighted_data, pi_values)
    end = time.perf_counter()
    tot_time = end - start

    return tot_time


def test_models(N, M, K1, K2):

    data, pi_values = generate_model_instance(N,M,K1,K2)
    weighted_data = convert_games_to_dict(data)

    std_model = run_all_newman(weighted_data, pi_values)
    old_newman = run_all_newman_old(data, pi_values)
    parallel = run_all_parrallel(data, pi_values)
    numpy = run_all_numpy(weighted_data, pi_values)
    
    return {'std_model': std_model, 'old_newman': old_newman, 'parrallel': parallel, 'numpy': numpy}


def test_M(results_dir):

    N=1000
    M_vec = np.logspace(2,6, num=10)
    K = 4

    results = []
    for m in M_vec:
        print(m)
        m = int(m)
        iteration = test_models(N, m, K, K)
        iteration['m'] = m
        results.append(iteration)

    
    df = pd.DataFrame(results)
    out_file = os.path.join(results_dir, 'test_M.csv')
    df.to_csv(out_file, index=False)

def test_N(results_dir):

    N_vec = np.logspace(2,6, num=10)
    M = 1000
    K = 4

    results = []
    for n in N_vec:
        n = int(n)
        iteration = test_models(n, M, K, K)
        iteration['n'] = n
        results.append(iteration)

    
    df = pd.DataFrame(results)
    out_file = os.path.join(results_dir, 'test_N.csv')
    df.to_csv(out_file, index=False)

def test_K(results_dir):

    N = 1000
    M = 1000
    K_vec = [2, 8, 15, 30, 50, 100]

    results = []
    for k in K_vec:
        iteration = test_models(N, M, k, k)
        iteration['k'] = k
        results.append(iteration)

    
    df = pd.DataFrame(results)
    out_file = os.path.join(results_dir, 'test_K.csv')
    df.to_csv(out_file, index=False)

if __name__ == '__main__':

    results_path = os.path.join(repo_root, 'exp', 'ex_speed_benchmark', 'results')
    os.makedirs(results_path, exist_ok=True)

    test_M(results_path)
    test_N(results_path)
    test_K(results_path)
