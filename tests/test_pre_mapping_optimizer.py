import sys
import networkx as nx

sys.path.append("..")
from src.graph_state_generation.optimizers.pre_mapping_optimizer import (
    fast_maximal_independent_set_stabilizer_reduction,
)


def test_max_independet_set_reduction():
    stabilizers_set_0 = [(0, (0, 5)), (1, (1, 2)), (2, (1, 10))]
    graph = {0: [2, 5], 1: [3], 2: [0, 3], 3: [1, 2, 4], 4: [3], 5: [0]}
    G = nx.Graph(graph)
    assert sorted(fast_maximal_independent_set_stabilizer_reduction(G)[0]) == [
        1,
        2,
        4,
        5,
    ]
