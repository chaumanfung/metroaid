#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:11:01 2019


"""

import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

#AMdepart = pandas.read_csv(r"C:\Users\u0087328\Desktop\Brussels calibration\AMdeparture.csv", sep=";")
PWBB = pandas.read_csv(r"/Users/Desktop/Brussels calibration/DEMAND BY OD/DPW_BB.tsv",sep="\t")
POP_PW_BB = sum(PWBB['population'])
print(POP_PW_BB)
PWBF = pandas.read_csv(r"/Users/Desktop/Brussels calibration/DEMAND BY OD/DPW_BF.tsv",sep="\t")
POP_PW_BF = sum(PWBF['population'])
PWBW = pandas.read_csv(r"/Users/Desktop/Brussels calibration/DEMAND BY OD/DPW_BW.tsv",sep="\t")
POP_PW_BW = sum(PWBW['population'])
print(POP_PW_BW+POP_PW_BF)

PWFB = pandas.read_csv(r"/Users/Desktop/Brussels calibration/DEMAND BY OD/DPW_FB.tsv",sep="\t")
POP_PW_FB = sum(PWFB['population'])
print(POP_PW_FB)
PWFF = pandas.read_csv(r"/Users/Desktop/Brussels calibration/DEMAND BY OD/DPW_FF.tsv",sep="\t")
POP_PW_FF = sum(PWFF['population'])
print(POP_PW_FF)
