import json
import random
import subprocess

import networkx as nx


def gen_erdos_renyi_graph_single_component(n, m):
    if_connected = 0
    for i in range(1000):
        G = nx.gnm_random_graph(n, m)
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

        n_edges_very_sparse = random.randint(
            n_nodes_ran, n_nodes_ran + edge_numbers / 4
        )
        n_edges_sparse = random.randint(
            n_nodes_ran + edge_numbers / 4, n_nodes_ran + edge_numbers / 2
        )
        n_edges_dense = random.randint(
            n_nodes_ran + edge_numbers / 2, n_nodes_ran + edge_numbers * 3 / 4
        )
        n_edges_very_dense = random.randint(
            n_nodes_ran + edge_numbers * 3 / 4, n_nodes_ran + edge_numbers
        )

        very_sparse = gen_erdos_renyi_graph_single_component(
            n_nodes_ran, n_edges_very_sparse
        )
        sparse = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_sparse)
        dense = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_dense)
        very_dense = gen_erdos_renyi_graph_single_component(
            n_nodes_ran, n_edges_very_dense
        )

        with open(f"graphs/very_sparse_{i}.json", "w") as json_file:
            json.dump(very_sparse, json_file)
        with open(f"graphs/dense_{i}.json", "w") as json_file:
            json.dump(sparse, json_file)
        with open(f"graphs/dense_{i}.json", "w") as json_file:
            json.dump(dense, json_file)
        with open(f"graphs/very_dense_{i}.json", "w") as json_file:
            json.dump(very_dense, json_file)


#     very_sparse_graphs = open("very_sparse_graphs.txt", "a", encoding="utf-8")
#     sparse_graphs = open("sparse_graphs.txt", "a", encoding="utf-8")
#     dense_graphs = open("dense_graphs.txt", "a", encoding="utf-8")
#     very_dense_graphs = open("very_dense_graphs.txt", "a", encoding="utf-8")

#     if (
#         very_sparse is not None
#         and int(subprocess.getoutput("wc -l %s" % "very_sparse_graphs.txt").split()[0])
#         < 100
#     ):
#         print("%s" % (very_sparse), file=very_sparse_graphs)
#     if (
#         sparse is not None
#         and int(subprocess.getoutput("wc -l %s" % "sparse_graphs.txt").split()[0]) < 100
#     ):
#         print("%s" % (sparse), file=sparse_graphs)
#     if (
#         dense is not None
#         and int(subprocess.getoutput("wc -l %s" % "dense_graphs.txt").split()[0]) < 100
#     ):
#         print("%s" % (dense), file=dense_graphs)
#     if (
#         very_dense is not None
#         and int(subprocess.getoutput("wc -l %s" % "very_dense_graphs.txt").split()[0])
#         < 100
#     ):
#         print("%s" % (very_dense), file=very_dense_graphs)


# print(
#     "Very sparse graph has %s lines"
#     % subprocess.getoutput("wc -l %s" % "very_sparse_graphs.txt").split()[0]
# )
# print(
#     "Sparse graph has %s lines"
#     % subprocess.getoutput("wc -l %s" % "sparse_graphs.txt").split()[0]
# )
# print(
#     "Dense graph has %s lines"
#     % subprocess.getoutput("wc -l %s" % "dense_graphs.txt").split()[0]
# )
# print(
#     "Very dense graph has %s lines"
#     % subprocess.getoutput("wc -l %s" % "very_dense_graphs.txt").split()[0]
# )
