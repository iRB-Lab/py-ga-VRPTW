# -*- coding: utf-8 -*-

import os
import fnmatch
import matplotlib.pyplot as plt
from json import dump
import pandas as pd
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
                print u'%s: %s exists. Overwrite.' % (__pathType(pathname), pathname)
            os.remove(pathname)
            return False
        else:
            if displayInfo:
                print u'%s: %s exists.' % (__pathType(pathname), pathname)
            return True
    else:
        if displayInfo:
            print u'%s: %s does not exist.' % (__pathType(pathname), pathname)
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
        # Count the number of lines in the file to customize the number of customers
        size = sum(1 for line in open(textFile))
        with open(textFile) as f:
            for lineNum, line in enumerate(f, start=1):
                if lineNum in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif lineNum == 1:
                    # <Instance name>
                    jsonData['instance_name'] = line.strip()
                elif lineNum == 5:
                    # <Maximum heavy vehicle number>, <Heavy vehicle capacity>,
                    # <Maximum light vehicle number>, <Light vehicle capacity>, <Light vehicle range>
                    values = line.strip().split()
                    jsonData['max_vehicle_number'] = int(values[0])
                    jsonData['vehicle_capacity'] = float(values[1])
                    try:
                        gotdata = values[2]
                    except IndexError:
                        gotdata = False
                    if gotdata:
                        jsonData['max_light_vehicle_number'] = int(values[2])
                        jsonData['light_vehicle_capacity'] = float(values[3])
                        jsonData['light_vehicle_range'] = float(values[4])
                    else:
                        pass
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
        # There are a constant 9 lines of header text before customers
        numOfCustomers = size - 9
        customers = ['deport'] + ['customer_%d' % x for x in range(1, numOfCustomers)]
        jsonData['distance_matrix'] = [[__distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers]
        jsonFilename = '%s.json' % jsonData['instance_name']
        jsonPathname = os.path.join(jsonDataDir, jsonFilename)
        print 'Write to file: %s' % jsonPathname
        makeDirsForFile(pathname=jsonPathname)
        with open(jsonPathname, 'w') as f:
            dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': '))


def plotResults():
    plt.style.use('ggplot')
    resultsDataDir = os.path.join(BASE_DIR, 'results')
    for csvFile in map(lambda csvFilename: os.path.join(resultsDataDir, csvFilename), fnmatch.filter(os.listdir(resultsDataDir), '*csv')):
        df = pd.read_csv(csvFile)
        # Delete the last 2 columns (std_fitness, avg_cost)
        if len(df.columns) == 6:
            df.drop(df.columns[[5]], axis=1, inplace=True)
        else:
            df.drop(df.columns[[5, 6]], axis=1, inplace=True)
        # Delete the first 2 columns (generation, evaluated_individuals) 
        df.drop(df.columns[[0,1]], axis=1, inplace=True)
        
        plt.figure()
        ax = df.plot(figsize=(20,10))
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness')

        # Save to folder
        filename = os.path.splitext(csvFile)[0]
        plt.savefig(filename + '.png')