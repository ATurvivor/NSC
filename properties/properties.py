from properties import globals


def read_properties(fname):
    """
    Reads properties file
    :param fname: properties file name
    :return: dictionary containing all properties and their corresponding values
    """
    with open(fname,'r') as f:
        data = f.readlines()
        properties = {}

        for line in data:
            line = line.split(' #')[0]
            if '=' in line and line[0] != '#':
                sp = line.split(' = ')
                properties[sp[0]] = sp[1]

    return properties


def set_properties(properties):
    """
    Sets properties
    :param properties: properties dictionary
    :return:
    """
    globals.gInfected = eval(properties['gInfected'])
    globals.gDebug = eval(properties['gDebug'])
    globals.START_TIME = eval(properties['START_TIME'])
    globals.STOP_TIME = eval(properties['STOP_TIME'])