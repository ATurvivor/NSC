

def default_cost(security_investment):
    """
    Default cost function
    :param security_investment:
    :return:
    """
    return security_investment**2 * 1.0 / 5 * (2.9 - 1.33 * security_investment)

