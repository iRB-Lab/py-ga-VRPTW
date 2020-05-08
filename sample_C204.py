# -*- coding: utf-8 -*-

'''sample_C204.py'''

import random
from gavrptw.core import run_gavrptw


def main():
    '''main()'''
    random.seed(64)

    instance_name = 'C204'

    unit_cost = 8.0
    init_cost = 100.0
    wait_cost = 1.0
    delay_cost = 1.5

    ind_size = 100
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 300

    export_csv = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)


if __name__ == '__main__':
    main()
