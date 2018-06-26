import networkx as nx
import matplotlib.pyplot as plt

from ext.cost_functions import *
from ext.extras import *



class Network(nx.DiGraph):
    def __init__(self, nodes, edges):
        """

        :param nodes: list of indices of nodes
        :param edges: list of edges
        :return:
        """
        nx.DiGraph.__init__(self)
        self.add_nodes_from(nodes, node_color='#6EB8CF', utility=0, value=0, infected=0, state=0,\
                            initial_infectious_time=1, infectious_time=1)
        self.add_edges_from(edges, edge_color='black')
        self.size = len(self.nodes())
        self.relative_size = 0

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
            except KeyError as error:
                pass
                print('\tKeyError : Edge (' + str(u) + ',' + str(v) + ') does not exist.')

    def get_rate_of_contact(self):
        """
        Returns security profile
        :return: dictionary
        """
        return {(u,v) : self[u][v]['rate'] for (u,v) in self.edges()}

    def update_display(self):
        """

        :return:
        """
        colors = ['#6EB8CF', '#BF404A']
        nodes = list(self.nodes())
        while nodes:
            u = nodes.pop(0)
            u_inf = self.node[u]['infected']
            self.node[u]['node_color'] = colors[u_inf]
            for v in self[u]: # neighbors
                v_inf = self.node[v]['infected']
                if v in nodes:
                    self.node[v]['node_color'] = colors[v_inf]
                    nodes.remove(v)
                self[u][v]['edge_color'] = colors[u_inf and v_inf]

    def display(self):
        """

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
        return len([n for n in self.nodes() if self.node[n]['state'] == 2])

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