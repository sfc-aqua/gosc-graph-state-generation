from timeit import default_timer as timer
from typing import List, Set

import networkx as nx
import numpy as np


def random_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    """This mapper randomly permutes the label and ignore the skipped_stabilizer set."""
    return list(np.random.permutation(g.number_of_nodes()))


# def min_cut_mapper(g: nx.Graph, skipped_stabilizer: Set[int]) -> List[int]:
#     return [x for x in range(g.number_of_nodes())]
