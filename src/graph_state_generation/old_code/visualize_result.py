import math
import numbers
import random

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tests.graph_state_generation.create_random_graph import (
    gen_erdos_renyi_graph_single_component,
)

from old_version import two_tile_patch_ver as twotile

n_nodes_ran = random.randint(3, 5)

row=3
col=2*n_nodes_ran
# generate sparse graph
n_edges_ran = random.randint(n_nodes_ran, math.floor((n_nodes_ran * (n_nodes_ran - 1))/ 2 / 2))

adj_list_gen = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_ran)  #generate random graph for testing

if adj_list_gen != None:
    # run compilation
    num_step_scheduled, num_stablizers, adj_list_gen, stablizer_on_qubits, board_step = twotile.main(adj_list_gen, n_nodes_ran)
    print(num_step_scheduled)
    print(num_stablizers)

def saveImage(p,step):
    filename = '../code_visualization/' + str(step) + '.png'
    p.savefig(filename)

for step in range(0,num_step_scheduled):
    plt.figure(figsize=(10, 5))

    ax = plt.gca()
    ax.set_xlim([0, col])
    ax.set_ylim([0, row])

    step_of_board = board_step[step]
    operation_step = stablizer_on_qubits[step]
    for i in range(0, row):
        row_board=step_of_board[i]
        for j in range(0, col):
            if isinstance(row_board[j],numbers.Number):
                # for qubits
                qubit_id=row_board[j]
                if qubit_id in operation_step.keys():
                    operation=operation_step[qubit_id]
                    if operation==['Z']:
                        rec = Rectangle((j, row - i - 1), width=1, height=1, facecolor='r', edgecolor="gray")
                    if operation==['X']:
                        rec = Rectangle((j, row - i - 1), width=1, height=1, facecolor='y', edgecolor="gray")
                    plt.text(j + 0.5, row - i - 1 + 0.5, (row_board[j],operation),fontweight='bold', fontsize=7.5, verticalalignment="center",
                             horizontalalignment="center")
                else:
                    rec = Rectangle((j, row - i - 1), width=1, height=1, facecolor='b', edgecolor="gray")
                    plt.text(j + 0.5, row - i-1 + 0.5, row_board[j], fontsize=7.5, verticalalignment="center", horizontalalignment="center")
                ax.add_patch(rec)

            if row_board[j] == None:
                # for unassigned tiles
                rec = Rectangle((j, row - i-1), width=1, height=1, facecolor='w', edgecolor="gray")
                #print(rec)
                ax.add_patch(rec)
            if row_board[j] == 'anc':
                # for ancilla patch
                rec = Rectangle((j, row -i-1), width=1, height=1, facecolor='gray', edgecolor="gray")
                #print(rec)
                ax.add_patch(rec)

    plt.title("step %s / %s" % (step, num_step_scheduled), fontsize='15', fontweight='bold', y=-0.03)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    saveImage(plt,step)
