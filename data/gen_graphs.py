import json
import random
import os

import math

import networkx as nx


def gen_erdos_renyi_graph_single_component(n, m):
    if_connected = 0
    for i in range(1000):
        G = nx.gnm_random_graph(n, m, seed=51)
        if_connected = nx.number_connected_components(G)
        if if_connected == 1:
            break
    if if_connected == 1:
        return nx.to_dict_of_lists(G)
    else:
        return None


for i in range(5):
    for n_nodes_ran in range(10, 1000, 50):
        # minimum number of edges for undirected connected graph is (n-1) edges
        # maximal number of edges for undirected connected graph is n(n-1)/2 edges
        edge_numbers = n_nodes_ran * (n_nodes_ran - 1) / 2 - n_nodes_ran

        random.seed(10)

        n_edges_very_sparse = random.randint(n_nodes_ran, math.floor(n_nodes_ran + edge_numbers / 4))

        n_edges_sparse = random.randint(
            math.floor(n_nodes_ran + edge_numbers / 4),
            math.floor(n_nodes_ran + edge_numbers / 2),
        )
        n_edges_dense = random.randint(
            math.floor(n_nodes_ran + edge_numbers / 2),
            math.floor(n_nodes_ran + edge_numbers * 3 / 4),
        )
        n_edges_very_dense = random.randint(
            math.floor(n_nodes_ran + edge_numbers * 3 / 4),
            math.floor(n_nodes_ran + edge_numbers),
        )

        very_sparse = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_very_sparse)
        sparse = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_sparse)
        dense = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_dense)
        very_dense = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_very_dense)
        if not os.path.exists("graph"):
            os.makedirs("graph")
        with open(f"graph/very_sparse_{i}.json", "w") as json_file:
            json.dump(very_sparse, json_file)
        with open(f"graph/dense_{i}.json", "w") as json_file:
            json.dump(sparse, json_file)
        with open(f"graph/dense_{i}.json", "w") as json_file:
            json.dump(dense, json_file)
        with open(f"graph/very_dense_{i}.json", "w") as json_file:
            json.dump(very_dense, json_file)
