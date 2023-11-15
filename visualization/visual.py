import sys
import warnings
import csv
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import numpy as np
import re
import os

sys.path.append("../")
from src.graph_state_generation.optimizers import (
    approximate_static_stabilizer_reduction,
    fast_maximal_independent_set_stabilizer_reduction,
    greedy_stabilizer_measurement_scheduler,
    random_mapper,
    min_cut_mapper,
    NGAopt_layout,
    total_edge_weight,
)

from src.graph_state_generation.substrate_scheduler import TwoRowSubstrateScheduler


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


def run_compiler(graph, mapper):
    compiler = TwoRowSubstrateScheduler(
        graph,
        pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
        node_to_patch_mapper=mapper,
        stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
    )
    compiler.run()
    return [
        compiler.input_graph.number_of_nodes(),
        compiler.time_steps,
        compiler.label,
        compiler.edge_weight,
    ]


def test_by_kind(graph_type, graph_size=100, step=10, mapper=NGAopt_layout):
    """
    Parameters:
    - graph_type: Available graph types: star, line, random_tree, complete.
    - graph size: The number of vertices in the largest graph to be tested.
    - step: The number of vertices to increase at each step.
    - mapper: The mapper to be compared with the random mapper.
    """

    results = []
    for i in range(10, graph_size + 1, step):
        if graph_type == "star":
            graph = nx.star_graph(i)
        elif graph_type == "line":
            graph = nx.path_graph(i)
        elif graph_type == "random_tree":
            random_seed = 10
            graph = nx.random_tree(i, seed=random_seed)
        elif graph_type == "complete":
            graph = nx.complete_graph(i)

        # Apply compiler with different mapper
        result_random = run_compiler(graph, random_mapper)
        result_min = run_compiler(graph, min_cut_mapper)
        result_nga = run_compiler(graph, mapper)

        # Append results to the list
        results.append(
            result_random[0:2]  # nodes
            + result_min[1:2]
            + result_nga[1:2]
            + result_random[2:3]
            + result_min[2:3]
            + result_nga[2:3]
            + result_random[3:4]
            + result_min[3:4]
            + result_nga[3:4]
        )

    # Save the results to a CSV file
    with open(
        f"results/{graph_type}_{graph_size}__{datetime.datetime.now()}.csv", "w", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(results)

    x = range(10, graph_size + 1, step)
    # plt.style.use("ggplot")
    # plt.figure(figsize=(12, 8))

    before = [x[0] for x in results]
    random = [x[1] for x in results]
    min_map = [x[2] for x in results]
    nga_map = [x[3] for x in results]
    weights = [x[7:10] for x in results]

    for i in range(len(min_map)):
        if min_map[i] < random[i]:
            newpath = f"results/{graph_type}"
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # Save the graphs that doesn't performs well
            plt.figure(figsize=(50, 30))
            plt.title("Random_Tree" + str(x[i]) + " nodes")

            # Get the new layout for the graph
            layout_random = results[i][4]
            layout_min_map = results[i][5]
            layout_nga_map = results[i][6]
            print(layout_random)
            print(layout_min_map)
            print(layout_nga_map)

            # Check for missing nodes in layouts
            for layout, layout_name in [
                (layout_random, "Random"),
                (layout_min_map, "Min Map"),
                (layout_nga_map, "NGA Map"),
            ]:
                missing_nodes_in_layout = set(graph.nodes) - set(layout)
                if missing_nodes_in_layout:
                    print(f"Missing nodes in {layout_name} layout:", missing_nodes_in_layout)

                # Check for extra nodes in layouts
                extra_nodes_in_layout = set(layout) - set(graph.nodes)
                if extra_nodes_in_layout:
                    print(f"Extra nodes in {layout_name} layout:", extra_nodes_in_layout)

            # Create label dictionaries based on the original graph
            labels_random = {node: str(node) for node in graph.nodes()}
            labels_min_map = {node: str(node) for node in graph.nodes()}
            labels_nga_map = {node: str(node) for node in graph.nodes()}

            # Convert graph to MultiDiGraph
            G = nx.MultiDiGraph(graph)
            # Create positions based on the layouts
            pos_random = {
                node: [layout_random.index(node), 1]
                for node in graph.nodes()
                if node in layout_random
            }
            pos_min_map = {
                node: [layout_min_map.index(node), 2]
                for node in graph.nodes()
                if node in layout_min_map
            }
            pos_nga_map = {
                node: [layout_nga_map.index(node), 3]
                for node in graph.nodes()
                if node in layout_nga_map
            }

            # Draw nodes using the new layouts
            valid_nodes_random = [node for node in G.nodes() if node in pos_random]
            valid_nodes_min = [node for node in G.nodes() if node in pos_min_map]
            valid_nodes_nga = [node for node in G.nodes() if node in pos_nga_map]
            nx.draw_networkx_nodes(
                G, pos_random, nodelist=valid_nodes_random, node_size=700, node_color="red"
            )
            nx.draw_networkx_nodes(
                G, pos_min_map, nodelist=valid_nodes_min, node_size=700, node_color="blue"
            )
            nx.draw_networkx_nodes(
                G, pos_nga_map, nodelist=valid_nodes_nga, node_size=700, node_color="green"
            )

            # Draw edges using the new layouts with curves
            for edge in graph.edges(data=True):
                edgelist = [(edge[0], edge[1])]
                print(edgelist)
                nx.draw_networkx_edges(
                    G,
                    pos_random,
                    edgelist=[edge],
                    connectionstyle="arc3, rad = 0.3",
                    arrowstyle="-",
                    edge_color="red",
                )
                nx.draw_networkx_edges(
                    G,
                    pos_min_map,
                    edgelist=[edge],
                    connectionstyle="arc3, rad = 0.3",
                    arrowstyle="-",
                    edge_color="blue",
                )
                nx.draw_networkx_edges(
                    G,
                    pos_nga_map,
                    edgelist=[edge],
                    connectionstyle="arc3, rad = 0.3",
                    arrowstyle="-",
                    edge_color="green",
                )

            # Use the labels dictionary for node labels
            nx.draw_networkx_labels(
                G, pos_random, labels=labels_random, font_size=22, font_color="whitesmoke"
            )
            nx.draw_networkx_labels(
                G, pos_min_map, labels=labels_min_map, font_size=22, font_color="whitesmoke"
            )
            nx.draw_networkx_labels(
                G, pos_nga_map, labels=labels_nga_map, font_size=22, font_color="whitesmoke"
            )
            y_offset = 0.5  # adjust this value as needed
            plt.text(
                -1,
                1 + y_offset,
                f"Random Mapper\nWeight: {results[i][7]}\nTimestep: {results[i][1]}",
                fontsize=20,
                ha="right",
            )
            plt.text(
                -1,
                2 + y_offset,
                f"Min Map Mapper\nWeight: {results[i][8]}\nTimestep: {results[i][2]}",
                fontsize=20,
                ha="right",
            )
            plt.text(
                -1,
                3 + y_offset,
                f"NGA Mapper\nWeight: {results[i][9]}\nTimestep: {results[i][3]}",
                fontsize=20,
                ha="right",
            )

            plt.savefig(
                f"results/{graph_type}/{graph_type}_{x[i]}_{datetime.datetime.now()}.png",
                dpi=300,
                bbox_inches="tight",
            )
            # Save the results to a CSV file
            with open(
                f"results/{graph_type}/{graph_type}_{x[i]}_{datetime.datetime.now()}.csv",
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)
                row = [
                    f"{graph_type}_{x[i]}_{datetime.datetime.now()}",
                    x[i],
                    min_map[i],
                    random[i],
                    weights[i],
                ]
                writer.writerow(row)


"""
    plt.plot(x, before, "+-", color=l_color[2], label="Origin Time Steps")
    plt.plot(x, random, "o-", color=l_color[0], label="Random Mapper")
    plt.errorbar(
        x,
        random,
        # yerr=[i for i in std_dev_random],
        color=l_color[0],
        capsize=4,
    )
    plt.plot(x, min_map, "*-", color=l_color[1], label="MinCut Mapper")
    plt.errorbar(
        x,
        min_map,
        # yerr=[i for i in std_dev_min],
        color=l_color[1],
        capsize=4,
    )
    plt.plot(x, nga_map, ">-", color=l_color[3], label="Naive General Algorithm")
    plt.errorbar(
        x,
        nga_map,
        # yerr=[i for i in std_dev_one],
        color=l_color[3],
        capsize=4,
    )

    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    plt.legend(loc="upper left")
    plt.savefig(f"results/{graph_type}_{graph_size}.png")
"""

test_by_kind("random_tree", graph_size=10, step=1, mapper=NGAopt_layout)
