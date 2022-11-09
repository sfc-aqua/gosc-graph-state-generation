#! /bin/usr/env python3
from enum import Enum
from timeit import default_timer as timer
from typing import List, Set, Tuple

import networkx as nx


class Basis(Enum):
    X = 1
    Z = 2


def default_pre_mapping_optimizer(g: nx.Graph) -> Tuple[Set[int], nx.Graph]:
    return (set(), g)


def default_node_to_patch_mapper(g: nx.Graph, _: Set[int]) -> List[int]:
    return [x for x in range(g.number_of_nodes())]


def default_stabilizer_scheduler(
    stabilizer_to_measure: List[Tuple[int, Tuple[int, int]]]
) -> List[List[Tuple[int, Tuple[int, int]]]]:

    return list(map(lambda x: [(x[0], x[1])], stabilizer_to_measure))


class TwoRowSubstrateScheduler:
    """The very basic substrate scheduler where all qubits are represented by 2-tile patches
    align in a single row and another row is for ancilla to perform multi-Pauli product
    measurement for stabilizer generator projection.

    It works in three phases by accepting 3 functions
    1. pre-mapping optimization
    2. node-to-patch mapping
    3. stabilizer measurement scheduling

    If the optimizer functions are not provided, no optimization is done and only one stabilizer measurement is performed at each time step resulting in O(V) time step
    """

    def __init__(
        self,
        input_graph: nx.Graph,
        pre_mapping_optimizer=default_pre_mapping_optimizer,  # nx.Graph -> Tuple(Set(stabilizer_to_skip), nx.Graph)
        node_to_patch_mapper=default_node_to_patch_mapper,  # nx.Graph -> List(int) of length V
        stabilizer_scheduler=default_stabilizer_scheduler,  # [(S_i, (min_i, max_i))] -> [[(S_i, (min_i, max_i))], [(S_j, (min_j, max_j))]] with length equals to number of timestep where S_i, min_i, and max_i are int
    ):
        """pre_mapping_optimizer -"""

        #
        self.input_graph: nx.Graph = input_graph
        self.label: List[int] = []
        self.adj_list: List[List[int]] = []
        self.stabilizer: List[
            Tuple[int, List[int]]
        ] = []  # Tuple[Pauli_X, List[Pauli_Z]] where it corresponds to the patch label

        self.stabilizer_to_measure: List[
            Tuple[int, Tuple[int, int]]
        ] = (
            []
        )  # (G_i, (ancilla_left, ancilla_right)) where G_i denote stabilizer of patch i
        self.pre_mapping_optimizer = pre_mapping_optimizer
        self.node_to_patch_mapper = node_to_patch_mapper
        self.stabilizer_scheduler = stabilizer_scheduler

        # parse the input graph and set class attributes
        self.adj_list = [vs for _, vs in nx.to_dict_of_lists(input_graph).items()]
        self.stabilizer_to_measure = []

        # for reporting instructions and time-space volume analysis
        self.patch_state_init: List[Basis] = [Basis.Z] * input_graph.number_of_nodes()
        self.measurement_steps: List[List[Tuple[int, Tuple[int, int]]]] = []

    def visualization(self, fmt="ascii"):
        pass

    def stabilizer_table(self):
        """print stabilizer of the input graph state in ascii format (I is replaced with _ for better readability).
        Only support up to 100 vertices."""
        n = self.input_graph.number_of_nodes()
        stabilizers_str: List[str] = [""] * n

        def _adj_to_stabilizer(i: int, vs: List[int]) -> str:
            barr = bytearray(b"_") * n
            barr[i] = 65 + 23  # 'X'
            for v in vs:
                barr[v] = 65 + 25  # 'Z'
            return barr.decode()

        for i in range(n):
            stabilizers_str[i] = _adj_to_stabilizer(i, self.adj_list[i])

        print("\n".join(stabilizers_str))

    def run(self):
        """Execute the three phases on creating the input graph state into Litinski's GoSC ruleset instructions.
        This function will also output the running time of each phase."""

        # graph optimization
        pre_opt_start_time = timer()
        stabilizer_to_skip, transformmed_graph = self.pre_mapping_optimizer(
            self.input_graph
        )
        pre_opt_end_time = timer()

        # node to patch mapping / labelling
        labelling_start_time = timer()
        self.label = self.node_to_patch_mapper(transformmed_graph, set())
        labelling_end_time = timer()

        scheduling_start_time = timer()
        # from here on we work on patch labelling and not labelling of the input graph
        for i, vs in enumerate(self.adj_list):
            mi = self.label[i]
            mvs = [self.label[v] for v in vs]

            if i in stabilizer_to_skip:
                self.patch_state_init[mi] = Basis.X
                continue

            self.stabilizer_to_measure.append(
                (mi, (min(mi, min(mvs)), (max(mi, max(mvs)))))
            )
        self.measurement_steps = self.stabilizer_scheduler(self.stabilizer_to_measure)
        scheduling_end_time = timer()

        # fmt: off
        # report time
        print(f'pre-mapping optimization took - {pre_opt_end_time - pre_opt_start_time}s')
        print(f'node to patch mapping took    - {labelling_end_time - labelling_start_time}s')
        print(f'measurement scheduler took    - {scheduling_end_time - scheduling_start_time}s')
        # fmt: on

    def get_summary(self):
        print(f"reduce from {self.input_graph.number_of_nodes()} to {len(self.measurement_steps)}")

    def get_instructions(self):
        # TODO: add labeling phase
        return self.measurement_steps
