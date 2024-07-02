import os 
import sys
import networkx as nx 

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(repo_root)

from src.utils.graph_tools import *

def compute_predicted_ratings_page_rank(games, pi_values):
    edge_list = binarize_data (games)

    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    
    # Initialize PageRank values with the provided pi_values
    personalization = {node: 1.0 for node in G.nodes}
    
    page_rank = nx.pagerank(G, personalization=personalization)
    for node in pi_values:
        pi_values[node] = page_rank.get(node, 1.0)
        
    
    normalize_scores(pi_values)
        
    return pi_values


def compute_predicted_ratings_page_rank_leadership(games, pi_values):
    edge_list = binarize_data_leadership (games)

    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    
    # Initialize PageRank values with the provided pi_values
    personalization = {node: 1.0 for node in G.nodes}
    
    page_rank = nx.pagerank(G, personalization=personalization)
    for node in pi_values:
        pi_values[node] = page_rank.get(node, 1.0)
            
    
    normalize_scores(pi_values)
        
    return pi_values


if __name__ == '__main__': 

    pi_values, data = generate_model_instance(500, 500, 2, 4)

    calculate_predicted_rankings_page_rank(data, pi_values)
 