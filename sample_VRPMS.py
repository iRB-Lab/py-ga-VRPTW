# sameple_VRPMS

import random
from gavrptw.core import gaVRPMS

def main():
    random.seed(64)

    instName = "VRPMS_Data_Small"

    # Init costs associated with the heavy resource
    # Make the heavy resource 10x the cost of the light
    unitCost = 1.0
    initCost = 0.0
    waitCost = 0.0
    delayCost = 0.0

    # Init costs associated with the light resource
    lightUnitCost = 0.5
    lightInitCost = 0.0
    lightWaitCost = 0.0
    lightDelayCost = 0.0

    # Individual size should match the number of customers
    indSize = 11
    popSize = 30
    # At a random amount so far
    # TODO sensitivity analysis
    cxPb = 0.85
    mutPb = 0.02
    NGen = 500

    exportCSV = True
    customizeData = True

    gaVRPMS(
        instName = instName,
        unitCost = unitCost,
        initCost = initCost,
        waitCost = waitCost,
        delayCost = delayCost,

        lightUnitCost = lightUnitCost,
        lightInitCost = lightInitCost,
        lightWaitCost = lightWaitCost,
        lightDelayCost = lightDelayCost,

        indSize = indSize,
        popSize = popSize,
        cxPb = cxPb,
        mutPb = mutPb,
        NGen = NGen,
        exportCSV = exportCSV,
        customizeData = customizeData
    )

if __name__ == '__main__':
    main()
