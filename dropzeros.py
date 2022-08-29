#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:01:17 2019



this script removes the zero population entries in the odmatrices to reduce the burden of database
"""

import pandas as pd
import numpy as np

odPW = pd.read_csv(r"/Users/Desktop/Brussels calibration/input/odPW.tsv", sep="\t")
odVL = pd.read_csv(r"/Users/Desktop/Brussels calibration/input/odVL.tsv", sep="\t")
odVZ = pd.read_csv(r"/Users/Desktop/Brussels calibration/input/odVZ.tsv", sep="\t")
odPW=odPW[odPW.population != 0]
odVL=odPW[odVL.population != 0]
odVZ=odPW[odVZ.population != 0]
odPW.to_csv(r"/Users/Desktop/odPW.tsv",sep="\t",index=False)
odVL.to_csv(r"/Users/Desktop/odVL.tsv",sep="\t",index=False)
odVZ.to_csv(r"/Users/Desktop/odVZ.tsv",sep="\t",index=False)

### the 12 groups