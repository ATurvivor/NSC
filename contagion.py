import random
from math import exp
from networks.network import Network
from ext import globals


def attack(G, nb_infections):
    """
    Attacks random node
    :param G: Graph
    :param nb_infections: Number of initially nb_infections nodes
    :return:
    """
    globals.gInfected = True
    infected_nodes = random.sample(G.nodes(), nb_infections)
    print('Initially infected nodes :', infected_nodes)
    G.add_nodes_from(infected_nodes, infected=1, state=1)  # initially nb_infections nodes
    while globals.gInfected:
        spread(G)
    G.display()


def spread(G):
    """
    Propagates information/infection in network
    :param G:
    :return:
    """
    infectious_state = [n for (n, state) in G.nodes(data='state') if state == 1] # get nodes in infectious state
    print('Nodes in infectious state :', infectious_state)
    if not infectious_state:
        print('No more nodes in infectious state. END.')
        globals.gInfected = False
        return

    for u in infectious_state: # for each currently infected node
        neighbors = [n for n in G[u] if G.node[n]['state'] == 0] # neighbors in susceptible state
        # print('neighbors ', neighbors)
        for v in neighbors:  # for each neighbor
            if random.uniform(0, 1) < calculate_transmissibility(G,u,v):
                if infect_node(G.node[v]['security']):
                    G.node[v]['infected'] = 1
                    G.node[v]['state'] = 1 # infectious state
        update_infectious_time(G, u)


def calculate_transmissibility(G,u,v):
    """
    Calculates transmissibility probability
    :param G:
    :param u:
    :param v:
    :return:
    """
    return 1.0 / len(G)
    #return 1 - exp(G[u][v]['rate'], G.node[u]['infectious_time'])


def infect_node(security_inv):
    """
    Returns True if node gets infected, False otherwise
    :param probability:
    :return:
    """
    if random.uniform(0, 1) < security_inv:
        return 1
    return 0


def update_infectious_time(G, n):
    """
    Update infectious time and current state, if applicable
    :param G:
    :param G:
    :return:
    """
    G.node[n]['infectious_time'] -= 1
    if G.node[n]['infectious_time'] == 0:  # if end of infectious state
        G.node[n]['infectious_time'] = G.node[n]['initial_infectious_time']
        G.node[n]['state'] = 2  # recovered state

if __name__ == '__main__':
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    edges = [(1, 2), (1, 6), (3, 2), (3, 4), (3, 8), (4, 7), (7, 8), (7, 9), (7, 10)]
    security_investment = {1: 0.7, 2: 0.6, 3: 0.5, 4: 0.8, 5: 0.8, 6: 0.75, 7: 0.78, 8: 0.9, 9: 0.45, 10: 0.93}
    N = Network(nodes, edges)
    N.set_security_investments(security_investment)
    attack(N, nb_infections=1)
