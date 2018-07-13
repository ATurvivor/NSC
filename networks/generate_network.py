import sys
from datetime import datetime

from itertools import chain
from networks.network import *

def random_graph_with_clustering(nodes, ps, pt):
    G = nx.empty_graph(nodes)
    stubs, corners = [ps() for _ in nodes], [pt() for _ in nodes]

    stubs[0] += sum(stubs) % 2
    corners[0] += sum(corners) % 3

    stubs = list(chain.from_iterable([n]*d for n, d in enumerate(stubs)))
    corners = list(chain.from_iterable([n]*d for n, d in enumerate(corners)))

    random.shuffle(stubs)
    random.shuffle(corners)

    n, t1, t2 = len(stubs)//2, len(corners)//3, 2*(len(corners)//3)
    stubs1, stubs2 = stubs[:n], stubs[n:]
    corners1, corners2, corners3 = corners[:t1], corners[t1:t2], corners[t2:]

    G.add_edges_from(zip(stubs1, stubs2))
    G.add_edges_from(zip(corners1, corners2))
    G.add_edges_from(zip(corners1, corners3))

    G.remove_edges_from(G.selfloop_edges())

    return G

def generate_attributes_file(n, **kwargs):
    """
    Generates an attribute file for networks to use

    :param n: number of nodes to generate attributes for
    :param \**kwargs:
        List of any parameters that are to be included in the attributes file,
        must match the number of nodes. If left blank a default attribute file
        will be generated
    :return fname: name of the output file
    """
    time = datetime.now()
    fname = 'attributes/'+ str(time.year) + str(time.month) + str(time.day) + '-' + \
            str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
            str(time.microsecond) + 'us_attributes.txt'
    if kwargs == {}:
        with open(fname,'w+') as fid:
            fid.write('id,initial_infectious_time,infectious_time,recovered_time,security_inv\n')
            for i in range(n):
                t = random.randint(globals.START_TIME, globals.STOP_TIME)
                tRecovered = random.randint()
                fid.write('{},{},{}\n'.format(i,t,t))

    return fname


def attributes_from_file(fid):  
    """
    :param fid: file object
    :return attributes: dictionary of {nodes : attributes}
    """
    header = fid.readline().rstrip().split(',')
    attributes = {}
    for line in fid:
        line = line.rstrip().split(',')
        attributes[int(line[0])] = dict(zip(header[1:], map(int, line[1:])))

    return attributes

def main(argv):
    n, m = 100, 5
    G = Network.from_graph(nx.barabasi_albert_graph(n, m))
    file_name = generate_attributes_file(n)

    with open(file_name) as fid:
        attributes = attributes_from_file(fid)
    nx.set_node_attributes(G, attributes)
    print(G.nodes(data=True))

if __name__=='__main__':
    main(sys.argv[1:])
