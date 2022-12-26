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
)
from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler

from networkx.algorithms.approximation import maximum_independent_set


warnings.filterwarnings("ignore", category=UserWarning)


for i in range(1):
    result = []
    for i in range(10, 1000, 50):
        graph = nx.star_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=approximate_static_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        result.append([compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)])
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"star_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 1000, 50)
    plt.style.use("ggplot")
    plt.figure(figsize=(10, 5))
    before = [x[0] for x in result]
    after = [x[1] for x in result]

    plt.plot(x, before, "s-", color="g", label="Original Time Steps")
    plt.plot(x, after, "o-", color="r", label="After Optimization")

    plt.title("Star Graph Performance Test")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time step")
    plt.legend()
    plt.grid(True)
    plt.savefig("star.png")


for i in range(1):
    result = []
    for i in range(10, 1000, 50):
        graph = nx.path_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        result.append([compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)])
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"line_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 1000, 50)
    plt.style.use("ggplot")
    plt.figure(figsize=(10, 5))
    before = [x[0] for x in result]
    after = [x[1] for x in result]

    plt.plot(x, before, "s-", color="g", label="Original Time Steps")
    plt.plot(x, after, "o-", color="r", label="After Optimization")

    plt.title("Line Graph Performance Test")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time step")
    plt.legend()
    plt.grid(True)
    plt.savefig("line.png")

for i in range(1):
    result = []
    for i in range(10, 1000, 50):
        graph = nx.complete_graph(i)

        compiler = TwoRowSubstrateScheduler(
            graph,
            pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
            node_to_patch_mapper=random_mapper,
            stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
        )
        compiler.run()
        result.append([compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)])
        # print(compiler.input_graph.number_of_nodes())
        # print(len(compiler.measurement_steps))

    with open(f"complete_{i}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(result)

    x = range(10, 1000, 50)
    plt.style.use("ggplot")
    plt.figure(figsize=(10, 5))
    before = [x[0] for x in result]
    after = [x[1] for x in result]

    plt.plot(x, before, "s-", color="g", label="Original Time Steps")
    plt.plot(x, after, "o-", color="r", label="After Optimization")

    plt.title("Complete Graph Performance Test")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time step")
    plt.legend()
    plt.grid(True)
    plt.savefig("complete.png")
