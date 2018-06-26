from networks.generate_network import *
from computations import *


def test_run():
    G = Network([i for i in range(5)], [(1,2), (3,4)])
    G.set_security_investments({0 : 0.2, 1 : 1, 2 : 1, 3 : 1, 4 : 1})

    print('Nodes : ' + str(G.nodes(data=True)))

    print('Security investment cost for node 0: ' + str(G.compute_cost(0)))
    print('Security investment for node 2 : ' + str(G.node[2]['security']))
    print('Security profile : ' + str(G.get_security_profile()))
    G.compute_utility()
    print('Social welfare : ' + str(G.compute_social_welfare()))

    #print(G.get_transmission_network())

    G.set_security_investments({2 : 0.5, 3 : 0.4, 6 : 0.2})

    print('Security investment for node 2 : ' + str(G.node[2]['security']))
    print('Security profile : ' + str(G.get_security_profile))


def utilities():
    """
    Compute utilities
    :return:
    """
    G = star_graph()
    G.set_security_investments({1 : 0.2, 2 : 1, 3 : 1, 4 : 1, 5 : 1})
    G.compute_utility()
    print(G.nodes(data=True))

def expectation():
    """
    Compute expectation
    :return:
    """
    N = star_graph()
    nodes = N.nodes()
    attack_decision = {n : 1.0/len(nodes) for n in nodes}
    qe = {1 : 0.2, 2 : 1, 3 : 1, 4 : 1, 5 : 1}
    #qs = {1 : 1, 2 : 0.2, 3 : 0.2, 4 : 0.2, 5 : 0.2}

    N.set_security_investments(qe)
    N.set_attack_decision(attack_decision)

    print(expected_nb_infections(N))


def network_effect():
    """
    Compute network effect
    :return:
    """
    nodes = [1,2,3]
    edges = [(1,2), (3,2)]
    security_investment = {1 : 0.3, 2 : 0.2, 3 : 0.5}
    attack_decision = {1 : 1.0/3, 2 : 1.0/3, 3 : 1.0/3}

    N = Network(nodes, edges)
    N.set_security_investments(security_investment)
    N.set_attack_decision(attack_decision)

    print('Network effect on node 2 : ' + str(N.compute_network_effect(2)))
    #for n in nodes:
    #    print('Network effect on node ' + str(n) + ' : ' + str(N.compute_network_effect(n)))

if __name__ == '__main__':
    #utilities()
    #test_run()
    #network_effect()
    expectation()