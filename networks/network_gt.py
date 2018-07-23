import random
import numpy as np
import graph_tool.all as gt

from properties import globals

class Network(gt.Graph):
    def __init__(self, nodes=None, edges=None, defaults=True. model='SIR'):
        super().__init__(directed=False)
        if nodes is not None and edges is not None:
            self.add_vertex(nodes)
            self.add_edge_list(edges)
            if defaults:
                self._default_properties()
        self.gp['model'] = self.new_gp('string', val=model)

    @classmethod
    def from_graph(cls, G):
        """
        Generates a network via a graph object from graph_tool

        :param G: graph object
        :return:
        """
        return cls(nodes=G.num_vertices(), edges=list(G.edges()))

    def _default_properties(self):
        """ Initializes the default properties of the network simulation

        :return:
        """
        low, high, n, m = globals.START_TIME, globals.STOP_TIME, self.num_vertices(), self.num_edges()
        infect, recover = np.random.randint(low, high, n), np.random.randint(low, high, n)

        self.vp['infectious_time'] = self.new_vp('int', vals=infect)
        self.vp['initial_infectious_time'] = self.new_vp('int', vals=infect)
        self.vp['recovered_time'] = self.new_vp('int', vals=recover)
        self.vp['initial_recovered_time'] = self.new_vp('int', vals=recover)
        self.vp['security'] = self.new_vp('double', vals=np.random.rand(n))
        self.vp['utility'] = self.new_vp('int', val=0)
        self.vp['recovered'] = self.new_vp('bool', val=False)
        self.vp['infected'] = self.new_vp('bool', val=False)
        self.ep['rate'] = self.new_ep('double', vals=np.random.rand(m))

    def get_transmissibility(self, u, v):
        """
        :param u: vertex object or vertex index
        :param v: vertex object or vertex index
        """
        edge = self.edge(u, v)
        return 1 - exp(-self.edge_properties['rate'][edge] * self.vertex_properties['infectious_time'][u])

    def infect_vertex(self, v):
        """ Attempts to infect vertex v

        :param v: vertex object or vertex index
        :return: True if vertex was infected, False otherwise
        """
        if random.random() > self.vertex_properties['security'][v]:
            self.vertex_properties['infected'] = 1
            self.vertex_properties['state'] = 1
            return True
        return False

    def update_infectious_time(self):
        """ Update infectious time and current state
        """
        self.set_vertex_filter('infected')
        self.vp['infectious_time'].ma -= 1
        mask = self.vp['infectious_time'].ma == 0
        self.vp['infectious_time'].ma[mask] = self.vp['initial_infectious_time'].ma[mask]
        self.clear_filters()
