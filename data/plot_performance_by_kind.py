import sys

sys.path.append("../")

import warnings
import csv
import matplotlib.pyplot as plt

import networkx as nx

from src.graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
    min_cut_mapper,
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from networkx.algorithms.approximation import maximum_independent_set

warnings.filterwarnings("ignore", category=UserWarning)

paras = {
    "axes.labelsize": 23,
    "axes.titlesize": 23,
    "xtick.labelsize": 21,
    "ytick.labelsize": 22,
    "legend.fontsize": 21,
}
plt.rcParams.update(paras)
plt.rcParams["font.sans-serif"] = ["Arial"]

l_color = [
    "#967AB6",
    "#82D1F4",
    "#E2CB8E",
    "#666469",
]


def test_by_kind(graph_type, graph_size, step, mapper=min_cut_mapper):
    result = []
    if graph_type == "star":
        for i in range(10, graph_size, step):
            graph = nx.star_graph(i)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )

        with open(f"star_{i}.csv", "w", newline="") as file:
            # create the csv writer
            writer = csv.writer(file)
            # write a row to the csv file
            writer.writerow(result)

        x = range(10, graph_size, step)
        # plt.style.use("ggplot")
        plt.figure(figsize=(8, 6))
        before = [x[0] for x in result]
        random = [x[1] for x in result]
        min_map = [x[2] for x in result]

        plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
        plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
        plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Time Step(s)")
        # plt.grid(True)
        plt.legend(loc="upuiper left")
        plt.savefig(f"star_{i}.png")
    elif graph_type == "line":
        for i in range(10, graph_size, step):
            graph = nx.path_graph(i)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )

        with open(f"line_{i}.csv", "w", newline="") as file:
            # create the csv writer
            writer = csv.writer(file)
            # write a row to the csv file
            writer.writerow(result)

        x = range(10, graph_size, step)
        # plt.style.use("ggplot")
        plt.figure(figsize=(8, 6))
        before = [x[0] for x in result]
        random = [x[1] for x in result]
        min_map = [x[2] for x in result]

        plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
        plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
        plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Time step(s)")
        plt.legend(loc="upper left")
        plt.savefig(f"line_{i}.png")
    elif graph_type == "random_tree":
        random_seed = 10
        for i in range(10, graph_size, step):
            graph = nx.random_tree(i, seed=random_seed)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )

        with open(f"random_tree_{i}.csv", "w", newline="") as file:
            # create the csv writer
            writer = csv.writer(file)
            # write a row to the csv file
            writer.writerow(result)

        x = range(10, graph_size,step)
        # plt.style.use("ggplot")
        plt.figure(figsize=(8, 6))
        before = [x[0] for x in result]
        random = [x[1] for x in result]
        min_map = [x[2] for x in result]

        plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
        plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
        plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Time step(s)")
        plt.legend(loc="upper left")
        # plt.grid(True)
        plt.savefig(f"random_tree_{i}.png")
    elif graph_type == "complete":
        for i in range(10, graph_size, step):
            graph = nx.complete_graph(i)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )

        with open(f"complete_{i}.csv", "w", newline="") as file:
            # create the csv writer
            writer = csv.writer(file)
            # write a row to the csv file
            writer.writerow(result)

        x = range(10, graph_size, step)
        # plt.style.use("ggplot")
        plt.figure(figsize=(8, 6))
        before = [x[0] for x in result]
        random = [x[1] for x in result]
        min_map = [x[2] for x in result]

        plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
        plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
        plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Time step(s)")
        plt.legend(loc="upper left")
        plt.savefig(f"complete{i}.png")


"""
def test_star_graph():
    result = []
    for i in range(10, 110, 10):
        graph = nx.star_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        compiler_map = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=min_cut_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler_map.run()
        result.append(
            [
                compiler.input_graph.number_of_nodes(),
                len(compiler.measurement_steps),
                len(compiler_map.measurement_steps),
            ]
        )
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"star_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 110, 10)
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = [x[0] for x in result]
    after = [x[1] for x in result]
    map = [x[2] for x in result]

    plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x, after, "o-", color=l_color[0], label="Random Mapper")
    plt.plot(x, map, "*-", color=l_color[1], label="MinCut Mapper")

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time Step(s)")
    # plt.grid(True)
    plt.legend(loc="upper left")
    plt.savefig("star.png")


def test_line_graph():
    result = []
    for i in range(10, 110, 10):
        graph = nx.path_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        compiler_map = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=min_cut_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler_map.run()
        result.append(
            [
                compiler.input_graph.number_of_nodes(),
                len(compiler.measurement_steps),
                len(compiler_map.measurement_steps),
            ]
        )
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"line_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 110, 10)
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = [x[0] for x in result]
    after = [x[1] for x in result]
    map = [x[2] for x in result]

    plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x, after, "o-", color=l_color[0], label="Random Mapper")
    plt.plot(x, map, "*-", color=l_color[1], label="MinCut Mapper")

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    plt.legend(loc="upper left")
    plt.savefig("line.png")


def test_complete_graph():

    result = []
    for i in range(10, 110, 10):
        graph = nx.complete_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        compiler_map = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=min_cut_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler_map.run()
        result.append(
            [
                compiler.input_graph.number_of_nodes(),
                len(compiler.measurement_steps),
                len(compiler_map.measurement_steps),
            ]
        )
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"complete_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 110, 10)
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = [x[0] for x in result]
    after = [x[1] for x in result]
    map = [x[2] for x in result]

    plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x, after, "o-", color=l_color[0], label="Random Mapper")
    plt.plot(x, map, "*-", color=l_color[1], label="MinCut Mapper")

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    plt.legend(loc="upper left")
    plt.savefig("complete.png")

def test_random_tree():
    for i in range(1):
        result = []
        random_seed = 10
        for i in range(10, 110, 10):
            graph = nx.random_tree(i, seed=random_seed)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            compiler_map = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=min_cut_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler_map.run()
            result.append(
                [
                    compiler.input_graph.number_of_nodes(),
                    len(compiler.measurement_steps),
                    len(compiler_map.measurement_steps),
                ]
            )
            # print(compiler.input_graph.number_of_nodes())
            # print(len(compiler.measurement_steps))

        with open(f"random_tree_{i}.csv", "w", newline="") as file:
            # create the csv writer
            writer = csv.writer(file)
            # write a row to the csv file
            writer.writerow(result)

        x = range(10, 110, 10)
        # plt.style.use("ggplot")
        plt.figure(figsize=(8, 6))
        before = [x[0] for x in result]
        after = [x[1] for x in result]
        map = [x[2] for x in result]

        plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
        plt.plot(x, after, "o-", color=l_color[0], label="Random Mapper")
        plt.plot(x, map, "*-", color=l_color[1], label="MinCut Mapper")

        plt.xlabel("Number of Vertices")
        plt.ylabel("Time step(s)")
        plt.legend(loc="upper left")
        # plt.grid(True)
        plt.savefig("random_tree.png")

test_random_tree()
test_star_graph()
test_line_graph()
test_complete_graph()
"""
test_by_kind('random_tree', 30, 10, mapper=min_cut_mapper)