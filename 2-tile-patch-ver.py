#define min board size as 3n? n:number of nodes

import read_input as rd
import numpy
import heapq

time_stamp=0
patch_index={}
pairs_id_index={}
#the value for board, row and col here is just for understanding
num_row=6
num_col=6
stablizers_pair=[]


#Read adjacency list as input in dictionary form
def read_adjacency(ad_list):
    n=len(ad_list.keys())
    sorted_adja=sorted(ad_list.items())
    for i in sorted_adja:
        temp = [int(i[0])]
        for j in i[1]:
            temp.append(int(j))
        stablizers_pair.append(temp)
    return n, stablizers_pair

def create_stablizer(stablizer_pair):
    stablizer_list=[]
    for i in range(len(stablizer_pair)):
        temp = ['I'] * len(stablizer_pair)
        temp[stablizer_pair[i][0]]='X'
        for j in range(1,len(stablizer_pair[i])):
            temp[stablizer_pair[i][j]]='Z'
        stablizer_list.append(temp)

    return stablizer_list

adj_list={
    "0":["1"],
    "1":["0","2"],
    "2":["1","3"],
    "3":["2"]
}

def create_board(r,c):
    board=numpy.zeros((r, c))
    return board

def create_qubits_index(col,board,row=0):
    num_index=col//2
    for i in range(num_index):
        patch_index[i]=[[row,col],[row,col+1]]
        col += 2
    return patch_index


def schedule_stablizers(operations):
    print(operations)
    heap=[]
    starttime = [min(i) for i in operations]
    endtime=[max(i) for i in operations]
    heapq.heappush(heap,endtime[0])
    n=len(operations)
    for i in range(1,n):
        if min(operations[i])>heap[0]:
            heapq.heappop(heap)
        heapq.heappush(heap,max(operations[i]))
    return heap

#Use the simplest method for now. mapping method tbd
def map_to_device(qubits_num,qubits_index):
    num_patch = 0
    for i in range(qubits_num):
        pairs_id_index[i] = i
        board[qubits_index[i][0]] = i
        board[qubits_index[i][1]] = i
        num_patch += 1
    return pairs_id_index, board, num_patch

board=create_board(num_row,num_col)
n,num_nodes=read_adjacency(adj_list)
num_step=schedule_stablizers(num_nodes)
print(num_step)
print(adj_list)
print(create_stablizer(num_nodes))
print("number of step to implement stablizer: "+str(len(num_step)))