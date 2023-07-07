from timeit import default_timer as timer

import networkx as nx

from src.graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    NGAopt_layout,
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler


def gen_erdos_renyi_graph_single_component(n, m):
    G = nx.gnm_random_graph(n, m)
    if nx.number_connected_components(G) == 1:
        return G
    else:
        return gen_erdos_renyi_graph_single_component(n, m)


# g = gen_erdos_renyi_graph_single_component(500, 2500)
# g = gen_erdos_renyi_graph_single_component(10, 9)
g = nx.cycle_graph(10)
nothing_compiler = TwoRowSubstrateScheduler(g)

st = timer()
nx.algorithms.approximation.maximum_independent_set(g)
ed = timer()
print(f"time taken - {ed - st}s")

nothing_compiler.run()
nothing_compiler.get_summary()
nothing_compiler.visualization()
print("========================================")

scheduler_only_compiler = TwoRowSubstrateScheduler(
    g, stabilizer_scheduler=greedy_stabilizer_measurement_scheduler
)
scheduler_only_compiler.run()
scheduler_only_compiler.get_summary()
scheduler_only_compiler.visualization()
print("========================================")

for _ in range(2):
    better_compiler = TwoRowSubstrateScheduler(
        g,
        pre_mapping_optimizer=approximate_static_stabilizer_reduction,
        node_to_patch_mapper=NGAopt_layout,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    better_compiler.run()
    better_compiler.get_summary()

print("========================================")
for _ in range(2):
    faster_compiler = TwoRowSubstrateScheduler(
        g,
        pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
        node_to_patch_mapper=NGAopt_layout,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    faster_compiler.run()
    faster_compiler.get_summary()
    faster_compiler.visualization()
