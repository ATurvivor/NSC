import matplotlib.pyplot as plt


from datetime import datetime
from timeit import default_timer as timer
from networks.generate_network import *
from networks.contagion import attack

from ext.tools import read_properties, set_properties

import random

def run():
    """
    Run simulations
    :return:
    """
    runs = 1

    nb_nodes = [10, 100, 500, 1000, 5000, 10000]
    opt = [1, 2, 3]
    models = ['SIR']
    #models = ['SIR', 'SIRS', 'SIS']
    #threshold = ['absolute', 'relative', 'probabilistic']
    av_size = {}

    properties = read_properties('../properties/simple_contagion.properties')
    set_properties(properties)

    print('Barabasi-Albert Model\n##########\n')

    for model in models:
        for n in nb_nodes:
            for m in opt:
                if m not in av_size:
                    av_size[m] = []

                size = 0
                ps = pt = lambda : random.randint(1,m)

                print('Model : {}, number of nodes : {}, m : {}'.format(model, n, m))
                for _ in range(runs):
                    #start = timer()
                    g = barabasi_albert_model(n, m, model=model)
                    attack(g, init_infections=1)
                    #end = timer()
                    #print('Elapsed time : {}\n'.format(end-start))

                    size += g.compute_final_size()
                av_size[m] += [size / runs]

                # print('Chung-Lu Model\n##########\n')
                # start = timer()
                # g = chung_lu_model(n, ps, model=model)
                # end = timer()
                # print('Elapsed time : {}\n'.format(end-start))
                #
                # print('Random Graphs with High Clustering\n##########\n')
                # start = timer()
                # g = random_graph_with_clustering(n, ps, pt, model=model)
                # end = timer()
                # print('Elapsed time : {}\n'.format(end-start))

    plot_results(nb_nodes, av_size)

def plot_results(nodes, size):
    """

    :return:
    """
    time = datetime.now()
    fname = 'results/simpleContagion' + str(time.year) + str(time.month) + str(time.day) + '-' + \
            str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
            str(time.microsecond) + 'us.png'

    for m in size.keys():
        plt.plot(nodes, size[m], label='m = {}'.format(m))
    plt.ylim(ymin=0)
    plt.legend(loc='upper left')
    plt.xlabel('Number of nodes')
    plt.ylabel('Final epidemic size')
    plt.title('Final epidemic size in terms of the number of nodes (SIR model)')
    plt.savefig(fname)

if __name__ == '__main__':
    run()


















