#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 15:27:34 2020


"""

import pandas #dataframe tool

link = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/links.tsv", sep="\t") 
demand_truck = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/od_matrix.tsv", sep="\t") 
demand_w = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/od_matrix(1).tsv", sep="\t") 
demand_n = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/od_matrix(2).tsv", sep="\t") 

link['capacity']=link['capacity']/10
demand_truck['population']=demand_truck['population']/10
demand_w['population']=demand_w['population']/10
demand_n['population']=demand_n['population']/10

link.to_csv(r"/Volumes/Samsung_T5/METROPOLIS/s_link.tsv", sep="\t",index=False)
demand_truck.to_csv(r"/Volumes/Samsung_T5/METROPOLIS/s_od_truck.tsv", sep="\t",index=False)
demand_w.to_csv(r"/Volumes/Samsung_T5/METROPOLIS/s_od_w.tsv", sep="\t",index=False)
demand_n.to_csv(r"/Volumes/Samsung_T5/METROPOLIS/s_od_n.tsv", sep="\t",index=False)


########################################################

run = 2207
toll = pandas.read_csv(r"D:\METROPOLIS\03052020\finetoll_5_"+str(run)+".tsv", sep="\t") 
s = "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
toll_0 = toll[toll.values==s]
toll['zero'] = toll['values']==s
toll_n0 = toll[toll.zero == False]

header = ['link', 'values', 'times']
toll_n0.to_csv(r"D:\METROPOLIS\03052020\finetoll_5_"+str(run)+".tsv", sep="\t",index=False,columns = header)
