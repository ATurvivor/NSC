import sys
import graph_tool.all as gt
import numpy as np

from timeit import default_timer as timer
from networks.construct_network import *
from networks.generate_network import *
from networks.contagion import attack
from properties.properties import *

def main(argv):
    properties = read_properties('properties/test.properties')
    set_properties(properties)

    n, m = 100, 2
    ps = pt = lambda : random.randint(1,m)
    output_size, bg_color = (1500, 1500), [1,1,1,1]

    g = barabasi_albert_model(n, m)
    attack(g, init_infections=1)
    if globals.gDispGraph:
        pos = gt.sfdp_layout(g)
        gt.graph_draw(g, pos=pos, vertex_fill_color=g.vp['recovered'], \
                bg_color=bg_color)

    if globals.gDraw:
        pos = gt.sfdp_layout(g)
        gt.graph_draw(g, pos=pos, vertex_fill_color=g.vp['recovered'], \
                output='output/graph.png', bg_color=bg_color, output_size=output_size)

    # print('Generating random graph with clustering...')
    # start = timer()
    # g = random_graph_with_clustering(n, ps, pt)
    # end = timer()
    # print('\tElasped time : {}\n\t{}'.format(end-start, g))
    # if globals.gDraw:
    #     deg = g.degree_property_map('in')
    #     deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    #     pos = gt.sfdp_layout(g)
    #     gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
    #             pos=pos, output_size=output_size, output='random_graph_with_clustering.png',\
    #             bg_color=bg_color)

    # print('Generating chung lu model')
    # start = timer()
    # g = chung_lu_model(n, ps)
    # end = timer()
    # print('\tElasped time : {}\n\t{}'.format(end-start, g))
    # if globals.gDraw:
    #     deg = g.degree_property_map('in')
    #     deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    #     pos = gt.sfdp_layout(g)
    #     gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
    #             pos=pos, output_size=output_size, output='chung_lu_model.png',\
    #             bg_color=bg_color)

    # print('Generating barbasi albert model')
    # start = timer()
    # g = barabasi_albert_model(n)
    # end = timer()
    # print('\tElasped time : {}\n\t{}'.format(end-start, g))
    # if globals.gDraw:
    #     deg = g.degree_property_map('in')
    #     deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    #     pos = gt.sfdp_layout(g)
    #     gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
    #             pos=pos, output_size=output_size, output='barabasi_albert_model.png',\
    #             bg_color=bg_color)


def network_effect_test():
    properties = read_properties('properties/test.properties')
    set_properties(properties)

    n, m = 10, 2
    #output_size, bg_color = (1500, 1500), [1,1,1,1]

    #g = star_graph(n)
    start = timer()
    g = barabasi_albert_model(n, m)
    val, val2 = g.compute_network_effect(g.vertex(1)), g.compute_network_effect(g.vertex(1))
    elapsed = timer() - start
    print('Elapsed Time : {}\nValues : {}, {}'.format(elapsed, val, val2))

    #pos = gt.sfdp_layout(g)
    #gt.graph_draw(g, pos=pos, vertex_fill_color=g.vp['recovered'], bg_color=bg_color)

if __name__ == '__main__':
    main(sys.argv)
    #network_effect_test()
















