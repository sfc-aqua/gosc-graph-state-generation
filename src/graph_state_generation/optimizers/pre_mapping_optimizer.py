from typing import Set, Tuple

import networkx as nx
import numpy as np


def approximate_static_stabilizer_reduction(g: nx.Graph) -> Tuple[Set[int], nx.Graph]:
    """Uses maximum independent set algorithm to find state initialization such that
    most stabilizer generators are already stabilized so the stabilizer measurements
    needed are reduced."""
    max_i_set = nx.algorithms.approximation.maximum_independent_set(g)
    return (max_i_set, g)


def fast_maximal_independent_set_stabilizer_reduction(
    g: nx.Graph,
) -> Tuple[Set[int], nx.Graph]:
    """Repeatly run maximal independent set on a random vertex to find
    largest maximal independent set."""
    i_set = nx.maximal_independent_set(g)
    max_retry = np.log2(g.number_of_nodes())
    retry = max_retry
    while retry > 0:
        ni_set = nx.maximal_independent_set(g)
        retry -= 1
        if len(ni_set) > len(i_set):
            retry = max_retry
            i_set = ni_set
    return (i_set, g)
