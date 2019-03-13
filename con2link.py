# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:31:58 2019

@author: chauman.fung@kuleuven.be
"""

import csv
from itertools import islice

with open(r'C:\Users\u0087328\Desktop\Brussels calibration\b_connectors.tsv','r') as tsvin, \
open(r'C:\Users\u0087328\Desktop\Brussels calibration\b_con2link.tsv', 'w') as tsvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvout = csv.writer(tsvout, delimiter='\t',lineterminator='\n')
    
    count = 0
    for line in islice(tsvin, 1, None):
        
        if line[2]=="D":
            line.insert(0, '')
            line[1],line[2]=line[2],line[1] #switch od columns
            del line[3] #delete od column
            line.insert(4, '1') #add function column: free flow
            line.insert(5, '1') #add number of lane column: 1
            line.insert(6, '30')    #add speed column
            line.insert(7, '1500')  #add capacity per lane column
            line[3] = line[3][:-2] #delete km
            
        else:
            line.insert(0, '')
            del line[3]
            line.insert(4, '1')
            line.insert(5, '1')
            line.insert(6, '30')
            line.insert(7, '1500')
            line[3] = line[3][:-2]

        count += 1
        line.insert(8, count) #insert count as id
             
        tsvout.writerow(line)

# name	origin	destination	length	function	lanes	speed	capacity	id
