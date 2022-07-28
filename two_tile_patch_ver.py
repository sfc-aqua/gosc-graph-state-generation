#define min board size as 3n? n:number of nodes
#no ancilla so far

import numpy
#import heapq
import random
from create_random_graph import gen_erdos_renyi_graph_single_component
import find_order_stablizers as order
import warnings
import matplotlib.cbook
import copy
import math
import networkx as nx
import networkx.algorithms.approximation as nxaa

warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

"""
adj_list={
    "0":["1"],
    "1":["0","2"],
    "2":["1","3"],
    "3":["2"]
}
"""
time_stamp=0 #for gosc rules time step, not used for now

def read_adjacency(ad_list):
    # Read adjacency list as input in dictionary form
    stablizers_pair = []
    n=len(ad_list.keys())
    sorted_adja=sorted(ad_list.items())
    for i in sorted_adja:
        temp = [int(i[0])]
        for j in i[1]:
            temp.append(int(j))
        stablizers_pair.append(temp)
    return n, stablizers_pair

def create_stablizer(stablizer_pair):
    #create stablizers from adjacency of node [[node,nodes it connected to]...]
    stablizer_list=[]
    for i in range(len(stablizer_pair)):
        temp = ['I'] * len(stablizer_pair)
        temp[stablizer_pair[i][0]]='X'
        for j in range(1,len(stablizer_pair[i])):
            temp[stablizer_pair[i][j]]='Z'
        stablizer_list.append(temp)
    return stablizer_list

def create_board(r,c):
    #create logical qubits board of certain size r*c
    board=numpy.empty((r, c),dtype=object) #default as none
    return board

def create_qubits_index(col,row=0):
    #the logical qubit index on the board, for one line 2-tile-patche
    patch_index = {}
    num_index=col//2
    col_position = 0
    for i in range(num_index):
        patch_index[i]=[[row,col_position],[row,col_position+1]]
        col_position += 2
    return patch_index

def schedule_stablizers(operations):
    #shedule the order of applying the stablizers using minHeap
    heap=[]
    operation_steps=[]
    n = len(operations)

    sorted_start=sorted(operations, key=lambda x: min(x))
    sorted_stablizers=create_stablizer(sorted_start)

    order.heappush(heap, max(sorted_start[0]),operation_steps,[sorted_stablizers[0]])
    for i in range(1,n):
        if min(sorted_start[i])>heap[0]:
            print(min(sorted_start[i]),heap[0])
            operation_update=copy.deepcopy(operation_steps[0])
            operation_update.append(sorted_stablizers[i])
            print(operation_update)
            order.heappop(heap,operation_steps)
            #print(sorted_stablizers[i])
            order.heappush(heap, max(sorted_start[i]), operation_steps, operation_update)
        else:
            order.heappush(heap,max(sorted_start[i]),operation_steps,[sorted_stablizers[i]])
    return heap,operation_steps

def reduce_stablizers_by_plus(stablizers, max_indepen_nodes,mapping):
    for node in max_indepen_nodes:
        node_on_board=mapping[node]
        for i in stablizers:
            for j in i:
                if j[node]=='X':
                    i.remove(j)
            if i==[]:
                stablizers.remove([])

    reduced_num=len(stablizers)

    return reduced_num, stablizers

def map_to_device(board,qubits_num,qubits_index):
    # Use the simplest method: qubit 1 map to index 1 on board. mapping method tbd
    num_patch = 0
    pairs_id_index = {}
    for i in range(qubits_num):
        pairs_id_index[i] = i
        board[qubits_index[i][0][0]][qubits_index[i][0][1]] = i
        board[qubits_index[i][1][0]][qubits_index[i][1][1]] = i
        num_patch += 1
    return pairs_id_index, board, num_patch

def stablizer_to_device(operation_steps,pairs_id_index):
    #which stablizer to which qubit on devices, in scheduled order
    #too cumbersome
    stablizer_on_device={}

    for i in range(len(operation_steps)):
        stablizer_on_device[i] = {}
        for j in range(len(operation_steps[i])):
            for k in range(len(operation_steps[i][j])):
                if operation_steps[i][j][k]=='I':
                    continue
                else:
                    if pairs_id_index[k] not in stablizer_on_device[i].keys():
                        stablizer_on_device[i][pairs_id_index[k]]=[operation_steps[i][j][k]]
                    else:
                        stablizer_on_device[i][pairs_id_index[k]].append(operation_steps[i][j][k])
    return stablizer_on_device

def create_ancilla(board,operation_steps):
    board_step={}
    for i in range(0,len(operation_steps)):
        board_step[i] = copy.deepcopy(board)
        for j in operation_steps[i]:
            start=min(j.index('X'),j.index('Z'))
            end=max(len(j) - j[::-1].index('X') - 1,len(j) - j[::-1].index('Z') - 1)
            board_step[i][1][2*start:2 * end+2] = 'anc'
    return board_step

#run the compilation
def main(adj_list,n_nodes,graph):
    #n_nodes_ran=random.randint(100, 200)
    #n_edges_ran=random.randint(n_nodes_ran-1, math.floor(n_nodes_ran*(n_nodes_ran-1)/2/2))
    #G,adj_list_gen=gen_erdos_renyi_graph_single_component(n_nodes_ran,n_edges_ran)  #generate random graph for testing

    #the value for board, row and col here is just for understanding

    num_row=3
    num_col=2*n_nodes
    board=create_board(num_row,num_col)
    num_nodes,node_adj=read_adjacency(adj_list)
    patch_index=create_qubits_index(num_col)
    pairs_id_index, board, num_patch=map_to_device(board,num_nodes,patch_index)
    print(node_adj)
    #print(pairs_id_index)
    print("Before schedule stablizers: "+ str(num_nodes))
    num_step, operation_steps=schedule_stablizers(node_adj)
    print("Before set to plus state: "+ str(len(operation_steps)))
    print(operation_steps)
    #step to decide nodes which set to plus state
    #max_independent=nxaa.maximum_independent_set(graph) #return the an approximate maximum independent set
    #print("Maximum independent nodes: "+str(max_independent))
    #reduce_num,reduce_sta=reduce_stablizers_by_plus(operation_steps,max_independent,pairs_id_index)
    #print("After set to plus state: "+str(reduce_num))
    #print(reduce_sta)


    stablizer_on_qubits=stablizer_to_device(operation_steps,pairs_id_index)
    board_step=create_ancilla(board,operation_steps)
    return  len(num_step),num_nodes,adj_list,stablizer_on_qubits,board_step

if __name__ == '__main__':
    n_nodes_ran = random.randint(4, 8)
    n_edges_ran = random.randint(n_nodes_ran+1, math.floor((n_nodes_ran * (n_nodes_ran - 1)) / 2 / 1.5))

    adj_list_gen, graph = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_ran) #generate random graph for testing

    if adj_list_gen!=None:

        #run compilation
        num_step_scheduled,num_stablizers, adj_list_gen,stablizer_on_qubits, board_step=main(adj_list_gen,n_nodes_ran,graph )

        #num_step,num_nodes, adj_list_gen,stablizer_on_qubits,board_step =main()
        #print out the results
        #print("adjacency list:"+str(adj_list_gen))
        #print("number of step to implement stablizer: "+str(num_step_scheduled))
        #print("measurement on qubits to apply: "+str(stablizer_on_qubits))
        #print("number of patch:"+str(num_patch))
        #print("qubit allocation on device:\n"+str(board_step))
