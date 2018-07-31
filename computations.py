import numpy as np


def expected_nb_infections(g):
        """
        Computes the expected number of infections in graph G
        :param G: Graph
        :return:
        """
        security_profile = g.vp['security'].a
        attack_decision = g.vp['attack_decision'].a
        return sum(attack_decision * (1 - security_profile))
