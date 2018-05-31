import networkx as nx
import numpy as np

from cost_functions import *
from extras import *


class Network(nx.DiGraph):
    def __init__(self, nodes, edges):
        """

        :param nodes: list of indices of nodes
        :param edges: list of edges
        :return:
        """
        nx.DiGraph.__init__(self)
        self.add_nodes_from(nodes, utility=0, value=0, infected=0)
        self.add_edges_from(edges)
        self.security_profile = {n: 0 for n in self.nodes()}
        self.attack_decision = {n: 0 for n in self.nodes()}

    def set_attack_decision(self, attack_decision):
        """
        Set attack decision
        :param attack_decision: dictionary
        :return:
        """
        self.attack_decision = attack_decision

    def set_security_profile(self, security_profile):
        """
        Set security investments
        :param security_investments: dictionary containing agent ids : security investment
        :return:
        """
        for n, value in security_profile.items():
            try:
                self.node[n]['security'] = value
                self.security_profile[n] = value
            except KeyError as error:
                pass
                print('KeyError : Agent with id #' + str(error) + ' does not exist.')

    def get_security_profile(self):
        """
        Return security profile
        :return:
        """
        self.security_profile = {n : self.node[n]['security'] for n in self.nodes()}
        return self.security_profile

    def reset_security_profile(self):
        """
        Reset security profile
        :return:
        """
        self.security_profile = dict.fromkeys(self.security_profile, 0)

    def compute_network_effect(self, i):
        """
        Calculates probability of infection reaching agent i
        :param N: Network
        :param i: Target node
        :return:
        """
        # TODO check probability
        qi = self.node[i]['security']
        r_prob = 0
        for node in self.nodes():
            for path in nx.all_simple_paths(self, source=node, target=i):
                source = path[0]
                r_prob += self.attack_decision[source] * prod([(1 - self.node[j]['security']) for j in path[:-1]])

        return (1 - qi) * r_prob

    def compute_utility(self):
        """
        Computes utility for each agent
        :return:
        """
        for n in self.nodes():
            node = self.node[n]
            node['utility'] = node['value'] * (1 - self.compute_network_effect(n)) - default_cost(node['security'])

    def compute_social_welfare(self):
        """
        Computes social welfare
        :return:
        """
        return sum([self.node[i]['utility'] for i in self.nodes()])

    def compute_nash_eq(self):
        """
        Computes Nash equilibrium
        :return:
        """
        return 0

    def compute_social_opt(self):
        """
        Computes social optimum of network
        :return:
        """
        return 0

    def compute_cost(self, n, function=default_cost):
        """
        Computes cost of security investment of node id
        :param function: cost function
        :param n: node n
        :return: Returns cost
        """
        return function(self.node[n]['security'])

    def expected_nbInfections(self):
        """
        Computes the expected number of infections
        :return:
        """
        n = self.number_of_nodes()
        # TODO : modify depending on attack strategy
        return 1.0 / n * sum(1 - np.asarray(self.security_profile.values()))

    def get_transmission_network(self):
        """
        Returns corresponding transmission network
        :return:
        """
        transmission_network = self.copy()
        nodes = [n for n in self.nodes() if self.node[n]['security'] == 1]
        transmission_network.remove_nodes_from(nodes)
        return transmission_network
