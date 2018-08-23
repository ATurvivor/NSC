from functools import reduce
from operator import mul
from ext import globals


def prod(iterable):
    return reduce(mul, iterable, 1)


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
    globals.START_TIME = eval(properties['START_TIME'])
    globals.STOP_TIME = eval(properties['STOP_TIME'])

    globals.gInfected = eval(properties['gInfected'])
    globals.gDebug = eval(properties['gDebug'])
    globals.gDispGraph = eval(properties['gDispGraph'])
    globals.gDraw = eval(properties['gDraw'])
    globals.gLog = eval(properties['gLog'])

    globals.gComplex = eval(properties['gComplex'])

    globals.gAnimate = eval(properties['gAnimate'])
    globals.gSaveImages = eval(properties['gSaveImages'])
    globals.gCount = eval(properties['gCount'])
    globals.gMaxCount = eval(properties['gMaxCount'])