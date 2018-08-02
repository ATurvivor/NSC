import graph_tool.all as gt
from itertools import chain
from networks.construct_network import *

def random_graph_with_clustering(nodes, ps, pt):
    G = Network(nodes)
    stubs, corners = [ps() for _ in range(nodes)], [pt() for _ in range(nodes)]

    stubs[0] += sum(stubs) % 2
    corners[0] += sum(corners) % 3

    stubs = list(chain.from_iterable([n]*d for n, d in enumerate(stubs)))
    corners = list(chain.from_iterable([n]*d for n, d in enumerate(corners)))

    random.shuffle(stubs)
    random.shuffle(corners)

    n, t1, t2 = len(stubs)//2, len(corners)//3, 2*(len(corners)//3)
    stubs1, stubs2 = stubs[:n], stubs[n:]
    corners1, corners2, corners3 = corners[:t1], corners[t1:t2], corners[t2:]

    G.add_edge_list(zip(stubs1, stubs2))
    G.add_edge_list(zip(corners1, corners2))
    G.add_edge_list(zip(corners1, corners3))
    # gt.remove_self_loops(G)

    G._default_properties()

    return G

def chung_lu_model(nodes, degree_seq):
    G = gt.random_graph(nodes, degree_seq, directed=False)
    return Network.from_graph(G)

def barabasi_albert_model(nodes, m=1):
    G = gt.price_network(nodes, m=m, directed=False)
    return Network.from_graph(G)

def star_graph(nodes):
    """
    Returns a star graph
    :param nodes: Number of nodes
    :return:
    """
    G = Network(nodes)
    source = G.vertex(0)
    G.add_edge_list([(source, i) for i in G.vertices() if i != source])
    return G