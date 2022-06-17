import pylab
import networkx as nx

def gen_erdos_renyi_graph_single_component(n, m):
    G = nx.gnm_random_graph(n, m)
    if nx.number_connected_components(G) == 1:
        nx.draw(G)
        #pylab.show()
        return G,nx.to_dict_of_lists(G)
    else:
        return gen_erdos_renyi_graph_single_component(n, m)