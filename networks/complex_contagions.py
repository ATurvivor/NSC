import random
import graph_tool.all as gt

from properties import globals

def complex_attack(g, threshold='absolute', value=2):
    """

    :param g:
    :param threshold:
    :param value:
    :return:
    """
    seed = random.choice(range(g.num_vertices()))
    g.vp['infectious'][seed] = 1
    seed_neighborhood = g.vertex(seed).out_neighbors()
    for n in seed_neighborhood:
        g.vp['infectious'][n] = 1

    iteration = 0
    while globals.gInfected:
        if globals.gDebug:
            print('t = {} : '.format(iteration), end='')
        complex_spread(g, threshold=threshold, value=value)
        iteration += 1

    print('\nEnd of propagation.\n\n')


def complex_spread(g, threshold='absolute', value=2):
    """

    :param g: network
    :param threshold: type of threshold
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
            neighbors = g.vertex(v).out_neighbors()
            inf_neighbors = [idx for idx in neighbors if g.vp['infectious'][idx]]
            if len(inf_neighbors) > value:
                g.vp['infectious'][v] = 1

    if g.gp['model'] == 'SIRS':
        g.update_recovered_time()
    g.update_infectious_time()

    if not infectious:
        globals.gInfected = False
        if globals.gDebug:
            print('Total nodes recovered nodes : {}/{}'.format(g.compute_final_size(), g.num_vertices()))
