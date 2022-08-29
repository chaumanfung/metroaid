#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:54:19 2019


"""

# merge od file with mainzone
import pandas
import numpy as np

gpzone = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\zonetomain.csv", sep=",")
gpzone['MAINZONE'].nunique()
odPW = pandas.read_csv(r"/Users/Desktop/Brussels calibration/s_odPW.tsv", sep="\t")
coordinates = pandas.read_csv(r"/Users/Desktop/Brussels calibration/related files and coor/corr4.csv", sep=",")
#match and insert a "MAINZONE" column 
PWzonesgp1 = pandas.merge(odPW,gpzone[['ZONE','MAINZONE']],left_on='origin',right_on='ZONE')
PWzonesgp2 = pandas.merge(PWzonesgp1,gpzone[['ZONE','MAINZONE']],left_on='destination',right_on='ZONE')
PWzonesgp3 = PWzonesgp2.drop_duplicates(subset=['MAINZONE_x','MAINZONE_y'], keep='first')
PWzonesgp4 = pandas.merge(PWzonesgp3,coordinates[['Y','X','id']],left_on='origin',right_on='id')
PWzonesgp5 = pandas.merge(PWzonesgp4,coordinates[['Y','X','id']],left_on='destination',right_on='id')

# importing googlemaps module 
import googlemaps
import csv

# Requires API key 
#gmaps = googlemaps.Client(key='') 


###########################################################
# queries
#my_dist=[]
for i in range(0,9016): 
    my_dist.append(gmaps.distance_matrix((PWzonesgp5['Y_x'][i],PWzonesgp5['X_x'][i]),(PWzonesgp5['Y_y'][i],PWzonesgp5['X_y'][i]) 
                                ,mode="transit")['rows'][0]['elements'][0] )

# Printing the result 
#print(my_dist)

# write to tsv
pandas.DataFrame.from_dict(data=my_dist,orient='columns').to_csv('test_pt.csv',header=True)

#write results and google coordinates of o and d to tsv
pt1=open(r'/Users/Desktop/Brussels calibration/pt1.csv','w')
s=[]
u=[]
ocx=[]
ocy=[]
ozone=[]
omzone=[]
dcx=[]
dcy=[]
dzone=[]
dmzone=[]
for k in range(0,len(my_dist)):
    if my_dist[k]['status']=='OK':
        s.append(my_dist[k]['distance']['text'])
        u.append(my_dist[k]['duration']['text'])
    else:
        s.append('NA')
        u.append('NA')
for i in range(0,9016):
           ocx.append(PWzonesgp5['Y_x'][i])
           ocy.append(PWzonesgp5['X_x'][i])
           ozone.append(PWzonesgp5['ZONE_x'][i])
           omzone.append(PWzonesgp5['MAINZONE_x'][i])
           dcx.append(PWzonesgp5['Y_y'][i])
           dcy.append(PWzonesgp5['X_y'][i])
           dzone.append(PWzonesgp5['ZONE_y'][i])
           dmzone.append(PWzonesgp5['MAINZONE_y'][i])

rows = zip(s,u,ocx,ocy,ozone,omzone,dcx,dcy,dzone,dmzone)
with open (r'/Users/Desktop/Brussels calibration/pt1.csv','w') as csvout:
    writer = csv.writer(csvout,delimiter=',',lineterminator='\n') 
    for row in rows:         
        writer.writerow(row)


#remove units of the columns
with open(r'/Users/Desktop/Brussels calibration/pt1.csv','r') as csvin, open(r'/Users/Desktop/Brussels calibration/pt2.csv','w') as csvout:
    csvin = csv.reader(csvin, delimiter=',',lineterminator='\n')
    csvout = csv.writer(csvout, delimiter=',',lineterminator='\n')
    
    for line in csvin:
        line[0] = line[0][:-3] #delete km
        if 'hour' not in line[1]:
            line[1] = line[1][:-5] #delete mins
        elif 'hours'in line[1]:
            h,m =line[1].split("hours")
            if 'mins'in m:
                m= m[:-5] #delete mins
            else:
                m = m[:-4]
            m = float(m)
            h=float(h)
            line[1]=60*float(h)+float(m)
           
        else:
            h,m =line[1].split("hour")
            if 'mins'in m:
                m= m[:-5] #delete mins
            else:
                m = m[:-4]
            
            m = float(m)
            h=float(h)
            line[1]=60*float(h)+float(m)

        csvout.writerow(line)

pttime = pandas.read_csv(r"/Users/Desktop/Brussels calibration/pt2.csv", sep=",")
PWzonesgp2.rename(columns={'MAINZONE_x':'omzone','MAINZONE_y':'dmzone'}, 
                 inplace=True)
pttime1 = pandas.merge(PWzonesgp2,pttime[['distance','travel time','omzone','dmzone']],on=['omzone', 'dmzone'])

pttime1.rename(columns={'travel time':'traveltime'}, 
                 inplace=True)
pttime1.fillna(10,inplace=True)

pttime1.rename(columns={'traveltime':'travel time'}, 
                 inplace=True)
pttime1[['origin','destination','travel time']].to_csv(r"/Users/Desktop/pttime.tsv",sep="\t",index=False)
pttime1.to_csv(r"/Users/Desktop/pttime_full.tsv",sep="\t",index=False)

