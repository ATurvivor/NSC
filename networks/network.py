import random

import matplotlib.pyplot as plt
import networkx as nx

from ext.cost_functions import *
from ext.extras import *
from properties import globals


class Network(nx.DiGraph):
    def __init__(self, nodes=None, edges=None):
        """

        :param nodes: list of indices of nodes
        :param edges: list of edges
        :return:
        """
        super().__init__(self)
        if nodes is not None and edges is not None:
            self.add_nodes_from(nodes)
            self.add_edges_from(edges)
            self.size = len(self.nodes())
        self.relative_size = 0

    @classmethod
    def from_graph(cls, G):
        """
        Generates a network via a graph object from Networkx

        :param G: graph object from networkx
        :return:
        """
        return cls(list(G.nodes()), list(G.to_directed().edges()))

    # @Override
    def add_node(self, node, **kwargs):
        """
        Overrides add_nodes method in class networkx

        :param nodes: iterable of nodes
        :return:
        """
        if kwargs == {}:
            t = random.randint(globals.START_TIME, globals.STOP_TIME)
            tRecovered = random.randint(globals.START_TIME, globals.STOP_TIME)
            s = random.random()
            super().add_node(node, node_color='#6EB8CF', utility=0, state=0, \
                    initial_infectious_time=t, infectious_time=t, \
                    initial_recovered_time=tRecovered, recovered_time=tRecovered,\
                    security=s, infected=0)
        else:
            super().add_node(node, **kwargs)

    # @Override
    def add_nodes_from(self, nodes, **kwargs):
        """
        Overrides add_nodes_from method in class networkx

        :param nodes: iterable of nodes
        :return:
        """
        if kwargs == {}:
            super().add_nodes_from(nodes, node_color='#6EB8CF', utility=0, state=0, infected=0)
            infectious_time = dict(zip(nodes, [random.randint(globals.START_TIME, globals.STOP_TIME) for _ in nodes]))
            recovered_time = dict(zip(nodes, [random.randint(globals.START_TIME, globals.STOP_TIME) for _ in nodes]))
            security = dict(zip(nodes, [random.random() for _ in nodes]))
            nx.set_node_attributes(self, infectious_time, 'initial_infectious_time')
            nx.set_node_attributes(self, infectious_time, 'infectious_time')
            nx.set_node_attributes(self, recovered_time, 'initial_recovered_time')
            nx.set_node_attributes(self, recovered_time, 'recovered_time')
            nx.set_node_attributes(self, security, 'security')
        else:
            super().add_nodes_from(nodes, **kwargs)

    # @Override
    def add_edge(self, edge, **kwargs):
        """
        Overrides add_edge method in class networkx 

        :param edges: edge single edge
        :return:
        """
        if kwargs == {}:
            r = random.random()
            super().add_edge(edge, edge_color='black', rate=r)
        else:
            super().add_edge(edge, **kwargs)

    # @Override
    def add_edges_from(self, edges, **kwargs):
        """
        Overrides add_edges_from method in class networkx

        :param edges: iterable of edges
        :return:
        """
        if kwargs == {}:
            super().add_edges_from(edges, edge_color='black')
            rate = dict(zip(edges, [random.random() for _ in edges]))
            nx.set_edge_attributes(self, rate, 'rate')
        else:
            super().add_edges_from(edges, **kwargs)

    def set_attack_decision(self, decision):
        """
        Sets attack decision
        :param decision:
        :return:
        """
        for n, value in decision.items():
            try:
                self.node[n]['decision'] = value
            except KeyError as error:
                pass
                print('\tKeyError : Agent with id #' + str(error) + ' does not exist.')

    def get_attack_decision(self):
        """
        Returns attack decision
        :return: dictionary
        """
        return {n : self.node[n]['decision'] for n in self.nodes()}

    def set_security_investments(self, security_inv):
        """
        Sets security investments
        :param security_inv: dictionary containing agent ids : security investment
        :return:
        """
        for n, value in security_inv.items():
            try:
                self.node[n]['security'] = value
            except KeyError as error:
                pass
                print('\tKeyError : Agent with id #' + str(error) + ' does not exist.')

    def get_security_profile(self):
        """
        Returns security profile
        :return: dictionary
        """
        return {n : self.node[n]['security'] for n in self.nodes()}

    def set_infectious_time(self, infectious):
        """
        Sets security investments
        :param security_inv: dictionary containing agent ids : security investment
        :return:
        """
        for n, value in infectious.items():
            try:
                self.node[n]['infectious_time'] = value
                self.node[n]['initial_infectious_time'] = value
            except KeyError as error:
                pass
                print('\tKeyError : Agent with id #' + str(error) + ' does not exist.')

    def get_infectious_time(self):
        """
        Returns security profile
        :return: dictionary
        """
        return {n : self.node[n]['infectious_time'] for n in self.nodes()}

    def set_rate_of_contact(self, rate):
        """
        Sets security investments
        :param security_inv: dictionary containing agent ids : security investment
        :return:
        """
        for (u,v), value in rate.items():
            try:
                self[u][v]['rate'] = value
            except KeyError:
                pass
                print('\tKeyError : Edge (' + str(u) + ',' + str(v) + ') does not exist.')

    def get_rate_of_contact(self):
        """
        Returns rates of contact
        :return: dictionary
        """
        return {(u,v) : self[u][v]['rate'] for (u,v) in self.edges()}

    def update_display(self):
        """
        Updates graph
        :return:
        """
        node_colors = ['#6EB8CF', '#BF404A']
        edge_colors = ['#000000', '#BF404A']
        nodes = list(self.nodes())
        while nodes:
            u = nodes.pop(0)
            u_inf = self.node[u]['infected']
            self.node[u]['node_color'] = node_colors[u_inf]
            for v in self[u]: # neighbors
                v_inf = self.node[v]['infected']
                if v in nodes:
                    self.node[v]['node_color'] = node_colors[v_inf]
                    nodes.remove(v)
                self[u][v]['edge_color'] = edge_colors[u_inf and v_inf]

    def display(self):
        """
        Displays graph
        :return:
        """
        self.update_display() # update

        node_colors = [self.node[n]['node_color'] for n in self.nodes()]
        edge_colors = [self[u][v]['edge_color'] for u,v in self.edges()]
        labels = {n : n for n in self.nodes()}
        pos = nx.layout.spring_layout(self)

        nx.draw_networkx_nodes(self, pos, node_color=node_colors, edgecolors='black')
        nx.draw_networkx_edges(self, pos, edge_color=edge_colors, arrowstyle='->', arrowsize=5, width=1)
        nx.draw_networkx_labels(self,pos,labels=labels, font_size=8)

        plt.plot()
        plt.show()

    def compute_externality(self, i, j):
        """
        Calculates externality of node i on j
        :param i:
        :return:
        """
        prob = 0
        attack_decision = self.get_attack_decision()
        for node in self.nodes():
            paths = [p for p in nx.all_simple_paths(self, source=node, target=j) if i in p]
            for path in paths:
                    prob += attack_decision[i] * prod([(1 - self.node[k]['security']) for k in path[:-1]])
        return (1 - self.node[i]['security']) * prob

    def compute_network_effect(self, i):
        """
        Calculates probability of infection reaching agent i, i.e. network effect on i
        :param N: Network
        :param i: node
        :return:
        """
        nodes = list(self.nodes())
        nodes.remove(i)
        if not nodes:
            return 1 - self.node[i]['security']
        else:
            j = nodes[0]
            new_network = self.reduce_graph(j)
            return new_network.compute_network_effect(i) + self.compute_externality(j, i)

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

    def compute_final_size(self):
        """
        Computes final size of an outbreak
        :return:
        """
        return len([n for n in self.nodes() if self.node[n]['infected'] == 1])

    def compute_relative_size(self):
        """
        Computes relative final size of graph
        :return:
        """
        return self.compute_final_size() / self.size

    def get_transmission_network(self):
        """
        Returns corresponding transmission network
        :return:
        """
        # TODO : verify method
        transmission_network = self.copy()
        nodes = [n for n in self.nodes() if self.node[n]['security'] == 1]
        transmission_network.remove_nodes_from(nodes)
        return transmission_network

    def reduce_graph(self, i):
        """

        :param i:
        :return:
        """
        # TODO : fix function
        new_network = self.copy()
        new_network.remove_node(i)
        return new_network
