import graph_tool.all as gt
from itertools import chain
from networks.construct_network import *

def random_graph_with_clustering(nodes, ps, pt, defaults=True, model='SIR', threshold='relative'):
    """
    Generates a random graph with clustering based on Newman's model
    :param nodes: Number of vertices in the graph
    :param ps: function that draws from the stub distribution
    :param pt: function that draws from triangle corner distribution
    :return:
    """
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
    
    if defaults is True:
        G._default_properties()
    else:
        G.gp['model'] = model
        G.gp['threshold'] = threshold

    return G

def chung_lu_model(nodes, degree_seq, defaults=True, model='SIR', threshold='relative'):
    """
    Generates a graph based on the chung lu model
    :param nodes: Number of vertices in the graph
    :param degree_seq: Function that takes in no arguments and samples from a distribution for degree sequence
    """
    G = gt.random_graph(nodes, degree_seq, directed=False)
    return Network.from_graph(G, defaults=defaults, model=model, threshold=threshold)

def barabasi_albert_model(nodes, m=1, defaults=True, model='SIR', threshold='relative'):
    """
    Generates a graph based on the barabasi albert model
    :param nodes: Number of vertices in the graph
    :param m: Initial seed for number of connections per iteration
    """
    G = gt.price_network(nodes, m=m, directed=False)
    return Network.from_graph(G, defaults=defaults, model=model, threshold=threshold)

def star_graph(nodes, defaults=True, model='SIR', threshold='relative'):
    """
    Returns a star network object
    :param nodes: Number of nodes
    :return:
    """
    edges = [(0, i) for i in range(1, nodes)]
    return Network(nodes, edges, defaults=defaults, model=model, threshold=threshold)

def layer_graphs(g1, g2):
    """
    Layers 2 graphs together and creates edges between nodes with the same ID (assumes sorted IDs)
    :param g1: First network
    :param g2: Second network
    :return g3: Layered network
    """
    g1.vp['layer'].a = 1 # TODO increment layer instead ?
    g2.vp['layer'].a = 2
    g1Size, g2Size = g1.num_vertices(), g2.num_vertices()
    g3 = gt.graph_union(g1, g2, internal_props=True)
    i, j = 0, g2Size
    while True:
        print(i,j)
        if i > g2Size-1 or j > g3.num_vertices()-1:
            break
        if g3.vp['id'][i] == g3.vp['id'][j]:
            e = g3.add_edge(i, j)
            # TODO Add a rate for these newly added edges
            # g3.ep['rate'][e] = random.random()
            i += 1
            j += 1
        else:
            if g3.vp['id'][i] > g3.vp['id'][j]:
                j += 1
            else:
                i += 1

    return g3
