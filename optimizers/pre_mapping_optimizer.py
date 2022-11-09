from typing import Set, Tuple

import networkx as nx


def approximate_static_stabilizer_reduction(g: nx.Graph) -> Tuple[Set[int], nx.Graph]:
    max_i_set = nx.algorithms.approximation.maximum_independent_set(g)
    return (max_i_set, g)
