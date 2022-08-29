#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:53:41 2019


"""

import csv
import pandas as pd
import numpy as np

#repeat for VL and VZ
df=pd.read_csv(r"/Users/username/Desktop/Brussels calibration/related files and coor/demandVZ.csv",sep=";",header=None)
o=[]
d=[]
p=[]
for i in range(1,1062):
    for j in range(1,1062):
        if i==j:
            pass
        else:
            o.append(df.at[i,0]) 
            d.append(df.at[0,j]) 
            p.append(df.at[i,j])
for i in range(0,len(p)):
    p[i]=str(p[i])
    if len(p[i])>1 and p[i][1]==',':
        p[i]=p[i].replace(',','')
        p[i]=float(p[i])
    else:
        p[i]=float(p[i])

for i in range(0,len(d)):
    d[i]=str(d[i])
    if d[i][-1]=='0' and d[i][-2]=='.':
        d[i]=d[i][:-2]
    elif d[i][1]==',':
        d[i]=d[i].replace(',','')
    else:
        pass
rows=zip(o,d,p)          
with open (r"/Users/username/Desktop/Brussels calibration/odVZ.tsv",'w') as tsvout:
    writer = csv.writer(tsvout,delimiter='\t',lineterminator='\n') 
    for row in rows:        
        writer.writerow(row)        
#  add manually column names : orgin destinationpopulation
        

odVL = pd.read_csv(r"/Users/username/Desktop/Brussels calibration/odVL.tsv", sep="\t")
odVZ = pd.read_csv(r"/Users/username/Desktop/Brussels calibration/odVZ.tsv", sep="\t")

odVL["poptruck"] = " "
odVL["poptruck"] = 2.5 * odVL['population']+3.5*odVZ['population']

odVL=odVL[odVL.poptruck != 0]

odVL.rename(columns={'population':'vlonly','poptruck':'population'}, 
                 inplace=True)
odVL[['origin','destination','population']].to_csv(r"/Users/username/Desktop/odtruck.tsv",sep="\t",index=False)

####################################
# for odPW, we need to generate an OD-matrix to include the PT travellers 
# this is done by using the mode shares by distance

# read PW file first


gpzone = pd.read_csv(r"/Users/username/Desktop/Brussels calibration/zonetomain.csv", sep=",")
odPW = pd.read_csv(r"/Users/username/Desktop/Brussels calibration/s_odPW.tsv", sep="\t")
coordinates = pd.read_csv(r"/Users/username/Desktop/Brussels calibration/related files and coor/corr4.csv", sep=",")
#match and insert a "MAINZONE" column 
PWzonesgp1 = pd.merge(odPW,gpzone[['ZONE','MAINZONE']],left_on='origin',right_on='ZONE')
PWzonesgp2 = pd.merge(PWzonesgp1,gpzone[['ZONE','MAINZONE']],left_on='destination',right_on='ZONE')
pttime = pd.read_csv(r"D:\METROPOLIS\Brussels calibration\pt2.csv", sep=",")
PWzonesgp2.rename(columns={'MAINZONE_x':'omzone','MAINZONE_y':'dmzone'}, 
                 inplace=True)
ptdist = pd.merge(PWzonesgp2,pttime[['distance','travel time','omzone','dmzone']],on=['omzone', 'dmzone'])

ptdist.distance.fillna(0.1,inplace=True)

ptdist['mul'] = ptdist['distance']
ptdist.loc[ptdist['distance'] >=40, 'mul'] = 1.49
ptdist.loc[ptdist['distance']<40,'mul']=1.28
ptdist.loc[ptdist['distance']<25,'mul']=1.11
ptdist.loc[ptdist['distance']<15,'mul']=1.18
ptdist.loc[ptdist['distance']<10,'mul'] = 1.14
ptdist.loc[ptdist['distance']< 7.5, 'mul'] = 1.08

# share column
ptdist['PTshare'] = ptdist['distance']
ptdist.loc[ptdist['distance'] >=40, 'PTshare'] = 0.12
ptdist.loc[ptdist['distance']<40,'PTshare']=0.33
ptdist.loc[ptdist['distance']<25,'PTshare']=0.22
ptdist.loc[ptdist['distance']<15,'PTshare']=0.1
ptdist.loc[ptdist['distance']<10,'PTshare'] = 0.15
ptdist.loc[ptdist['distance']< 7.5, 'PTshare'] = 0.08

ptdist['tpop']=''
ptdist.rename(columns={'population':'pop'}, 
                 inplace=True)
ptdist['tpop']=ptdist['pop']*ptdist['mul']
ptdist.rename(columns={'tpop':'population'}, 
                 inplace=True)

ptdist[['origin','destination','population']].to_csv(r"/Users/username/Desktop/odPW_dist.tsv",sep="\t",index=False)
ptdist.to_csv(r"/Users/username/Desktop/ptdist_full.tsv",sep="\t",index=False)

#put odPW into two groups only (W and N)
ptdist['Wpop']=''
ptdist['Wpop']=ptdist['population']*0.32
ptdist['Npop']=''
ptdist['Npop']=ptdist['population']*0.68


ptdist[['origin','destination','Wpop']].to_csv(r"/Users/Desktop/odPW_W_dist.tsv",sep="\t",index=False)
ptdist[['origin','destination','Npop']].to_csv(r"/Users/Desktop/odPW_N_dist.tsv",sep="\t",index=False)


##put odPW into four groups: HW, HN, LW,LN
#ptdist['HWpop']=''
#ptdist['HWpop']=ptdist['population']*0.3227
#ptdist['HNpop']=''
#ptdist['HNpop']=ptdist['population']*0.6773
#ptdist['LWpop']=''
#ptdist['LWpop']=ptdist['population']*0.21627
#ptdist['LNpop']=''
#ptdist['LNpop']=ptdist['population']*0.78373
#
#ptdist[['origin','destination','HWpop']].to_csv(r"/Users/Desktop/odPW_HW_dist.tsv",sep="\t",index=False)
#ptdist[['origin','destination','HNpop']].to_csv(r"/Users/Desktop/odPW_HN_dist.tsv",sep="\t",index=False)
#ptdist[['origin','destination','LWpop']].to_csv(r"/Users/Desktop/odPW_LW_dist.tsv",sep="\t",index=False)
#ptdist[['origin','destination','LNpop']].to_csv(r"/Users/Desktop/odPW_LN_dist.tsv",sep="\t",index=False)
#
