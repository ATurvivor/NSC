import matplotlib.pyplot as plt
import os

from datetime import datetime
from networks.generate_network import *
from networks.contagion import attack

from ext.tools import read_properties, set_properties

import random

def run():
    """
    Run simulations
    :return:
    """
    runs = 10
    nodes = [10, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    opt = [1, 2, 3]
    models = ['SIR'] # ['SIR', 'SIRS', 'SIS']
    #threshold = ['absolute', 'relative', 'probabilistic']
    average_size = {'Barabasi_Albert' : {}, 'Chung_Lu' : {}, 'Random_Graphs' : {}}

    properties = read_properties('../properties/simple_contagion.properties')
    set_properties(properties)


    for model in models:
        for n in nodes:
            for m in opt:

                ps = pt = lambda : random.randint(1,m)
                print('Model : {}, number of nodes : {}, m : {}'.format(model, n, m))

                for graph in average_size.keys():
                    size = 0
                    if graph == 'Barabasi_Albert':
                        print('- Barabasi Albert Model')
                        for _ in range(runs):
                            g = barabasi_albert_model(n, m, model=model)
                            attack(g, init_infections=1)
                            size += g.compute_final_size()

                    elif graph == 'Chung_Lu':
                        print('- Chung Lu Model')
                        for _ in range(runs):
                            g = chung_lu_model(n, ps, model=model)
                            attack(g, init_infections=1)
                            size += g.compute_final_size()
                    else:
                        print('- Random Graph with High Clustering\n')
                        for _ in range(runs):
                            g = random_graph_with_clustering(n, ps, pt, model=model)
                            attack(g, init_infections=1)
                            size += g.compute_final_size()

                    if m not in average_size[graph]:
                        average_size[graph][m] = [size / runs]
                    else:
                        average_size[graph][m] += [size / runs]

    time = datetime.now()
    fname = 'results/simpleContagion' + str(time.year) + str(time.month) + str(time.day) + '-' + \
            str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
            str(time.microsecond) + 'us.txt'

    f = open(fname, 'w+')
    f.write(str(average_size))
    f.close()

def plot_results(directory):
    """

    :return:
    """
    plt.figure(num=None, figsize=(8, 15), dpi=80, facecolor='w', edgecolor='k')
    for fname in os.listdir(directory):
        if fname.endswith('.txt'):
            f = open(directory + fname, 'r')
            average_size = eval(f.read())
            nodes = [10, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
            index = 1
            for key in average_size.keys():
                plt.subplot(3, 1, index)
                graph_results = average_size[key]

                for m in graph_results.keys():
                    plt.plot(nodes, graph_results[m], label='m = {}'.format(m))

                plt.ylim(ymin=0)
                plt.legend(loc='upper left')
                plt.ylabel('Final epidemic size')
                plt.title('{} Model'.format(key))
                index += 1

            plt.xlabel('Number of nodes')
            plt.suptitle('Final epidemic size in terms of the number of nodes (SIR model)')
            imgname = directory + str.replace(fname, 'txt', 'png')
            plt.savefig(imgname)

if __name__ == '__main__':
    #run()
    plot_results('results/')

















