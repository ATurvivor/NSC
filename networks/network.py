import networkx as nx


class Network(nx.Graph):
    def __init__(self, nodes):
        """

        :type nodes: integer
        :param nodes: number of nodes
        :return:
        """
        nx.Graph.__init__(self)
        self.add_nodes_from([n for n in range(5)])
        self.securityProfile = []
        self.set_security_profile()

    def add_attribute(self, id, attribute, value):
        """
        Add an attribute to node id
        :param id: node id
        :param attribute: attribute key
        :param value: attribute value
        :return:
        """
        self.nodes[id][attribute] = value
        if attribute == 'security':
            self.update_security_profile()

    def add_attributes(self, attributesList, valuesList, nodeList=None):
        """
        Add multiple attributes to nodes
        :param attributesList: list of keys
        :param valuesList: list of list of values for each node, for each attribute
        :param nodeList: list of nodes, if none, then all nodes in network
        :return:
        """
        if nodeList:
            nodes = nodeList
        else:
            nodes = self.nodes

        try:
            for a in range(len(attributesList)):
                att = attributesList[a]
                for n, v in zip(nodes, valuesList[a]):
                    self.add_attribute(n,att,v)
        except:
            print(ValueError)

    def set_security_profile(self):
        """

        :return:
        """
        for n in self.nodes:
            self.node[n]['security'] = 0

    def update_security_profile(self):
        """

        :return:
        """
        self.securityProfile = [self.node[n]['security'] for n in self.nodes]

    def computeNash(self):
        """
        Computes Nash equilibrium
        :return:
        """
        return 0

    def computeSocialOpt(self):
        """
        Computes social optimum of network
        :return:
        """
        return 0

    def computeSocialWelfare(self):
        """

        :return:
        """
        return sum([self.node[i]['utility'] for i in self.nodes])

    def computeCost(self, function, id):
        """
        Computes cost of security investment of node id
        :param function: cost function
        :param id: node id
        :return: Returns cost
        """
        return function(*self.node[id]['security'])

if __name__ == '__main__':
    G = Network(5)
    print(G.nodes)

    G.add_attributes(['security', 'utility'], [[0,0.2,0.4,0.2,5], [1,2,1,0,4]])
    #for n in G.nodes:
    #    G.add_attribute(n, 'utility', 2)

    print('Attribute test : ' + str(G.node[3]['security']))
    print('Social welfare : ' + str(G.computeSocialWelfare()))

    print('Security profile : ' + str(G.securityProfile))