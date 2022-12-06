import networkx as nx

from graph_state_generation.optimizers.pre_mapping_optimizer import (
    fast_maximal_independent_set_stabilizer_reduction,
)


def test_max_independet_set_reduction_0():
    graph_0 = {0: [2, 5], 1: [3], 2: [0, 3], 3: [1, 2, 4], 4: [3], 5: [0]}
    G_0 = nx.Graph(graph_0)
    assert sorted(fast_maximal_independent_set_stabilizer_reduction(G_0)[0]) == [
        1,
        2,
        4,
        5,
    ]


def test_max_independet_set_reduction_1():
    graph_1 = {0: [1, 2, 3, 4, 5], 1: [0], 2: [0], 3: [0], 4: [0], 5: [0]}
    G_1 = nx.Graph(graph_1)
    assert sorted(fast_maximal_independent_set_stabilizer_reduction(G_1)[0]) == [
        1,
        2,
        3,
        4,
        5,
    ]

def test_max_independet_set_reduction_2():
    graph_2 = {0: [1, 2], 1: [0, 3], 2: [0, 5], 3: [1, 4], 4: [1, 2, 3, 5], 5: [2, 4]}
    G_2 = nx.Graph(graph_2)
    assert sorted(fast_maximal_independent_set_stabilizer_reduction(G_2)[0]) == [
        0,
        3,
        5,
    ]
