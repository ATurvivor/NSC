import random
import numpy as np
import graph_tool.all as gt

from math import exp
from properties import globals

class Network(gt.Graph):
    def __init__(self, vertices=None, edges=None, defaults=True, model='SIR'):
        super().__init__(directed=False)
        # Setting up all properties of the graph
        self.gp['model'] = self.new_gp('string', val=model)
        self.vp['infectious_time'] = self.new_vp('int')
        self.vp['initial_infectious_time'] = self.new_vp('int')
        self.vp['recovered_time'] = self.new_vp('int')
        self.vp['initial_recovered_time'] = self.new_vp('int')
        self.vp['security'] = self.new_vp('double')
        self.vp['utility'] = self.new_vp('int')
        self.vp['recovered'] = self.new_vp('bool')
        self.vp['infectious'] = self.new_vp('bool')
        self.vp['susceptible'] = self.new_vp('bool')
        self.vp['attack_decision'] = self.new_vp('double')
        self.ep['rate'] = self.new_ep('double')
        if vertices is not None and edges is not None:
            self.add_vertex(vertices)
            self.add_edge_list(edges)
            if defaults:
                self._default_properties()

    @classmethod
    def from_graph(cls, G):
        """
        Generates a network via a graph object from graph_tool

        :param G: graph object
        :return:
        """
        return cls(vertices=G.num_vertices(), edges=list(G.edges()))

    def _default_properties(self):
        """
        Initializes the default properties of the network simulation

        :return:
        """
        low, high, n, m = globals.START_TIME, globals.STOP_TIME, self.num_vertices(), self.num_edges()
        infect, recover = np.random.randint(low, high, n), np.random.randint(low, high, n)

        self.vp['infectious_time'].a = infect
        self.vp['initial_infectious_time'].a = infect
        self.vp['recovered_time'].a = recover
        self.vp['initial_recovered_time'].a = recover
        self.vp['security'].a = np.random.rand(n)
        self.vp['utility'].a = 0
        self.vp['recovered'].a = False
        self.vp['infectious'].a = False
        self.vp['susceptible'].a = True
        self.vp['attack_decision'].a = 1/n
        self.ep['rate'].a = np.random.rand(m)

    def get_transmissibility(self, u, v):
        """
        Calculates the transmissibility between two nodes in the network

        :param u: vertex object or vertex index
        :param v: vertex object or vertex index
        """
        edge = self.edge(u, v)
        return 1 - exp(-self.edge_properties['rate'][edge] * self.vertex_properties['infectious_time'][u])

    def infect_vertex(self, v):
        """
        Attempts to infect vertex v

        :param v: vertex object or vertex index
        :return: True if vertex was infectious, False otherwise
        """
        if random.random() < self.vertex_properties['security'][v]:
            return False
        self.vp['infectious'][v] = True
        self.vp['susceptible'][v] = False
        return True

    def update_infectious_time(self):
        """
        Update infectious time and current state

        :return:
        """
        self.set_vertex_filter(self.vp['infectious'])

        self.vp['infectious_time'].ma -= 1
        mask = self.vp['infectious_time'].ma == 0
        self.vp['infectious_time'].ma[mask] = self.vp['initial_infectious_time'].ma[mask]
        self.vp['infectious'].ma[mask] = False
        self.vp['recovered'].ma[mask] = True

        self.clear_filters()

        return

    def update_recovered_time(self):
        """
        Update recovered time and current state

        :return:
        """
        self.set_vertex_filter(self.vp['recovered'])

        self.vp['recovered_time'].ma -= 1
        mask = self.vp['recovered_time'].ma == 0
        self.vp['recovered_time'].ma[mask] = self.vp['initial_recovered_time'].ma[mask]
        self.vp['recovered'] = False
        self.vp['susceptible'].ma[mask] = True

        self.clear_filters()

        return

    def compute_externality(self, i, j):
        """
        Calculates externality of vertex i on j
        :param i: vertex object or vertex index
        :param j: vertex object or vertex index
        :return:
        """
        # TODO : Figure out how to calculate paths using graph_tools

        return

    def compute_network_effect(self, i):
        """
        Calculates probability of infection reaching agent i, i.e network effect on i
        :param i: vertex object or vertex index
        :return:
        """
        # TODO : Calculate network effect without removing a node from the graph

        return

    def compute_social_welfare(self):
        """
        Computes social welfare
        :return:
        """
        return sum(self.vp['utility'].a)

    def compute_final_size(self):
        """
        Computes final size of an outbreak
        :return:
        """
        self.set_vertex_filter(self.vp['infectious'])
        num_infected = self.num_vertices()
        self.clear_filters()
        return num_infected

    def compute_relative_size(self):
        """
        Computes relative final size of graph
        :return:
        """
        return self.compute_final_size() / self.num_vertices()
