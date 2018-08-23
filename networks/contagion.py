import random
import graph_tool.all as gt

from properties import globals

def attack(g, init_infections):
    """
    Attacks random vertices on g
    :param g: network to simulate on
    :param init_infections: Number of initially infected vertices
    :return:
    """
    infect_idx = random.sample(range(g.num_vertices()), init_infections)
    infectious_vertices = [g.vertex(idx) for idx in infect_idx]
    for vertex in infectious_vertices:
        g.vp['infectious'][vertex] = 1

    iteration = 0
    while globals.gInfected:
        if globals.gDebug:
            print('t = {} : '.format(iteration), end='')
        spread(g)
        iteration += 1

    print('\nEnd of propagation.\n\n')

def spread(g):
    """
    Performs 1 time step iteration of propogating information over the newtork
    :param g: network to simulate on
    :return:
    """
    infectious = False
    g.set_vertex_filter(g.vp['infectious'])
    infectious_vertices = g.vertices()
    if globals.gDebug:
        print('Number of active infectors : {}'.format(g.num_vertices()))
    g.clear_filters()

    for v in infectious_vertices:
        infectious = True
        for u in g.vertex(v).all_neighbors():
            if g.vp['infectious'][u] or g.vp['recovered'][u]:
                continue
            if random.random() < g.get_transmissibility(v, u):
                g.infect_vertex(u)

    if g.gp['model'] == 'SIRS':
        g.update_recovered_time()
    g.update_infectious_time()

    if not infectious:
        globals.gInfected = False
        if globals.gDebug:
            print('Total nodes recovered nodes : {}/{}'.format(g.compute_final_size(), g.num_vertices()))



















