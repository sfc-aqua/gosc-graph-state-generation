from timeit import default_timer as timer
from typing import List, Set

import networkx as nx
import numpy as np


# to make file not empty
def straightforward_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    return [x for x in range(g.number_of_nodes())]


def random_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    return list(np.random.permutation(g.number_of_nodes()))


# def min_cut_mapper(g: nx.Graph, skipped_stabilizer: Set[int]) -> List[int]:
#     return [x for x in range(g.number_of_nodes())]
