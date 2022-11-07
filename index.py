import pandas as pd
import numpy as np
import os
from constants.constants import *
from molecules.TestCases import TestCases


#Read dev and sqa reports from the csv files
source = pd.read_csv(devRepLoc,delimiter=',')
target = pd.read_csv(sqaRepLoc,delimiter=',',low_memory=False).drop_duplicates()

#Read data mapping sheet
dms = pd.read_excel(datampsheet,sheet_name=datamapSheetName,skiprows=skipRowsofDMS)

test = TestCases(source,target,dms)
test.commonTestCases()
test.findDelimetter()