import networkx as nx
import random

Graph_Adjacency_List = "***.txt"
handle = open(Graph_Adjacency_List, 'r')
G=nx.read_adjlist(handle,create_using=nx.MultiGraph(), nodetype=int)

def cut(G):
    while G.number_of_nodes()>2 :
        u,v= random.choice(G.edges())
        G = nx.contracted_edge(G, (u, v), self_loops=False)
    return G.number_of_edges()

m=100
for i in range(1000):
    random.seed()
    c=cut(G)
    if c< m:
        m=c
        print m