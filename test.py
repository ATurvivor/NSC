import graph_tool.all as gt
import numpy as np

from timeit import default_timer as timer
from networks.network_gt import *
from networks.generate_network_gt import *
from properties.properties import *

def main():
    properties = read_properties('properties/test.properties')
    set_properties(properties)

    n, m = 1500, 10
    ps = pt = lambda : random.randint(1,m)
    G = []
    output_size, bg_color = (800, 800), [1,1,1,1]

    print('Generating random graph with clustering...')
    start = timer()
    g = random_graph_with_clustering(n, ps, pt)
    end = timer()
    print('\tElasped time : {}'.format(end-start))
    print('\t{}'.format(g))
    deg = g.degree_property_map('in')
    deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    pos = gt.sfdp_layout(g)
    gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
            pos=pos, output_size=output_size, output='random_graph_with_clustering.png',\
            bg_color=bg_color)

    print('Generating chung lu model')
    start = timer()
    g = chung_lu_model(n, ps)
    end = timer()
    print('\tElasped time : {}'.format(end-start))
    print('\t{}'.format(g))
    deg = g.degree_property_map('in')
    deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    pos = gt.sfdp_layout(g)
    gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
            pos=pos, output_size=output_size, output='chung_lu_model.png',\
            bg_color=bg_color)

    print('Generating barbasi albert model')
    start = timer()
    g = barabasi_albert_model(n)
    end = timer()
    print('\tElasped time : {}'.format(end-start))
    print('\t{}'.format(g))
    deg = g.degree_property_map('in')
    deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
    pos = gt.sfdp_layout(g)
    gt.graph_draw(g, #vertex_size=deg, vertex_fill_color=deg, vorder=deg,\
            pos=pos, output_size=output_size, output='barabasi_albert_model.png',\
            bg_color=bg_color)

if __name__ == '__main__':
    main()
