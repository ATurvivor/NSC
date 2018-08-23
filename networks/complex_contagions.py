import random
from ext import globals
from ext.threshold_functions import sigmoid


def complex_attack(g):
    """
    Attacks random vertex and its neighbors on g
    :param g: graph
    :return:
    """
    seed = random.choice(range(g.num_vertices()))
    g.vp['infectious'][seed] = True
    seed_neighborhood = g.vertex(seed).out_neighbors()
    for n in seed_neighborhood:
        g.vp['infectious'][n] = True

    iteration = 0
    while globals.gInfected:
        if globals.gDebug:
            print('t = {} : '.format(iteration), end='')
        complex_spread(g)
        iteration += 1

    print('\nEnd of propagation.\n\n')


def complex_spread(g, f=sigmoid):
    """
    Performs 1 time step iteration of propogating information over the newtork
    :param g: graph
    :param f: probabilistic function
    :return:
    """
    infectious = False
    g.set_vertex_filter(g.vp['infectious'])
    infectious_vertices = g.num_vertices()
    if globals.gDebug:
        print('Number of active infectors : {}'.format(g.num_vertices()))
    g.clear_filters()

    if infectious_vertices:
        infectious = True
        for v in g.vertices():
            if g.vp['infectious'][v] or g.vp['recovered'][v]:
                continue
            g.infect_vertex(v, complex=True)

    if g.gp['model'] == 'SIRS':
        g.update_recovered_time()
    g.update_infectious_time()

    if not infectious:
        globals.gInfected = False
        if globals.gDebug:
            print('Total nodes recovered nodes : {}/{}'.format(g.compute_final_size(), g.num_vertices()))
