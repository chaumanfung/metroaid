# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:03:06 2019

This script compares the departure time destribution from odmatrix and
the departure time destribution obtained from metropolis
"""

import pandas
import matplotlib.pyplot as plt
#import statsmodels.api as sm
#import numpy as np
import requests

#AMdepart = pandas.read_csv(r"C:\Users\u0087328\Desktop\Brussels calibration\AMdeparture.csv", sep=";")
#AMdepart = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/AMdeparture.csv", sep=";")
AMdepart = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\AMdeparture.csv", sep=";")

AMdepart['PW']=AMdepart['PW']/100
AMdepart['VL']=AMdepart['VL']/20
AMdepart['VZ']=AMdepart['VZ']/20
AMdepart['trucks']=AMdepart['VL']+AMdepart['VZ']
AMdepart['all']=AMdepart['PW']+AMdepart['VL']+AMdepart['VZ']

#uresults = pandas.read_csv(r"/Users/username/Desktop/stepsize1/14/user_results.tsv", sep="\t")
######################################
run = 2207
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

uresults['td1']=300+uresults['td']/60
uresultsTrucks['tdTrucks']=300+uresultsTrucks['td']/60
uresultsW['tdW']=300+uresultsW['td']/60
uresultsN['tdN']=300+uresultsN['td']/60
uresults_car['tdCar']=300+uresults_car['td']/60
uresults_pt['tdPt']=300+uresults_pt['td']/60

plt.hist(uresultsTrucks['tdTrucks'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
plt.plot(AMdepart['Time'],AMdepart['trucks'])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(('field','metropolis'),loc='upper left')
plt.title('Trucks departure time, field vs simulated')
plt.grid(True)
fig = plt.gcf()
plt.show()
#fig.savefig('/Volumes/Samsung_T5/METROPOLIS/dpTrucks_'+str(run)+'.png')
fig.savefig(r'D:\METROPOLIS\nov2020\dptruck.png')

#plt.hist(uresultsVL['tdVL'],bins=[300,315,330,345,360,375,390,405,420,435,450,465,480,495,510,525,540,555,570,585,600,615,630,645,660])
plt.hist(uresults_car['tdCar'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
plt.plot(AMdepart['Time'],AMdepart['PW'])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(('field','metropolis'),loc='upper left')
plt.title('Car departure time, field vs simulated')
fig = plt.gcf()
plt.show()
#fig.savefig('/Volumes/Samsung_T5/METROPOLIS/dpCar_'+str(run)+'.png')
fig.savefig(r'D:\METROPOLIS\nov2020\dpcar.png')

#plt.hist(uresultsVZ['tdVZ'],bins=[300,315,330,345,360,375,390,405,420,435,450,465,480,495,510,525,540,555,570,585,600,615,630,645,660])
'''plt.hist(uresults_pt['tdPT'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
plt.plot(AMdepart['Time'],AMdepart['VZ'])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(('field','metropolis'),loc='upper left')
plt.title('VZ departure time, field vs simulated')
plt.grid(True)
fig = plt.gcf()
plt.show()
fig.savefig('/Users/username/Desktop/dpVZ_'+str(run)+'.png')'''

plt.hist(uresults['td1'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
plt.plot(AMdepart['Time'],AMdepart['all'])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(('field','metropolis'),loc='upper left')
plt.title('all departure time, field vs simulated')
plt.grid(True)
fig = plt.gcf()
plt.show()
fig.savefig('/Volumes/Samsung_T5/METROPOLIS/dpall_'+str(run)+'.png')