import random
import copy
import time


def contract(ver, e):
    while len(ver) > 2:  # create a new graph every time (not efficient)
        ind = random.randrange(0, len(e))
        [u, v] = e.pop(ind)  # pick a edge randomly
        ver.remove(v)  # remove v from vertices
        newEdge = list()
        for i in range(len(e)):
            if e[i][0] == v:
                e[i][0] = u
            elif e[i][1] == v:
                e[i][1] = u
            if e[i][0] != e[i][1]: newEdge.append(e[i])  # remove self-loops
        e = newEdge
    return (len(e))  # return the number of the remained edges


if __name__ == '__main__':
    """f = open('kargerMinCut.txt')
    _f = list(f)
    edges = list()  # initialize vertices and edges
    vertices = list()
    for i in range(len(_f)):  # got 2517 different edges
        s = _f[i].split()"""
    graph = {1: [2, 3],
             2: [1, 3],
             3: [1, 2],
             }
    vertices = list()
    edges = list()  # initialize vertices and edges
    vertices.append(graph.keys())
    for i in graph.values():
        for j in i:
            if [int(s[j]), int(s[0])] not in edges:
                edges.append([int(s[0]), int(s[j])])

    result = list()
    starttime = time.clock()
    for i in range(2000):  # we take n^2logn times so that the Pr(allfail) <= 1/n where n is the number of vertics
        v = copy.deepcopy(vertices)  # notice: deepcopy
        e = copy.deepcopy(edges)
        r = contract(v, e)
        result.append(r)
    endtime = time.clock()
    # print(result)
    print(min(result))
    print(endtime - starttime)