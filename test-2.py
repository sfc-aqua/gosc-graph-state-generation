import two_tile_patch_ver as twotile
import time
import random
import math
from create_random_graph import gen_erdos_renyi_graph_single_component

time_compilation=0 #compilation timer
result=[]
num_op=0
total_stablizers=0 #total steps of applying stablizers without optimization
total_optimzed_stablizers=0 #total steps of applying stablizers with optimization

for i in range(1000):
    n_nodes_ran = random.randint(100, 200)

    #generate sparse graph
    #n_edges_ran = random.randint(n_nodes_ran+10, math.floor((n_nodes_ran * (n_nodes_ran - 1))/ 2 / 2))

    #generate dense graph
    n_edges_ran = random.randint(math.floor((n_nodes_ran * (n_nodes_ran - 1))/ 2 / 2),(n_nodes_ran * (n_nodes_ran - 1))/ 2)

    adj_list_gen = gen_erdos_renyi_graph_single_component(n_nodes_ran, n_edges_ran)  #generate random graph for testing

    if adj_list_gen!=None:
        time_start = time.time()
        #run compilation
        num_step_scheduled,num_stablizers, adj_list_gen,stablizer_on_qubits,board_step=twotile.main(adj_list_gen,n_nodes_ran )

        total_stablizers += num_stablizers
        total_optimzed_stablizers +=num_step_scheduled

        if num_step_scheduled< num_stablizers:
            print("After scheduling: "+str(num_step_scheduled)+ " Before scheduling: "+ str(num_stablizers))
            num_op+=1
        result.append([num_step_scheduled, num_stablizers])
        time_end = time.time()
        time_compilation += time_end-time_start

print("Percentage of optimized after scheduing= "+str(num_op))
print(str(total_optimzed_stablizers)+" of "+str(total_stablizers))
print("time cost", time_compilation,'s')