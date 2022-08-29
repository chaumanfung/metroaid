#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:59:51 2019

"""

#import requests 
import pandas
import numpy as np
import requests
import xlsxwriter

links_mainzone = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\links_mainzone_n.csv", sep=",")
links = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\links.tsv", sep="\t")

#########################################################################
#########################################################################
run = 9720 #2209#2210 #2207, 2208, 2209,2212, 2334, 2210
mileage = 	2.67762
ext = 0.04 #external cost by km
#step=
#alpha=  
#interval = 5
#dimin = 12* 6 #for 5min interval, 6 hours
#########################################################################
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)
with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content) 
#####################################################
# take link_result.tsv to calculate toll
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results.tsv for calculation of welfare
userresults = pandas.read_csv("user_results.tsv", sep="\t")
###################################################
# calculate welfare
welfare=[] #welfare with refund of toll revenue
welfareno=[] #welfare without refund of toll revenue
cs=[] #only add consumer surplus of all users

welfare.append(sum(userresults['surplus'])+sum(userresults['fee'])-float(mileage)*100000*float(ext)) 
print(welfare)
welfareno.append(sum(userresults['surplus'])-float(mileage)*100000*float(ext))
print(welfareno)
cs.append(sum(userresults['surplus']))
print(cs)

#####################################################
workbook = xlsxwriter.Workbook('cs.xlsx')
worksheet = workbook.add_worksheet()
array = [welfare,
         welfareno,
         cs]
row = 0
for col, data in enumerate(array):
    worksheet.write_column(row, col, data)
workbook.close()
#####################################################
#####################################################
#### FLAT Toll #### for roads in ALL regions by distance at 7-9, all users ####
pkm=0.15
#create toll tsv file for runs
links1 = links[links.function == 2] #subset with non-freeflow
links1.insert(9,'dist_toll',links['length']*pkm)
x = np.zeros(len(links1))
dftolltime=np.column_stack((x,links1["dist_toll"],x))
links1['toll_dist2'] = dftolltime.tolist()
links1['toll_dist2'] = links1['toll_dist2'].astype(str).str[1:-1]
links1["times"]= "420,540"
links1.rename({'id':'link'}, axis='columns',inplace=True)
links1.rename({'toll_dist2':'values'}, axis='columns',inplace=True)
links1[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\toll_dist05.tsv",sep="\t",index=False)

#####################################################
nodes_on = pandas.read_csv(r"D:\METROPOLIS\input_NETWORK\nodes_n.csv", sep=",")
nodes_on1 = pandas.merge(links_mainzone, nodes_on, how='outer',
                            left_on=['FROMNODENO'],
                            right_on=['node_old'])
nodes_on2 = pandas.merge(nodes_on1, nodes_on, how='outer',
                            left_on=['TONODENO'],
                            right_on=['node_old'])

links_on = pandas.merge(nodes_on2, links, how='inner',
                            left_on=['node_new_x','node_new_y'],
                            right_on=['origin','destination'])
#####################################################
#### Regions #### categorize inks by regions
links_bru = links_on[links_on.NISCode == 1000]
links_fla = links_on[links_on.NISCode == 2000]
links_wal = links_on[links_on.NISCode == 3000]
links_nil= links_on[(links_on['NISCode']!=1000)]
links_nil= links_nil[(links_nil['NISCode']!=2000)]
links_nil= links_nil[(links_nil['NISCode']!=3000)]

#### produce script for regional tolls ####
## flat tolls 0700-0900, each region charges and gets own toll revenues
## brussels charges links_bru; flanders charges links_fla; links_nil stay free

### Brussels ###
pkm=0.15
links_bruT = links_bru[links_bru.function == 2] #subset with non-freeflow
links_bruT.insert(179,'dist_toll',links_bruT['length']*pkm)
links_bruT['dist_toll'] = links_bruT['length']*pkm
x = np.zeros(len(links_bruT))
dftolltime=np.column_stack((x,links_bruT["dist_toll"],x))
links_bruT['toll_dist2'] = dftolltime.tolist()
links_bruT['toll_dist2'] = links_bruT['toll_dist2'].astype(str).str[1:-1]
links_bruT["times"]= "420,540"
links_bruT.rename({'id':'link'}, axis='columns',inplace=True)
links_bruT.rename({'toll_dist2':'values'}, axis='columns',inplace=True)
links_bruT[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\tollDistB15.tsv",sep="\t",index=False)

### Flanders ###
#pkm=0.05
links_flaT = links_fla[links_fla.function == 2] #subset with non-freeflow
links_flaT.insert(179,'dist_toll',links_flaT['length']*pkm)
#links_flaT['dist_toll'] = links_flaT['length']*pkm
x = np.zeros(len(links_flaT))
dftolltime=np.column_stack((x,links_flaT["dist_toll"],x))
links_flaT['toll_dist2'] = dftolltime.tolist()
links_flaT['toll_dist2'] = links_flaT['toll_dist2'].astype(str).str[1:-1]
links_flaT["times"]= "420,540"
links_flaT.rename({'id':'link'}, axis='columns',inplace=True)
links_flaT.rename({'toll_dist2':'values'}, axis='columns',inplace=True)
links_flaT[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\tollDistF15.tsv",sep="\t",index=False)

## wallonia
links_walT = links_wal[links_wal.function == 2] #subset with non-freeflow
links_walT.insert(179,'dist_toll',links_walT['length']*pkm)
links_walT['dist_toll'] = links_walT['length']*pkm
x = np.zeros(len(links_walT))
dftolltime=np.column_stack((x,links_walT["dist_toll"],x))
links_walT['toll_dist2'] = dftolltime.tolist()
links_walT['toll_dist2'] = links_walT['toll_dist2'].astype(str).str[1:-1]
links_walT["times"]= "420,540"
links_walT.rename({'id':'link'}, axis='columns',inplace=True)
links_walT.rename({'toll_dist2':'values'}, axis='columns',inplace=True)
links_walT[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\tollDistW15.tsv",sep="\t",index=False)

### crossregions/nil ###
#pkm=0.02
links_nilT = links_nil[links_nil.function == 2] #subset with non-freeflow
links_nilT.insert(179,'dist_toll',links_nilT['length']*pkm)
#links_flaT['dist_toll'] = links_flaT['length']*pkm
x = np.zeros(len(links_nilT))
dftolltime=np.column_stack((x,links_nilT["dist_toll"],x))
links_nilT['toll_dist2'] = dftolltime.tolist()
links_nilT['toll_dist2'] = links_nilT['toll_dist2'].astype(str).str[1:-1]
links_nilT["times"]= "420,540"
links_nilT.rename({'id':'link'}, axis='columns',inplace=True)
links_nilT.rename({'toll_dist2':'values'}, axis='columns',inplace=True)
links_nilT[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\tollDistN15.tsv",sep="\t",index=False)

#########################################################################
#########################################################################
#### categorize users by regions, using origin mainzones of users
mainzone = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\mainzone.csv", sep=";")

welfare=[]
welfareno=[]
cs=[]
revenue=[]
extCost=[]
revfromB=[]
revfromF=[]
revfromW=[]
csB=[]
csF=[]
csW=[]
revtoB=[]
revtoF=[]
revtoW=[]
revtoN=[]
trucks=[]
work=[]
nwork=[]

#run = 9235#2335#2210 #2207, 2208, 2209,2212, 2334, 2210
#mileage = 2.66727
#pkm =0.15
#ext = 0.04 #external cost by km
#step=
#alpha=  
#interval = 5
#dimin = 12* 6 #for 5min interval, 6 hours
#########################################################################
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)
with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content) 
#####################################################
# take link_result.tsv to calculate toll
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results.tsv for calculation of welfare
userresults = pandas.read_csv("user_results.tsv", sep="\t")
###################################################

# calculate welfare (group specific)
userresults1 = pandas.merge(userresults,mainzone,left_on="origin",right_on="ZONE")
userresults2 = pandas.merge(userresults1,mainzone,left_on="destination",right_on="ZONE")
userresultsB = userresults2[userresults2.MAINZONE_x==1]
userresultsW = userresults2[userresults2.MAINZONE_x==2]
userresultsF = userresults2[userresults2.MAINZONE_x==3]

########### TOTAL WELFARE #######################

trucks.append(userresults.travelerType.value_counts()['trucks'])
print(trucks)
work.append(userresults.travelerType.value_counts()['W'])
print(work)
nwork.append(userresults.travelerType.value_counts()['N'])
print(nwork)
welfare.append(sum(userresults['surplus'])+sum(userresults['fee'])-float(mileage)*100000*float(ext)) 
print(welfare)
welfareno.append(sum(userresults['surplus'])-float(mileage)*100000*float(ext))
print(welfareno)
cs.append(sum(userresults['surplus']))
print(cs)
revenue.append(sum(userresults['fee']))
print(revenue)
extCost.append(float(mileage)*100000*float(ext))
print(extCost)
######### WELFARE Brussels #############################
revfromB.append(sum(userresultsB['fee'])) 
print(revfromB)
csB.append(sum(userresultsB['surplus']))
print(csB)
######### WELFARE Flanders #############################
revfromF.append(sum(userresultsF['fee'])) 
print(revfromF)
csF.append(sum(userresultsF['surplus']))
print(csF)
######### WELFARE W #############################
revfromW.append(sum(userresultsW['fee'])) 
print(revfromW)
csW.append(sum(userresultsW['surplus']))
print(csW)
#####################################################
pkmb = 0.15
links_bruR = pandas.merge(linkresults,links_bruT,how='inner',left_on="link",right_on="link")
links_bruR['tolled'] = links_bruR.iloc[:,97:120].sum(axis=1)+links_bruR.iloc[:,73:96].sum(axis=1)-links_bruR.iloc[:,217:240].sum(axis=1)
links_bruR['tolledAmt'] = links_bruR['length']*pkmb*links_bruR['tolled']
revtoB.append(sum(links_bruR['tolledAmt']))
print(revtoB)
revtoB[0]+csB[0]
#####################################################
pkmf = 0.15
links_flaR = pandas.merge(linkresults,links_flaT,how='inner',left_on="link",right_on="link")
links_flaR['tolled'] = links_flaR.iloc[:,97:120].sum(axis=1)+links_flaR.iloc[:,73:96].sum(axis=1)-links_flaR.iloc[:,217:240].sum(axis=1)
links_flaR['tolledAmt'] = links_flaR['length']*pkmf*links_flaR['tolled']
revtoF.append(sum(links_flaR['tolledAmt']))
print(revtoF)
revtoF[0]+csF[0]
#####################################################
#####################################################
pkm = 0.15
links_walR = pandas.merge(linkresults,links_walT,how='inner',left_on="link",right_on="link")
links_walR['tolled'] = links_walR.iloc[:,97:120].sum(axis=1)+links_walR.iloc[:,73:96].sum(axis=1)-links_walR.iloc[:,217:240].sum(axis=1)
links_walR['tolledAmt'] = links_walR['length']*pkm*links_walR['tolled']
revtoW.append(sum(links_walR['tolledAmt']))
print(revtoW)
revtoW[0]+csW[0]
#####################################################
pkm = 0.02
links_nilR = pandas.merge(linkresults,links_nilT,how='inner',left_on="link",right_on="link")
links_nilR['tolled'] = links_nilR.iloc[:,97:120].sum(axis=1)+links_nilR.iloc[:,73:96].sum(axis=1)-links_nilR.iloc[:,217:240].sum(axis=1)
links_nilR['tolledAmt'] = links_nilR['length']*pkm*links_nilR['tolled']
revtoN.append(sum(links_nilR['tolledAmt']))
print(revtoN)
#####################################################
workbook = xlsxwriter.Workbook(r"D:\METROPOLIS\nov2020\cs_flat30.xlsx")
worksheet = workbook.add_worksheet()
array = [welfare,
         welfareno,
         cs,
         revenue,
         extCost,
         revfromB,
         revfromF,
         revfromW,
         csB,
         csF,
         csW,
         revtoB,
         revtoF,
         revtoW,
         revtoN,
         trucks,
         work,
         nwork]
row = 0
for col, data in enumerate(array):
    worksheet.write_column(row, col, data)
workbook.close()
#####################################################

############################################################################
#############CORDON TOLL ENTERING BRUSSELS REGION###########################
#########################################################################
run =9724#2209#2210 #2207, 2208, 2209,2212, 2334, 2210
mileage = 	2.70405

ext = 0.04 #external cost by km
#step=
#alpha=  
#interval = 5
#dimin = 12* 6 #for 5min interval, 6 hours
#########################################################################
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)
with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content) 
#####################################################
# take link_result.tsv to calculate toll
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results.tsv for calculation of welfare
userresults = pandas.read_csv("user_results.tsv", sep="\t")
###################################################
mainzone = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\mainzone.csv", sep=";")
# calculate welfare (group specific)
userresults1 = pandas.merge(userresults,mainzone,left_on="origin",right_on="ZONE")
userresults2 = pandas.merge(userresults1,mainzone,left_on="destination",right_on="ZONE")
userresultsB = userresults2[userresults2.MAINZONE_x==1]
userresultsW = userresults2[userresults2.MAINZONE_x==2]
userresultsF = userresults2[userresults2.MAINZONE_x==3]
#userresultsW2B = userresults2[userresults2.MAINZONE_x==2 & userresults2.MAINZONE_y==1]
#userresultsF2B = userresults2[userresults2.MAINZONE_x==3 & userresults2.MAINZONE_y==1]
#####################################################
#####################################################
nodes_on = pandas.read_csv(r"D:\METROPOLIS\input_NETWORK\nodes_n.csv", sep=",")
nodes_on1 = pandas.merge(links_mainzone, nodes_on, how='outer',
                            left_on=['FROMNODENO'],
                            right_on=['node_old'])
nodes_on2 = pandas.merge(nodes_on1, nodes_on, how='outer',
                            left_on=['TONODENO'],
                            right_on=['node_old'])

links_on = pandas.merge(nodes_on2, links, how='inner',
                            left_on=['node_new_x','node_new_y'],
                            right_on=['origin','destination'])
#####################################################

## identify the links which has origin in 3 and destination in 1
node_region = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\node_region.csv", sep=",")
node_region1 = pandas.merge(links_on, node_region, how='outer',
                            left_on=['node_old_x'],
                            right_on=['NO'])
node_region2 = pandas.merge(node_region1, node_region, how='outer',
                            left_on=['node_old_y'],
                            right_on=['NO'])
dlink = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\dlink.tsv", sep="\t")

matchnode = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\input\wid_n_intersection.tsv", sep="\t")
nodes=pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\nodes.csv", sep=";",encoding='ISO-8859-1')
rnodes=pandas.merge(matchnode,nodes[["NODE:NO","PROVINCIE"]],left_on="NodeNo",right_on="NODE:NO")
clink=pandas.merge(dlink,rnodes[["2000","PROVINCIE"]],left_on="origin",right_on="2000")
clink1=pandas.merge(clink,rnodes[["2000","PROVINCIE"]],left_on="destination",right_on="2000")

clink1['PROVINCIE_x'].fillna("unknown",inplace=True)
dftoll2=clink1[clink1.PROVINCIE_x!="BRUSSEL"]
dftoll2=dftoll2[dftoll2.PROVINCIE_x!="unknown"]
dftoll2=dftoll2[dftoll2.PROVINCIE_y=="BRUSSEL"]
#dftoll2["traveler_type"]=1 #cars only?
dftoll2["values"]="0,4,0" #how much cordon?
dftoll2["times"]= "420,540"
dftoll2.rename({'id':'link'}, axis='columns',inplace=True)
#dftoll2[['link','values','times']].to_csv(r"D:\METROPOLIS\Brussels calibration\cordon400.tsv",sep="\t",index=False)
#in total, 215 links are tolled.
#####################################################
#####################################################
# calculate welfare
welfare=[] #welfare with refund of toll revenue
welfareno=[] #welfare without refund of toll revenue
cs=[] #only add consumer surplus of all users
trucks=[]
work=[]
nwork=[]
revenue=[]
extCost=[]
revfromB=[]
csB=[]
revfromF=[]
csF=[]
revfromW=[]
csW=[]
trucks.append(userresults.travelerType.value_counts()['trucks'])
print(trucks)
work.append(userresults.travelerType.value_counts()['W'])
print(work)
nwork.append(userresults.travelerType.value_counts()['N'])
print(nwork)
welfare.append(sum(userresults['surplus'])+sum(userresults['fee'])-float(mileage)*100000*float(ext)) 
print(welfare)
welfareno.append(sum(userresults['surplus'])-float(mileage)*100000*float(ext))
print(welfareno)
cs.append(sum(userresults['surplus']))
print(cs)
revenue.append(sum(userresults['fee']))
print(revenue)
extCost.append(float(mileage)*100000*float(ext))
print(extCost)
######### WELFARE Brussels #############################
revfromB.append(sum(userresultsB['fee'])) 
print(revfromB)
csB.append(sum(userresultsB['surplus']))
print(csB)
csB[0]+revenue[0]
######### WELFARE Flanders #############################
revfromF.append(sum(userresultsF['fee'])) 
print(revfromF)
csF.append(sum(userresultsF['surplus']))
print(csF)
######### WELFARE W #############################
revfromW.append(sum(userresultsW['fee'])) 
print(revfromW)
csW.append(sum(userresultsW['surplus']))
print(csW)


#####################################################
workbook = xlsxwriter.Workbook('csEnter300.xlsx')
worksheet = workbook.add_worksheet()
array = [welfareno,
         welfare,
         revenue,
         csB,
         revfromB,
         csF,
         revfromF,
         csW,
         revfromW,
         cs,
         trucks,
         work,
         nwork,
         extCost]
row = 0
for col, data in enumerate(array):
    worksheet.write_column(row, col, data)
workbook.close()
#####################################################
############################################################################
############################################################################
#### fine toll ####
"""How this toll setting script works:
    "read the link_results.tsv file (contains link specific results: inflow
    outflow of each link in each interval and in each direction) 
    pick the information on congestion (inflow and outflow) of links,     
    add a toll for a certain interval according to a rule,
    write this in a toll.tsv file (link,values,times,traveler_type)
    REMEMBER TO MAKE SIMULATION PUBLIC (NO LOGIN REQUIRED)
    """
###############################################################################   
import requests  #for taking tsv files from metro-web
import pandas #dataframe tool
import numpy as np # array tool
#import scipy.sparse as sparse
#from selenium import webdriver #for taking particular cell in the metro-web aggregate result table

#################### NEED ONLY ONCE # create list #compute link occupancy 
linkinfo = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\dlink.tsv", sep="\t")
linkinfo['maxval']=''        
for row in linkinfo.itertuples(): #for loop is to  be avoided but itertupeles is faster
    linkinfo['maxval']=linkinfo['lanes']*linkinfo['length']*linkinfo['capacity']*10/linkinfo['speed']
##########################################
# START HERE FOR RUN>1
#########################################
run=9715 #the run number shown on metro-web
#url0 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run) # the number in the middle is your own simulation number
#driver = webdriver.Chrome(executable_path=r"/Volumes/Samsung_T5/METROPOLIS/metro/chromedriver") 
#driver.get(url0)
#mileage=driver.find_element_by_xpath("//html/body/div[1]/div[1]/div/table/tbody/tr[1]/td[10]").text
#driver.close()

#####################change before run
mileage = 2.68209
ext =0.04
step=1
alpha=14.5   
########################################################################
interval = 15
dimin = 4* 6 #for 15min interval, 6 hours
#########################################################################
#url00 = "https://metropolis.sauder.ubc.ca/174/run/2081/user_output" 
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
#first no is the simulation number and second is the run number
#loop over the run number for each iteration
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  

#r00 = requests.get(url00)
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)

#with open("user_results.tsv",'wb') as f00: 
#    f00.write(r00.content)
#userresults00 = pandas.read_csv("user_results.tsv", sep="\t")  

with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content) 
#####################################################
# take link_result.tsv to calculate toll
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results.tsv for calculation of welfare
userresults = pandas.read_csv("user_results.tsv", sep="\t")
###################################################
welfare=[]
welfareno=[]
cs=[]
extCost=[]
# calculate welfare
welfare.append(sum(userresults['surplus'])+sum(userresults['fee'])-float(mileage)*100000*0.04) 
print(welfare)
welfareno.append(sum(userresults['surplus'])-float(mileage)*100000*0.04)
print(welfareno)
cs.append(sum(userresults['surplus']))
print(cs)
extCost.append(float(mileage)*100000*float(ext))
print(extCost)

linkresults.to_numpy
linkinfo.to_numpy
linkresults1 = np.array(linkresults)
linkinfo1 = np.array(linkinfo)
#or########################################################################
#create zero matrix for initial toll
##################OR#######################################################
##################OR#######################################################
ptoll=np.zeros((len(linkresults),dimin))
##################OR#######################################################
ptoll0 = pandas.read_csv(r"D:\METROPOLIS\finetoll_9713.csv", sep=",",header=None)
#2207,8231,8423,8876,9080,9081,9082
#cap75, 9084
ptoll=ptoll0
ptoll = ptoll.to_numpy()
##################OR#######################################################
##################OR#######################################################
#########################################################################
occ = []
for t in range(1,dimin+1):
    occ1 = linkresults1[:,1*dimin+t]-linkresults1[:,3*dimin+t]
    occ.append(occ1)
for t in range(1,dimin):
    for i in range(0,len(linkresults1)):
        occ[t][i] = occ[t][i] + occ[t-1][i]
occ=np.asarray(occ) 
occt=occ.transpose()
#########################################################################
ptoll1=[]
ptoll0=[]
for t in range(1,dimin+1):
    #a = ptoll[:,t-1]+(step*alpha*(linkinfo1[:,3]/linkinfo1[:,4]*(
        #linkresults1[:,t]-(linkinfo1[:,9]/3))/(linkinfo1[:,9]/3)))   
    a = ptoll[:,t-1]+(step*alpha*(linkinfo1[:,3]/linkinfo1[:,4]*(
        occt[:,t-1]-(linkinfo1[:,9]))/(linkinfo1[:,9])))  
    a = a.clip(min=0)
    ptoll0 = np.concatenate((ptoll0,a),axis=0)
ptoll0 = np.reshape(ptoll0,(len(linkresults),dimin))

np.savetxt(r"D:\METROPOLIS\finetoll_"+str(run)+".csv", ptoll0, delimiter=",")
#########################################################################
    
x = np.zeros(len(linkresults))
ptoll1=np.column_stack((x,ptoll0,x))

linkresults['ptollval'] = ptoll1.tolist()
linkresults['ptollval'] = linkresults['ptollval'].astype(str).str[1:-1]
linkresults['ptolltimes']='' 

for t in range(0,dimin+1):
    linkresults['ptolltimes']+=str(300+t*interval)+','
linkresults['ptolltimes']=linkresults['ptolltimes'].astype(str).str[:-1]
#########################################################################
#########################################################################
# form a dict for ptolltimes and ptollval? if ptollval==0, delete ptolltimes
#########################################################################
#########################################################################
#create toll.tsv
linkresults = linkresults.rename(columns = {"ptollval": "values","ptolltimes":"times"})
header = ['link', 'values', 'times']
linkresults.to_csv(r"D:\METROPOLIS\finetoll_"+str(run)+".tsv", sep="\t",index=False,columns = header)

########################################
#### toll cap #########################
########################################
tollcap = 0.75
tollcap = 0.5
#run 9081 at max, toll script at 9080 is best
run=9080
ptollcap0 = pandas.read_csv(r"D:\METROPOLIS\finetoll_"+str(run)+".csv", sep=",",header=None)
ptollcap = ptollcap0*tollcap

x = np.zeros(len(linkresults))
ptollcap1=np.column_stack((x,ptollcap,x))

linkresults['ptollval'] = ptollcap1.tolist()
linkresults['ptollval'] = linkresults['ptollval'].astype(str).str[1:-1]
linkresults['ptolltimes']='' 

for t in range(0,dimin+1):
    linkresults['ptolltimes']+=str(300+t*interval)+','
linkresults['ptolltimes']=linkresults['ptolltimes'].astype(str).str[:-1]

#create toll.tsv
linkresults = linkresults.rename(columns = {"ptollval": "values","ptolltimes":"times"})
header = ['link', 'values', 'times']
linkresults.to_csv(r"D:\METROPOLIS\finetollCap75_"+str(run)+".tsv", sep="\t",index=False,columns = header)


#########################################################################
#########################################################################
usermerged=pandas.merge(userresults00[['origin','destination','travelerType','surplus','fee','td','ta']], userresults[['origin','destination','travelerType','surplus','fee','td','ta']], on=['origin','destination','travelerType'], how='inner')
usermerged1=usermerged[usermerged.fee_x == 0]
usermerged['gainQ'] = np.where(usermerged['surplus_y']-usermerged['surplus_x']>0, 1, 0)
gainers.append(sum(usermerged['gainQ']))
usermerged['losers']=usermerged['surplus_y']-usermerged['surplus_x']
usermerged['tt_x']=usermerged['ta_x']-usermerged['td_x']
usermerged['tt_y']=usermerged['ta_y']-usermerged['td_y']
usergainers= usermerged[usermerged.origin==1146]
usergainers= usergainers[usergainers.destination==1158]
usergainers.mean(axis=0)

import matplotlib.pyplot as plt
usergainers['td_x']=300+usergainers['td_x']/60
usergainers['td_y']=300+usergainers['td_y']/60

plt.hist(usergainers['td_x'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
##plt.hist(usergainers['td_y'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
#         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
#         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
#         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
#         650,655,660])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('departure time:before')
plt.grid(True)
fig = plt.gcf()
plt.show()
fig.savefig('/Users/username/Desktop/depart1146_pre.png')

plt.hist(usergainers['td_y'],bins=[300,305,310,315,320,325,330,335,340,345,350,355,360,
         365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,
         460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,
         555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,
         650,655,660])
plt.xlabel('departure time', fontsize=16)
plt.ylabel('frequency',fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('departure time:after')
plt.grid(True)
fig = plt.gcf()
plt.show()
fig.savefig('/Users/username/Desktop/depart1146_post.png')