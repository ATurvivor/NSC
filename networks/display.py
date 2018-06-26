import networkx as nx

import matplotlib.pyplot as plt

def display_graph(G):
    """

    :param G:
    :return:
    """
    plt.ion()
    #plt.clf()
    #edge_colors = ['black' if not G.node[u]['infected'] and not G.node[v]['infected'] else 'red' for (u,v) in G.edges()]
    node_colors = [G.node[n]['node_color'] for n in G.nodes()]
    edge_colors = [G[u][v]['edge_color'] for u,v in G.edges()]
    pos = nx.layout.spring_layout(G)

    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors)
    edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='->', arrowsize=5, width=1)

    plt.plot()
    #plt.show(block=False)

    #nx.draw_networkx(G, pos, arrowstyle='->', node_colors='b',edge_colors=edge_colors)
    #plt.show()