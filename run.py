from networks.network import *
from networks.contagion import attack
from properties.properties import *


def network_effect():
    """
    Compute network effect
    :return:
    """
    nodes = [1,2,3]
    edges = [(1,2), (3,2)]
    security_inv = {1 : 0.3, 2 : 0.2, 3 : 0.5}
    attack_decision = {1 : 1.0/3, 2 : 1.0/3, 3 : 1.0/3}

    N = Network(nodes, edges)
    N.set_security_investments(security_inv)
    N.set_attack_decision(attack_decision)

    print('Network effect on node 2 : ' + str(N.compute_network_effect(2)))

if __name__ == '__main__':
    properties = read_properties('properties/test.properties')
    set_properties(properties)

    n,m = 5,2
    N = Network.from_graph(nx.barabasi_albert_graph(n,m))
    security_investment = {x : random.random() for x in range(n)}
    N.set_security_investments(security_investment)
    if globals.gDebug:
        print(N.nodes(data=True))
    attack(N, init_infections=1, model='SIRS')