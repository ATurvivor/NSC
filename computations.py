import numpy as np


def expected_nb_infections(G):
        """
        Computes the expected number of infections in graph G
        :param G: Graph
        :return:
        """
        security_profile = np.asarray(list(G.get_security_profile().values()))
        attack_decision = np.asarray(list(G.get_attack_decision().values()))
        return sum(attack_decision * (1 - security_profile))
