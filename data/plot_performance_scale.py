import sys

sys.path.append("../")
import math
import numpy as np

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
    "axes.labelsize": 20,
    "axes.titlesize": 21,
    "xtick.labelsize": 17,
    "ytick.labelsize": 18,
    "legend.fontsize": 17,
}
plt.rcParams.update(paras)
plt.rcParams["font.sans-serif"] = ["Arial"]

l_color = [
    "#967AB6",
    "#82D1F4",
    "#E2CB8E",
    "#666469",
]


from networkx.algorithms.approximation import maximum_independent_set

warnings.filterwarnings("ignore", category=UserWarning)


def gen_erdos_renyi_graph_single_component(n, m, seed=51):
    if_connected = 0
    for i in range(5000):
        G = nx.gnm_random_graph(n, m, seed)
        if_connected = nx.number_connected_components(G)
        if if_connected == 1:
            break
    if if_connected == 1:
        return G
    else:
        return None


def test_random_tree(n,iterations=1,start_size=100,end_size=5000,step=100,mapper=min_cut_mapper,end_size_mapper=400):
    all_result = {}
    for num in range(0, iterations):
        result = []
        random_seed = 10
        for i in range(start_size,end_size, step):
            # graph=gen_erdos_renyi_graph_single_component(i,i * math.log(i),51+num)
            graph = gen_erdos_renyi_graph_single_component(i, i * i / math.log(i), 51 + num)

            compiler = TwoRowSubstrateScheduler(
                graph,
                pre_mapping_optimizer=fast_maximal_independent_set_stabilizer_reduction,
                node_to_patch_mapper=random_mapper,
                stabilizer_scheduler=greedy_stabilizer_measurement_scheduler,
            )
            compiler.run()
            if i < end_size_mapper:
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
            else:
                result.append(
                    [compiler.input_graph.number_of_nodes(), len(compiler.measurement_steps)]
                )
        all_result[num] = result
        # print(len(compiler.measurement_steps))
    with open(f"performance_scale_{end_size}.csv", "w", newline="") as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        for i in all_result.keys():
            writer.writerow(all_result[i])


def plot_from_csv():
    initial = []
    random = []
    min = []
    with open("scale_both.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            row_initial = []
            row_random = []
            row_min = []
            for i in row:
                li = list(i.split(","))
                if len(li) > 2:
                    row_initial.append(int(li[0].replace("[", "")))
                    row_random.append(int(li[1].replace(",", "")))
                    row_min.append(int(li[2].replace("]", "")))
                else:
                    row_initial.append(int(li[0].replace("[", "")))
                    row_random.append(int(li[1].replace("]", "")))
            initial.append(row_initial)
            random.append(row_random)
            min.append(row_min)
    sum_random = {}
    sum_min = {}
    avg_random = []
    avg_min = []
    var_random = {}
    var_min = {}
    for i in random:
        for j in range(len(i)):
            if j not in sum_random.keys():
                sum_random[j] = 0
            sum_random[j] += i[j]
    for i in min:
        for j in range(len(i)):
            if j not in sum_min.keys():
                sum_min[j] = 0
            sum_min[j] += i[j]

    for i in sum_min.keys():
        sum_min[i] = sum_min[i] / 10
    for i in sum_random.keys():
        sum_random[i] = sum_random[i] / 10

    for i in random:
        for j in range(len(i)):
            if j not in var_random.keys():
                var_random[j] = []
            var_random[j].append(i[j])
    for i in min:
        for j in range(len(i)):
            if j not in var_min.keys():
                var_min[j] = []
            var_min[j].append(i[j])

    for i in var_min.keys():
        var_min[i] = np.std(var_min[i])
    for i in var_random.keys():
        var_random[i] = np.std(var_random[i])
    # print(var_min)
    # print(var_random)
    x = range(100, 5000, 100)
    # density=[str(round(i/(100*(100-1)/2),2)) for i in x]
    # plt.style.use("ggplot")
    plt.figure(figsize=(8, 6))
    before = initial[0]
    spa = 100 * math.log(100)
    den = 100 * 100 / math.log(100)
    tre = [float(i) for i in sum_min.values()]

    plt.plot(x, before, "+-", color=l_color[2], label="Naive Time Steps")
    plt.plot(x, [float(i) for i in sum_random.values()], "o-", color=l_color[0], label="Random Mapper")
    # plt.errorbar(x, [float(i) for i in sum_random.values()], yerr = [float(i) for i in var_random.values()],color=l_color[0],capsize=4)
    plt.plot(x[0:3], tre[0:3], "*-", color=l_color[1], label="MinCut Mapper")
    # plt.errorbar(x[0:4], [float(i) for i in sum_min.values()], yerr = [float(i) for i in var_min.values()],color=l_color[1],capsize=4)

    # plt.axvline(500, color=l_color[3], linestyle='--', label='500 Vertices')
    plt.axvline(1000, color="r", linestyle="--", label="1000 Vertices")
    # plt.title("Performance Test on Different Graph Size")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Time step(s)")
    # plt.xticks(x,density)
    plt.legend(loc="lower right")
    # plt.grid(True)
    plt.savefig("scale_5000.png")
