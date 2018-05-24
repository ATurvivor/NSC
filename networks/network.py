import networkx as nx
import numpy as np

from scipy.optimize import fmin
from copy import copy
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
        self.add_nodes_from(nodes)
        self.add_edges_from(edges)

        self.security_profile = {}
        self.attack_decision = {}

        self.init_params()

    def init_params(self):
        """
        Initialise parameters
        :return:
        """
        self.init_security_profile()
        self.init_attack_decision()
        self.init_attributes()

    def init_security_profile(self):
        for n in self.nodes():
            self.node[n]['security'] = 0
            self.security_profile[n] = 0

    def init_attack_decision(self):
        self.attack_decision = {n : 0 for n in self.nodes()}

    def init_attributes(self):
        att = {n : {'value' : 1, 'utility' : 0, 'infected' : 0} for n in self.nodes()}
        self.add_attributes(att)

    def set_attack_decision(self, attack_decision):
        self.attack_decision = attack_decision

    def set_security_profile(self, security_investment):
        """
        Set security investments for agents
        :param security_investment: dictionary containing agent ids : security investment
        :return:
        """
        for n, value in security_investment.items():
            try:
                self.node[n]['security'] = value
                self.security_profile[n] = value
            except KeyError as error:
                pass
                print('KeyError : Agent with id #' + str(error) + ' does not exist.')

    def get_security_profile(self):
        """
        Return security investment for multiple agents
        :param profile: dictionary containing security profile (key : agent id, value : security investment)
        :return:
        """
        for n in self.nodes():
            self.security_profile[n] = self.node[n]['security']

        return self.security_profile

    def reset_security_profile(self):
        self.security_profile = dict.fromkeys(self.security_profile, 0)

    def add_attribute(self, id, attribute, value):
        """
        Add an attribute to node id
        :param id: agent id
        :param attribute: attribute key
        :param value: attribute value
        :return:
        """
        self.node[id][attribute] = value

    def add_attributes(self, attributes):
        """
        Add multiple attributes to nodes
        :param attributes: dictionary of agent ids with value a tuple (attribute, value)
        :return:
        """
        for n in attributes.keys():
            for att,value in attributes[n].items():
                self.add_attribute(n, att, value)

    def compute_network_effect(self, i):
        """
        Calculates probability of infection reaching agent i
        :param N: Network
        :param i: Target node
        :return:
        """
        qi = self.node[i]['security']
        r_prob = 0
        for node in self.nodes():
            for path in nx.all_simple_paths(self, source=node, target=i):
                source = path[0]
                r_prob += self.attack_decision[source] * prod([(1 - self.node[j]['security']) for j in path[:-1]])

        return (1 - qi) * r_prob

    def compute_utility(self):
        """
        Computes utility function for each agent
        :return:
        """
        for n in self.nodes():
            qn = self.node[n]['security']
            self.node[n]['utility'] = self.node[n]['value'] * (1 - self.compute_network_effect(n)) - default_cost(qn)


    def compute_social_welfare(self):
        """

        :return:
        """
        return sum([self.node[i]['utility'] for i in self.nodes()])

    def compute_nash_eq(self):
        """
        Computes Nash equilibrium
        :return:
        """
        for n in self.nodes():
            sec = copy(self.security_profile)
        return 0

    def compute_social_opt(self):
        """
        Computes social optimum of network
        :return:
        """
        return 0

    def compute_cost(self, id, function=default_cost):
        """
        Computes cost of security investment of node id
        :param function: cost function
        :param id: node id
        :return: Returns cost
        """
        return function(self.node[id]['security'])

    def expected_nbInfections(self):
        n = self.number_of_nodes()
        return 1.0 / n * sum(1 - np.asarray(self.security_profile.values())) # TODO : modify depending on attack strategy

    def get_transmission_network(self):
        """
        Returns corresponding transmission network
        :return:
        """
        networkT = self.copy()
        ids = [n for n in self.nodes() if self.node[n]['security'] == 1]
        networkT.remove_nodes_from(ids)
        return networkT