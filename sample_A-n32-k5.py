# -*- coding: utf-8 -*-
# sample_A-n32-k5.py

import random
from gavrptw.core import gaVRPTW


def main():
    random.seed(64)

    instName = 'A-n32-k5'

    unitCost = 1.0
    initCost = 0.0
    waitCost = 0.0
    delayCost = 0.0

    indSize = 31
    popSize = 100
    cxPb = 1
    mutPb = 0.00
    NGen = 400

    exportCSV = True
    customizeData = True

    gaVRPTW(
        instName=instName,
        unitCost=unitCost,
        initCost=initCost,
        waitCost=waitCost,
        delayCost=delayCost,
        indSize=indSize,
        popSize=popSize,
        cxPb=cxPb,
        mutPb=mutPb,
        NGen=NGen,
        exportCSV=exportCSV,
        customizeData=customizeData
    )


if __name__ == '__main__':
    main()