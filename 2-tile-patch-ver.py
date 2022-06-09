#define min board size as 3n? n:number of nodes

import numpy
import heapq

time_stamp=0 #for gosc rules time step, not used for now
#the value for board, row and col here is just for understanding
num_row=6
num_col=6

adj_list={
    "0":["1"],
    "1":["0","2"],
    "2":["1","3"],
    "3":["2"]
}

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
    board=numpy.zeros((r, c))
    return board

def create_qubits_index(col,board,row=0):
    #the logical qubit index on the board, for one line 2-tile-patche
    num_index=col//2
    for i in range(num_index):
        patch_index[i]=[[row,col],[row,col+1]]
        col += 2
    return patch_index

def schedule_stablizers(operations):
    #shedule the order of applying the stablizers using minHeap
    heap=[]
    operation_steps=[]
    n = len(operations)
    step=0

    sorted_start=sorted(operations, key=lambda x: min(x))
    sorted_stablizers=create_stablizer(sorted_start)
    heapq.heappush(heap,max(sorted_start[0]))
    operation_steps.append([sorted_stablizers[0]])

    for i in range(1,n):
        if min(sorted_start[i])>heap[0]:
            heapq.heappop(heap)
            operation_steps[0].append(sorted_stablizers[i])
            operation_steps.append(operation_steps.pop(0))
        else:
            step+=1
            operation_steps.append([sorted_stablizers[i]])
        heapq.heappush(heap,max(sorted_start[i]))
    return heap,operation_steps

patch_index={}
pairs_id_index={}
def map_to_device(qubits_num,qubits_index):
    # Use the simplest method: qubit 1 map to index 1 on board. mapping method tbd
    num_patch = 0
    for i in range(qubits_num):
        pairs_id_index[i] = i
        board[qubits_index[i][0]] = i
        board[qubits_index[i][1]] = i
        num_patch += 1
    return pairs_id_index, board, num_patch

#run the compilation
board=create_board(num_row,num_col)
num_nodes,node_adj=read_adjacency(adj_list)
num_step, operation_steps=schedule_stablizers(node_adj)
#map_to_device(num_nodes,)

#print out the results
print("number of step to implement stablizer: "+str(len(num_step)))
print("order of apply stablizers: "+str(operation_steps))