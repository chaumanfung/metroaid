# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:26:16 2019

@author: chauman.fung@kuleuven.be
"""

import csv
from itertools import islice

with open(r'C:\Users\u0087328\Desktop\Brussels calibration\b_links.tsv','r') as tsvin, \
open(r'C:\Users\u0087328\Desktop\Brussels calibration\b_links2.tsv', 'w') as tsvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvout = csv.writer(tsvout, delimiter='\t',lineterminator='\n')

    for line in islice(tsvin, 1, None):
        line.insert(0, '') #add blank column for name
        line.insert(0, '2') # add function column, function 2 (bottleneck)
        line.insert(0, '') #insert capacity per lane column 
        line[0] = float(line[9])/float(line[6])  #calculate capacity per lane
        del line[-1]
        line[7] = line[7][:-2] #remove km
        line[8] = line[8][:-4] #remove km/h
        
#        tsvout.writerow(['capacity','function','name','id','origin','destination',
            #           'lanes','length','speed'])
    
        tsvout.writerow(line)


#capacity	function	name	id	origin	destination	lanes	length	speed