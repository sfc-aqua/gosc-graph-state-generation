from timeit import default_timer as timer

import networkx as nx

from src.graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler


def gen_erdos_renyi_graph_single_component(n, m):
    G = nx.gnm_random_graph(n, m)
    if nx.number_connected_components(G) == 1:
        return G
    else:
        return gen_erdos_renyi_graph_single_component(n, m)


g = gen_erdos_renyi_graph_single_component(500, 2500)
nothing_compiler = TwoRowSubstrateScheduler(g)

st = timer()
nx.algorithms.approximation.maximum_independent_set(g)
ed = timer()
print(f"time taken - {ed - st}s")

nothing_compiler.run()
nothing_compiler.get_summary()
print("========================================")
for _ in range(5):
    better_compiler = TwoRowSubstrateScheduler(
        g,
        pre_mapping_optimizer=approximate_static_stabilizer_reduction,
        node_to_patch_mapper=random_mapper,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    better_compiler.run()
    better_compiler.get_summary()
