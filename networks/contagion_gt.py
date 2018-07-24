import random
import graph_tool.all as gt

from networks.network_gt import Network
from properties import globals

def attack(g, init_infections):
    infect_idx = random.sample(range(g.num_vertices()), init_infections)
    infected_vertices = [g.vertex(idx) for idx in infect_idx]
    for vertex in infected_vertices:
        g.vp['infected'][vertex] = 1
        g.vp['active'][vertex] = 1
    iteration = 0
    while globals.gInfected:
        print('t = {} : '.format(iteration), end='')
        spread(g)
        iteration += 1

def spread(g):
    infected = False
    g.set_vertex_filter(g.vp['active'])
    infected_vertices = g.vertices()
    if globals.gDebug:
        print('Number of active infectors : {}'.format(g.num_vertices()))
    g.clear_filters()
    for v in infected_vertices:
        infected = True
        for u in g.vertex(v).all_neighbors():
            if g.vp['infected'][u]:
                continue
            if random.random() < g.get_transmissibility(v, u):
                g.infect_vertex(u)
    g.update_infectious_time()

    if not infected:
        globals.gInfected = False
        g.set_vertex_filter(g.vp['infected'])
        num_infected = g.num_vertices()
        g.clear_filters()
        print('Total nodes infected : {}/{}'.format(num_infected, g.num_vertices()))

