"""The two-tile patch version for building arbitrary logical graph states based on a game of surface code"""

import numpy
import find_order_stablizers as order
import warnings
import matplotlib.cbook
import copy
import networkx as nx
import networkx.algorithms.approximation as nxaa
import min_cut

warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


class TwoTileVer():
    """
    attributes:

    ad_list: dictionary
    adjacency list of an arbitrary graph

    graph: NetworkX Graph

    time_stamp: int
    for gosc rules time step, not used for now

    num_node: int
    number of node in the graph

    stablizers_pair: list
    a list of the nodes in the graph with all the adjacent nodes,
    example: [[0, 1], [1, 0, 2, 3], [2, 1, 3], [3, 1, 2]]

    stablizer_list: list
    a list of stablizers to build the graph state represented in pauli operators X, Z and I,
    example: [['X', 'Z', 'I', 'I'], ['Z', 'X', 'Z', 'Z'], ['I', 'Z', 'X', 'Z'], ['I', 'Z', 'Z', 'X']]

    board: list
    the layout of the pre-sized device represented by logical qubits for constructing graph states

    patch_index: dictionary
    the index of the logical qubits and the physical qubits on the board
    example: {0: [[0, 0], [0, 1]], 1: [[0, 2], [0, 3]], 2: [[0, 4], [0, 5]], 3: [[0, 6], [0, 7]]}

    operation_steps: list
    list of scheduled stablizers, each element of the list represents the stablizer executed in the time step
    example: [[['X', 'Z', 'I', 'I']], [['Z', 'X', 'Z', 'Z']], [['I', 'Z', 'X', 'Z']], [['I', 'Z', 'Z', 'X']]]

    operation_steps_reduced:list
    a list of operations required to build the graph state after setting all nodes in the maximum independent set to
    plus state.
    example: [[['Z', 'X', 'Z', 'Z']], [['I', 'Z', 'X', 'Z']]]

    pairs_id_index: dictionary
    the dictionary where the keys are logical qubits and the values are virtual qubits.
    example: {0: 0, 1: 1, 2: 2, 3: 3}

    stablizer_on_device: dictionary
    the dictionary where the keys are time step and the values are the operator to be applied on logical qubits
    example: {0: {0: ['X'], 1: ['Z']}, 1: {0: ['Z'], 1: ['X'], 2: ['Z'], 3: ['Z']}, 2: {1: ['Z'], 2: ['X'], 3: ['Z']},
    3: {1: ['Z'], 2: ['Z'], 3: ['X']}}

    board_step: dictionary
    the dictionary where the keys are time step and the values are the layout of the board at that time step.
    """

    def __init__(
        self,
        ad_list,  #adjacency list of an arbitrary graph
        graph

    ):
        self.ad_list = ad_list
        self.graph = graph
        self.time_stamp= 0 #for gosc rules time step, not used for now
        self.cut_list = [self.ad_list.copy()] # tbd
        self.mapping=[]

    def read_adjacency(self):
        # Read adjacency list in dictionary form as input
        self.stablizers_pair = []
        self.num_node = len(self.ad_list.keys())
        sorted_adj = sorted(self.ad_list.items())
        for node, adj in sorted_adj:
            temp = [int(node)]
            for adj_node in adj:
                temp.append(int(adj_node))
            self.stablizers_pair.append(temp)

    def create_stablizer(self):
        #create stablizers from adjacency of node [[node,adjacent nodes]...]
        self.stablizer_list=[]
        for stablizer in range(len(self.stablizers_pair_reduced)):
            temp = ['I'] * len(self.stablizers_pair)
            temp[self.stablizers_pair_reduced[stablizer][0]]='X'
            for adj in range(1,len(self.stablizers_pair_reduced[stablizer])):
                temp[self.stablizers_pair_reduced[stablizer][adj]]='Z'
            self.stablizer_list.append(temp)

    def create_board(self,r,c):
        #create logical qubits board of certain size r*c
        self.board=numpy.empty((r, c),dtype=object) #default as none

    def create_patch_index(self, col,row=0):
        #the logical qubit index on the board, for one line 2-tile-patches
        self.patch_index = {}
        num_index=col//2
        col_position = 0
        for i in range(num_index):
            self.patch_index[i]=[[row,col_position],[row,col_position+1]]
            col_position += 2

    def schedule_stablizers(self):
        #shedule the order of applying the stablizers using minHeap
        heap=[]
        self.operation_steps=[]
        reverse_bits = {v: k for k, v in self.pairs_id_index.items()}
        for stablizer in self.stablizers_pair_reduced:
            for node in range(len(stablizer)):
                stablizer[node]=reverse_bits[stablizer[node]]
        self.stablizers_pair_reduced=sorted(self.stablizers_pair_reduced, key=lambda x: min(x))
        self.create_stablizer()

        order.heappush(heap, max(self.stablizers_pair_reduced[0]),self.operation_steps,[self.stablizer_list[0]])
        for stablizer in range(1,len(self.stablizers_pair_reduced)):
            if min(self.stablizers_pair_reduced[stablizer])>heap[0]:
                operation_update=copy.deepcopy(self.operation_steps[0])
                operation_update.append(self.stablizer_list[stablizer])
                order.heappop(heap,self.operation_steps)
                order.heappush(heap, max(self.stablizers_pair_reduced[stablizer]), self.operation_steps, operation_update)
            else:
                order.heappush(heap,max(self.stablizers_pair_reduced[stablizer]),self.operation_steps,[self.stablizer_list[stablizer]])


    def reduce_stablizers_by_plus(self, max_indepen_nodes):
        self.operation_steps_reduced=copy.deepcopy(self.operation_steps)
        for node in max_indepen_nodes:
            for step in self.operation_steps_reduced:
                for stablizer in step:
                    if stablizer[node]=='X':
                        step.remove(stablizer)
                if step==[]:
                    self.operation_steps_reduced.remove([])

        reduced_num=len(self.operation_steps)-len(self.operation_steps_reduced)
        return reduced_num

    def reduce_stablizers_by_plus_mo(self, max_indepen_nodes):
        self.stablizers_pair_reduced=copy.deepcopy(self.stablizers_pair)
        for node in max_indepen_nodes:
            for stablizer in self.stablizers_pair:
                if stablizer[0]==node:
                    self.stablizers_pair_reduced.remove(stablizer)
                if stablizer==[]:
                    self.stablizers_pair_reduced.remove([])
        reduced_num=len(self.stablizers_pair)-len(self.stablizers_pair_reduced)
        return reduced_num

    def map_to_device(self):
        # Use the simplest method: qubit 1 map to index 1 on board. mapping method tbd
        self.pairs_id_index = {}
        for i in range(self.num_node):
            self.pairs_id_index[i] = i
            self.board[self.patch_index[i][0][0]][self.patch_index[i][0][1]] = i
            self.board[self.patch_index[i][1][0]][self.patch_index[i][1][1]] = i

    def map_to_device_min(self):
        for component in range(len(self.cut_list)):
            if len(self.cut_list[component])>2:
                cut=min_cut.main(self.cut_list[component])
                for edge in cut:
                    self.cut_list[component][edge[0]].remove(edge[1])
                    self.cut_list[component][edge[1]].remove(edge[0])
                G = nx.Graph(self.cut_list[component])
                del self.cut_list[component]
                for c in nx.connected_components(G):
                    self.cut_list.append(nx.to_dict_of_lists(G.subgraph(c).copy()))
                return self.map_to_device_min()
            else:

                for node in self.cut_list[component].keys():
                    self.mapping.append(node)
                del self.cut_list[component]
                return self.map_to_device_min()
        self.pairs_id_index = {}
        for i in range(self.num_node):
            self.pairs_id_index[i] = self.mapping[i]
            self.board[self.patch_index[i][0][0]][self.patch_index[i][0][1]] = self.mapping[i]
            self.board[self.patch_index[i][1][0]][self.patch_index[i][1][1]] = self.mapping[i]

    def stablizer_to_device(self):
        #which stablizer to which qubit on devices, in scheduled order
        #too cumbersome
        self.stablizer_on_device={}

        for step in range(len(self.operation_steps)):
            self.stablizer_on_device[step] = {}
            for stablizer in range(len(self.operation_steps[step])):
                for operator in range(len(self.operation_steps[step][stablizer])):
                    if self.operation_steps[step][stablizer][operator]=='I':
                        continue
                    else:
                        if self.pairs_id_index[operator] not in self.stablizer_on_device[step].keys():
                            self.stablizer_on_device[step][self.pairs_id_index[operator]]=[self.operation_steps[step][stablizer][operator]]
                        else:
                            self.stablizer_on_device[step][self.pairs_id_index[operator]].append(self.operation_steps[step][stablizer][operator])

    def create_ancilla(self):
        self.board_step={}
        for step in range(0,len(self.operation_steps)):
            self.board_step[step] = copy.deepcopy(self.board)
            for stablizer in self.operation_steps[step]:
                start=min(stablizer.index('X'),stablizer.index('Z'))
                end=max(len(stablizer) - stablizer[::-1].index('X') - 1,len(stablizer) - stablizer[::-1].index('Z') - 1)
                self.board_step[step][1][2*start:2 * end+2] = 'anc'

    #run the compilation
    def run(self):
        self.read_adjacency()
        num_row=3
        num_col=2*self.num_node
        self.create_board(num_row,num_col)
        self.create_patch_index(num_col)
        self.map_to_device_min()
        #self.schedule_stablizers()
        max_independent=nxaa.maximum_independent_set(self.graph) #return the an approximate maximum independent set
        reduce_num=self.reduce_stablizers_by_plus_mo(max_independent)
        self.schedule_stablizers()
        self.stablizer_to_device()
        self.create_ancilla()


"""
graph = {0:[1],
         1: [0, 2, 3],
         2: [1, 3],
         3: [1, 2]}
G = nx.Graph(graph)
Job=TwoTileVer(ad_list=graph,graph=G)
Job.run()

"""






















