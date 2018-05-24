import random


def attack(graph):
    """
    Attacks random node
    :param graph:
    :return:
    """
    id = random.choice(graph.nodes())
    node = graph.node[id]
    p = random.random()

    if p < node['security']:
        graph.add_attribute(id, 'infected', 1)
        spread(node)

def spread(node):
    """
    Spreads infection from some infected node
    :param node:
    :return:
    """


    return 0