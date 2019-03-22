# -*- coding: utf-8 -*-

'''gavrptw/uitls.py'''

import os
import io
import fnmatch
from json import load, dump
from . import BASE_DIR


def make_dirs_for_file(path):
    '''gavrptw.uitls.make_dirs_for_file(path)'''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def guess_path_type(path):
    '''gavrptw.uitls.guess_path_type(path)'''
    if os.path.isfile(path):
        return 'File'
    if os.path.isdir(path):
        return 'Directory'
    if os.path.islink(path):
        return 'Symbolic Link'
    if os.path.ismount(path):
        return 'Mount Point'
    return 'Path'


def exist(path, overwrite=False, display_info=True):
    '''gavrptw.uitls.exist(path, overwrite=False, display_info=True)'''
    if os.path.exists(path):
        if overwrite:
            if display_info:
                print('{}: {} exists. Overwrite.'.format(guess_path_type(path), path))
            os.remove(path)
            return False
        if display_info:
            print('{}: {} exists.'.format(guess_path_type(path), path))
        return True
    if display_info:
        print('{}: {} does not exist.'.format(guess_path_type(path), path))
    return False


def load_instance(json_file):
    '''gavrptw.uitls.load_instance(json_file)'''
    if exist(path=json_file, overwrite=False, display_info=True):
        with io.open(json_file, 'rt', newline='') as file_object:
            return load(file_object)
    return None


def calculate_distance(customer1, customer2):
    '''gavrptw.uitls.calculate_distance(customer1, customer2)'''
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5


def text2json(customize=False):
    '''gavrptw.uitls.text2json(customize=False)'''
    if customize:
        text_data_dir = os.path.join(BASE_DIR, 'data', 'text_customize')
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        text_data_dir = os.path.join(BASE_DIR, 'data', 'text')
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json')
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename), \
        fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        json_data = {}
        with io.open(text_file, 'rt', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                if line_count in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instance_name'] = line.strip()
                elif line_count == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    json_data['max_vehicle_number'] = int(values[0])
                    json_data['vehicle_capacity'] = float(values[1])
                elif line_count == 10:
                    # Custom number = 0, deport
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data['deport'] = {
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
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data['customer_{}'.format(values[0])] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
        customers = ['deport'] + ['customer_{}'.format(x) for x in range(1, 101)]
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], json_data[customer2]) \
            for customer1 in customers] for customer2 in customers]
        json_file_name = '{}.json'.format(json_data['instance_name'])
        json_file = os.path.join(json_data_dir, json_file_name)
        print('Write to file: {}'.format(json_file))
        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))
