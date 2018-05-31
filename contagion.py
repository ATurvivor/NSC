import random


def attack(graph):
    """
    Attacks random node
    :param graph:
    :return:
    """
    indices = random.sample(graph.nodes(), 3)
    nodes = [graph.node[n] for n in indices]
    graph.add_nodes_from(nodes, infected=1) # initially infected nodes

    #p = random.random()
    #if p < node['security']:
    spread()


def spread():
    """
    Spreads infection in network
    :return:
    """
    return 0