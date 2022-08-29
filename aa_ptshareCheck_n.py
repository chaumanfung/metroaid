#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 23:42:34 2019


"""

import pandas
import requests

######################################
run = 1989
# extract simulated time from metropolis output
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
#first no is the simulation number and second is the run number
#loop over the run number for each iteration
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)
with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content) 
#####################################################
# take link_result.tsv columns to calculate toll
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results. tsv too for calculation of welfare
uresults = pandas.read_csv("user_results.tsv", sep="\t")
#####################################################
uresultsTrucks = uresults[uresults.travelerType=='trucks']
uresultsW = uresults[uresults.travelerType=='W']
uresultsN = uresults[uresults.travelerType=='N']
uresultsW_car = uresultsW[uresultsW.driveCar==1]
uresultsW_pt = uresultsW[uresultsW.driveCar==0]
uresultsN_car = uresultsN[uresultsN.driveCar==1]
uresultsN_pt = uresultsN[uresultsN.driveCar==0]
uresults_car = uresults[uresults.driveCar==1] 
uresults_car = uresults_car[uresults_car.travelerType!='trucks']
uresults_pt = uresults[uresults.driveCar==0]
# car 77871/(77871+23870)
# 1958: 85596/(85596+16225)= 0.84
# 1959: 82724/(82724+15331)= 0.84
PTcheck = pandas.read_csv(r"/Users/Desktop/ptdist_full.tsv", sep="\t")
PTcheck.loc['Total',:]= PTcheck.sum(axis=0)
# car, 0.8472
######NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN##################
# calculate PT share by distance
pttime = pd.read_csv(r"D:\METROPOLIS\Brussels calibration\pt2.csv", sep=",")
uresults_car.rename(columns={'origin':'ozone','destination':'dzone'}, 
                 inplace=True)
uresults_car1 = pd.merge(uresults_car,pttime[['distance','travel time','ozone','dzone']],on=['ozone', 'dzone'])
uresults_pt.rename(columns={'origin':'ozone','destination':'dzone'}, 
                 inplace=True)
uresults_pt1 = pd.merge(uresults_pt,pttime[['distance','travel time','ozone','dzone']],on=['ozone', 'dzone'])

bins = [0, 7.5, 10, 15, 25, 40, 300]
uresults_car1['binned_dist'] = pd.cut(uresults_car1['distance'], bins=bins)
uresults_pt1['binned_dist'] = pd.cut(uresults_pt1['distance'], bins=bins)
s_car = uresults_car1['binned_dist'].value_counts()
print(s_car)
s_pt = uresults_pt1['binned_dist'].value_counts()
print(s_pt)
