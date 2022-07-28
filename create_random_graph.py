import pylab
import networkx as nx


"""
def gen_erdos_renyi_graph_single_component(n, m):
    G = nx.gnm_random_graph(n, m)
    if nx.number_connected_components(G) == 1:
        nx.draw(G)
        #pylab.show()
        #print(n,m)

        #return NetworkX graph and adjacency list
        return G,nx.to_dict_of_lists(G)
    else:
        return gen_erdos_renyi_graph_single_component(n, m)
"""

def gen_erdos_renyi_graph_single_component(n, m):
    if_connected=0
    for i in range(1000):
        G = nx.gnm_random_graph(n, m)
        if_connected=nx.number_connected_components(G)
        if if_connected == 1:
            nx.draw(G)
            #pylab.show()
            #pylab.savefig('./img/' + 'graphtest' + '.png')
            #return adjacency list
            break
    if if_connected==1:
        return nx.to_dict_of_lists(G),G
    else:
        return None
