import random
import networkx as nx

from networks.network import Network
from properties import globals
from math import exp


def attack(G, init_infections, model='SIR'):
    """
    Attacks random node
    :param G: Graph
    :param init_infections: Number of initially init_infections nodes
    :param model: Propagation model
    :return:
    """
    infected_nodes = random.sample(G.nodes(), init_infections)
    if globals.gDebug:
        print('Initially infected nodes :', infected_nodes)
    att = {n : {'infected' : 1, 'state' : 1} for n in infected_nodes}
    nx.set_node_attributes(G, att)  # initially init_infections nodes
    while globals.gInfected:
        spread(G, model=model)
    if globals.disp_graph:
        G.display()


def spread(G, model='SIR'):
    """
    Propagates information/infection in network
    :param G:
    :param model:
    :return:
    """
    infectious_state = [n for (n, state) in G.nodes(data='state') if state == 1] # get nodes in infectious state
    recovered_state = [n for (n, state) in G.nodes(data='state') if state == 2] # get nodes in recovered state

    #print('Nodes in infectious state :', [(n, G.nodes[n]['infectious_time']) for n in infectious_state])
    if globals.gDebug:
        print('Nodes in infectious state :', infectious_state)
        #print('Nodes in recovered state :', recovered_state)
    if not infectious_state:
        print('No more nodes in infectious state. END.')
        print('Final size of outbreak : ' + str(G.compute_final_size()) + ' / ' + str(len(G.nodes())) + ' nodes.')
        globals.gInfected = False
        return

    # SIRS case : at the end of recovered state, cycle back to susceptible state
    if model == 'SIRS':
        for u in recovered_state:
            update_recovered_time(G, u)

    for u in infectious_state: # nodes in infectious state
        neighbors = [n for n in G[u] if G.node[n]['state'] == 0] # neighbors in susceptible state
        # print('neighbors ', neighbors)
        for v in neighbors:  # for each neighbor
            if random.uniform(0, 1) < calculate_transmissibility(G, u, v):
                if infect_node(G.node[v]['security']):
                    G.node[v]['state'] = 1 # infectious state
                    G.node[v]['infected'] = 1
        update_infectious_time(G, u, model=model)


def calculate_transmissibility(G,u,v):
    """
    Calculates transmissibility probability
    :param G: Graph
    :param u: Node
    :param v: Node
    :return:
    """
    #return 1.0 / len(G)
    return 1 - exp(-G[u][v]['rate'] * G.node[u]['infectious_time'])


def infect_node(security_inv):
    """
    Returns True if node gets infected, False otherwise
    :param security_inv:
    :return:
    """
    if random.uniform(0, 1) < security_inv:
        return 0
    return 1


def update_infectious_time(G, n, model='SIR'):
    """
    Update infectious time and current state, if applicable
    :param G:
    :param n:
    :param model:
    :return:
    """
    G.node[n]['infectious_time'] -= 1
    if G.node[n]['infectious_time'] == 0:  # if end of infectious state
        G.node[n]['infectious_time'] = G.node[n]['initial_infectious_time']
        if model == 'SIS':
            G.node[n]['state'] = 0 # susceptible state
        else:
            G.node[n]['state'] = 2  # recovered state


def update_recovered_time(G, n):
    """

    :param G:
    :param n:
    :return:
    """
    G.node[n]['recovered_time'] -= 1
    if G.node[n]['recovered_time'] == 0:  # if end of infectious state
        G.node[n]['recovered_time'] = G.node[n]['initial_recovered_time']
        G.node[n]['state'] = 0 # susceptible state


if __name__ == '__main__':
    # nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # edges = [(1, 2), (1, 6), (3, 2), (3, 4), (3, 8), (4, 7), (7, 8), (7, 9), (7, 10)]
    # security_investment = {1: 0.7, 2: 0.6, 3: 0.5, 4: 0.8, 5: 0.8, 6: 0.75, 7: 0.78, 8: 0.9, 9: 0.45, 10: 0.93}
    # N = Network(nodes, edges)
    # N.set_security_investments(security_investment)
    # attack(N, nb_infections=1)
    n,m = 100,2
    N = Network.from_graph(nx.barabasi_albert_graph(n,m))
    security_investment = {x : random.random() for x in range(n)}
    N.set_security_investments(security_investment)
    print(N.nodes(data=True))
    attack(N, init_infections=1)
