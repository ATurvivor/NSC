from networks.generate_network import *
import pylab

def display_graph(G):
    """

    :param G:
    :return:
    """
    edge_colors = ['black' if not G.node[u]['infected'] and not G.node[v]['infected'] else 'red' for (u,v) in G.edges()]
    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos, edge_colors=edge_colors)
    pylab.show()

if __name__ == '__main__':
    G = star_graph()
    display_graph(G)