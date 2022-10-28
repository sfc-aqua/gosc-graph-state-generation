import math
import random
import re
import time

from graph_state_generation.two_tile_patch import TwoTileVer

from .create_random_graph import gen_erdos_renyi_graph_single_component

time_compilation=0 #compilation timer
result=[]
num_op=0
total_stablizers=0 #total steps of applying stablizers without optimization
total_optimzed_stablizers=0 #total steps of applying stablizers with optimization

for i in range(1):
    n_nodes_ran = random.randint(5, 8)

    #generate sparse graph
    n_edges_ran = random.randint(n_nodes_ran+3, math.floor((n_nodes_ran * (n_nodes_ran - 1))/ 2 / 2))

    #generate dense graph　
    #n_edges_ran = random.randint(math.floor((n_nodes_ran * (n_nodes_ran - 1))/ 2 / 2),(n_nodes_ran * (n_nodes_ran - 1))/ 2)

    adj_list_gen, graph = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_ran)  #generate random graph for testing

    time_start = time.time()
    if adj_list_gen!=None:

        #run compilation

        Job = TwoTileVer(ad_list=adj_list_gen, graph=graph)
        Job.run()
        print("After scheduling: " + str(len(Job.operation_steps)) + " Before scheduling: " + str(Job.num_node))
        #print("Adjacent list: "+str(len(Job.ad_list)))
        #print("Mapping"+str(Job.pairs_id_index))
        #print("time step"+str(len(Job.operation_steps)))
        #print(operationJob.operation_steps_reduced)

    time_end = time.time()
    time_compilation += time_end-time_start

print(time_compilation)
