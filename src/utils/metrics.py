
import numpy as np 
from scipy.stats import spearmanr, kendalltau

# helpers
def get_sorted_ratings(scores_dict):
    # Sort the dictionary by keys (players) and return the values (scores) in the same order
    sorted_players = sorted(scores_dict.keys())
    sorted_scores = [scores_dict[player] for player in sorted_players]
    return sorted_scores


def measure_rms(predicted_scores, ground_truth_scores, epsilon=1e-10):
    # Ensure the keys in both dictionaries are the same
    if predicted_scores.keys() != ground_truth_scores.keys():
        raise ValueError("Keys in predicted_scores and ground_truth_scores do not match.")
    

    predicted_scores = [score for player, score in sorted(predicted_scores.items(), key=lambda x: x[0])]
    true_scores = [score for player, score in sorted(ground_truth_scores.items(), key=lambda x: x[0])]


    predicted_scores = np.array(predicted_scores) + epsilon
    true_scores = np.array(true_scores) + epsilon


    rms = np.sqrt(np.mean((np.log(predicted_scores) - np.log(true_scores)) ** 2))
    
    return rms


def measure_rho(predicted_scores, ground_truth_scores):
    # measure predicted score of a player to it's true score
    predicted_scores = get_sorted_ratings(predicted_scores)
    true_scores = get_sorted_ratings(ground_truth_scores)

    correlation, p_val = spearmanr(predicted_scores, true_scores)

    return correlation


def measure_tau(predicted_scores, ground_truth_scores):
    # Sort both dictionaries by keys (players) to ensure alignment
    sorted_predicted = get_sorted_ratings(predicted_scores)
    sorted_true = get_sorted_ratings(ground_truth_scores)

    # Calculate Kendall's tau correlation coefficient
    correlation, p_val = kendalltau(sorted_predicted, sorted_true)

    return correlation


def measure_log_likelihood (data, pi_values, model = 'ho_bt', epsilon=1e-10):
    
    
    log_like = log_prior = 0.0
    
    for i in pi_values:
        log_prior += np.log(pi_values[i]+epsilon) - 2.0 * np.log(1.0+pi_values[i]+epsilon)
        
    ############################################    
    if model == 'ho_bt':
        for i in range(0,len(data)):
            for j in range(0, len(data[i])-1):
                tmp = np.log(pi_values[data[i][j]] + epsilon)
                norm = 0.0
                for k in range(j, len(data[i])):
                    norm += pi_values[data[i][k]]
                tmp -= np.log(norm+epsilon)
                log_like += tmp
            
    ############################################    
    if model == 'ho_bt_leader':
        for i in range(0,len(data)):
            tmp = np.log(pi_values[data[i][0]] + epsilon)
            norm = 0.0
            for j in range(0, len(data[i])):
                norm += pi_values[data[i][j]]
            tmp -= np.log(norm+epsilon)
            log_like += tmp

    
    return log_like, log_prior
    
#measure in average log likelihood in accordance to a weighted test set
def measure_likelihood(pred_ranking, testing_set, epsilon=1e-10):
    total_log_likelihood = 0.0

    for game in testing_set:
        for j in range(len(game)-1):
            tmp = np.log(pred_ranking[game[j]] + epsilon)
            total_ratings = sum(pred_ranking[k] for k in game[j:])
            tmp -= np.log(total_ratings + epsilon)
            total_log_likelihood +=  tmp

    total_games = len(testing_set)
    return total_log_likelihood / total_games   


def measure_leadership_likelihood(pred_ranking, testing_set, epsilon=1e-10):

    total_log_likelihood = 0.0

    for game in testing_set:
        tmp = np.log(pred_ranking[game[0]] + epsilon)
        total_ratings = sum(pred_ranking[k] for k in game)
        tmp -= np.log(total_ratings + epsilon)
        total_log_likelihood +=  tmp

    total_games = len(testing_set)
    return total_log_likelihood/total_games




# ALTERNATIVE LIKELIHOOD ESTIMATIONS

# def  measure_likelihood(pred_ranking, testing_set):
#     return [recursive_probability_estimation(pred_ranking, game, weight) for game, weight in testing_set.items()]

# def measure_leadership_likelihood(pred_ranking, testing_set):
#     return [leadership_probability_estimation(pred_ranking, game, weight) for game, weight in testing_set.items()]

# def measure_likelihood_ratio(pred_ranking, pi_values, testing_set):
#     likelihood_ratios = []
#     for game in testing_set:
#         pred_likelihood = recursive_probability_estimation(pred_ranking, game)
#         ground_truth_likelihood = recursive_probability_estimation(pi_values, game)
#         likelihood_ratios.append(pred_likelihood / ground_truth_likelihood)
#     return likelihood_ratios

# def leadership_probability_estimation(pred_rating, game, weight, epsilon=1e-10):
#     player_rankings = [pred_rating[player] for player in game]
#     highest_rank = player_rankings[0]
#     total_ratings = sum(player_rankings)
#     return weight * (np.log(highest_rank+epsilon) - np.log(total_ratings+epsilon))

# def recursive_probability_estimation(pred_rating, game, weight, total_prob_estimation=0, episilon=1e-10):
#     player_ratings = [pred_rating[player] for player in game]
#     first_pos = player_ratings[0]
#     total_ratings = sum(player_ratings)
#     total_prob_estimation += np.log(first_pos+episilon) - np.log(total_ratings+episilon)

#     if len(player_ratings) > 2:
#         return recursive_probability_estimation(pred_rating, game[1:], weight, total_prob_estimation)
#     else:
#         return total_prob_estimation * weight

