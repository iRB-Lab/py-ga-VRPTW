# -*- coding: utf-8 -*-

import os
import fnmatch
from json import dump
from . import BASE_DIR


def makeDirsForFile(pathname):
    try:
        os.makedirs(os.path.split(pathname)[0])
    except:
        pass


def exist(pathname, overwrite=False, displayInfo=True):
    def __pathType(pathname):
        if os.path.isfile(pathname):
            return 'File'
        if os.path.isdir(pathname):
            return 'Directory'
        if os.path.islink(pathname):
            return 'Symbolic Link'
        if os.path.ismount(pathname):
            return 'Mount Point'
        return 'Path'
    if os.path.exists(pathname):
        if overwrite:
            if displayInfo:
                print('%s: %s exists. Overwrite.' % (__pathType(pathname), pathname))
            os.remove(pathname)
            return False
        else:
            if displayInfo:
                print('%s: %s exists.' % (__pathType(pathname), pathname))
            return True
    else:
        if displayInfo:
            print('%s: %s does not exist.' % (__pathType(pathname), pathname))
        return False


def text2json(customize=False):
    def __distance(customer1, customer2):
        return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5
    if customize:
        textDataDir = os.path.join(BASE_DIR, 'data', 'text_customize')
        jsonDataDir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        textDataDir = os.path.join(BASE_DIR, 'data', 'text')
        jsonDataDir = os.path.join(BASE_DIR, 'data', 'json')
    for textFile in map(lambda textFilename: os.path.join(textDataDir, textFilename), fnmatch.filter(os.listdir(textDataDir), '*.txt')):
        jsonData = {}
        with open(textFile) as f:
            for lineNum, line in enumerate(f, start=1):
                if lineNum in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif lineNum == 1:
                    # <Instance name>
                    jsonData['instance_name'] = line.strip()
                elif lineNum == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    jsonData['max_vehicle_number'] = int(values[0])
                    jsonData['vehicle_capacity'] = float(values[1])
                elif lineNum == 10:
                    # Custom number = 0, deport
                    # <Custom number>, <X coordinate>, <Y coordinate>, <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    jsonData['deport'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
                else:
                    # <Custom number>, <X coordinate>, <Y coordinate>, <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    jsonData['customer_%s' % values[0]] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
        customers = ['deport'] + ['customer_%d' % x for x in range(1, 101)]
        jsonData['distance_matrix'] = [[__distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers]
        jsonFilename = '%s.json' % jsonData['instance_name']
        jsonPathname = os.path.join(jsonDataDir, jsonFilename)
        print('Write to file: %s' % jsonPathname)
        makeDirsForFile(pathname=jsonPathname)
        with open(jsonPathname, 'w') as f:
            dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': '))
