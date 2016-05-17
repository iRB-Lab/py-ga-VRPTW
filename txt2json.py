# -*- coding: utf-8 -*-

import os
import sys
import json
from basic.common import ROOT_PATH, makeDirsForFile, existFile


def distance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5


def main():
    rootpath = ROOT_PATH
    txtDataDir = os.path.join(rootpath, 'data', 'txt')
    jsonDataDir = os.path.join(rootpath,'data', 'json')

    for txtFile in map(lambda txtFilename: os.path.join(txtDataDir, txtFilename), os.listdir(txtDataDir)):
        jsonData = {}
        with open(txtFile) as f:
            for lineCount, line in enumerate(f, start=1):
                if lineCount in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif lineCount == 1:
                    # <Instance name>
                    jsonData['instance_name'] = line.strip()
                elif lineCount == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    jsonData['max_vehicle_number'] = int(values[0])
                    jsonData['vehicle_capacity'] = float(values[1])
                elif lineCount == 10:
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
                        'due_date': float(values[5]),
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
                        'due_date': float(values[5]),
                        'service_time': float(values[6]),
                    }

        customers = ['deport'] + ['customer_%s' % str(x) for x in range(1, 101)]
        jsonData['distance_matrix'] = [[distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers]


        jsonFilename = '%s.js' % jsonData['instance_name']
        jsonFile = os.path.join(jsonDataDir, jsonFilename)
        print 'Write to file: %s' % jsonFile
        makeDirsForFile(jsonFile)
        with open(jsonFile, 'w') as f:
            json.dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()