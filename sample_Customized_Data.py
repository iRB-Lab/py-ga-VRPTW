# -*- coding: utf-8 -*-
# sample_Customized_Data.py

import random
from gavrptw.core import gaVRPTW


def main():
    random.seed(64)

    instName = 'Customized_Data'

    unitCost = 8.0
    initCost = 100.0
    waitCost = 1.0
    delayCost = 1.5

    indSize = 100
    popSize = 400
    cxPb = 0.85
    mutPb = 0.02
    NGen = 300

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