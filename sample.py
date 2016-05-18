# -*- coding: utf-8 -*-
# sample.py

import random
from gaVRPTW import gaVRPTW


def main():
    random.seed(64)

    instName = 'R101'

    unitCost = 8.0
    initCost = 60.0
    waitCost = 0.5
    delayCost = 1.5

    indSize = 25
    popSize = 80
    cxPb = 0.85
    mutPb = 0.01
    NGen = 100

    # instName = 'C204'

    # unitCost = 8.0
    # initCost = 100.0
    # waitCost = 1.0
    # delayCost = 1.5

    # indSize = 100
    # popSize = 400
    # cxPb = 0.85
    # mutPb = 0.02
    # NGen = 300

    gaVRPTW(instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen)


if __name__ == '__main__':
    main()