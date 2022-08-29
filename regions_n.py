# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:29:56 2019



This script put different zones and links in different regions
"""

import pandas
#import matplotlib.pyplot as plt
#import statsmodels.api as sm
#import numpy as np
zone_node = pandas.read_csv(r"/Volumes/Samsung_T5/zone_node.csv", sep=",")
links = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/input_NETWORK/links_n.csv",sep=",")
mainzone = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/mainzone.csv", sep=";")
zone_node.drop_duplicates(subset ="NO",keep = False, inplace = True) 
zone_node = zone_node[['NO','NO_2','PROVINCIE','GEMEENTE','XCOORD','YCOORD']]
zone_node.rename(columns={'NO':'node_old', 'NO_2':'ZONE'},inplace=True)
zone_node2 = pandas.merge(zone_node,mainzone[["ZONE","MAINZONE"]],left_on="ZONE",right_on="ZONE")
links2 = pandas.merge(links,zone_node2[["node_old","ZONE","MAINZONE"]],left_on="from_node_old",right_on="node_old",how="outer")
links3 = pandas.merge(links2,zone_node2[["node_old","ZONE","MAINZONE"]],left_on="to_node_old",right_on="node_old",how="outer")
links3['length'] = links3['length'].astype(str)

################################################################################
################################################################################

tollsys = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/tollsys.csv", sep=";")
matchnode = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/input/wid_n_intersection.tsv", sep="\t")
# match the visum node number to renumber in metropolis input
tollsys1 = pandas.merge(matchnode,tollsys[["FROMNODENO","TONODENO","TOLLSYSTEMNO"]],left_on="NodeNo",right_on="FROMNODENO")
tollsys2 = pandas.merge(matchnode,tollsys1,left_on="NodeNo",right_on="TONODENO")
# put existing zones into mainzones to form 9 user groups
# put existing links into toll system for welfare objectives
dlink = pandas.read_csv(r"/Users/Desktop/Brussels calibration/dlink.tsv", sep="\t")
tollsys2.rename(columns={'2000_x':'origin',
                          '2000_y':'destination',
                          'TOLLSYSTEMNO':'mainzone'}, 
                 inplace=True)


objclass = pandas.merge(dlink,tollsys2[["origin","destination","mainzone"]],on=["origin","destination"])

#for user groups, use the main zone of origin and destination to define
demandPW = pandas.read_csv(r"/Users/Desktop/Brussels calibration/input/odPW.tsv", sep="\t")
demandVL = pandas.read_csv(r"/Users/Desktop/Brussels calibration/input/odVL.tsv", sep="\t")
demandVZ = pandas.read_csv(r"/Users/Desktop/Brussels calibration/input/odVZ.tsv", sep="\t")

demandPW1 = pandas.merge(demandPW,mainzone[["ZONE","MAINZONE"]],left_on="origin",right_on="ZONE")
demandPW2 = pandas.merge(demandPW1,mainzone[["ZONE","MAINZONE"]],left_on="destination",right_on="ZONE")
demandVL1 = pandas.merge(demandVL,mainzone[["ZONE","MAINZONE"]],left_on="origin",right_on="ZONE")
demandVL2 = pandas.merge(demandVL1,mainzone[["ZONE","MAINZONE"]],left_on="destination",right_on="ZONE")
demandVZ1 = pandas.merge(demandVZ,mainzone[["ZONE","MAINZONE"]],left_on="origin",right_on="ZONE")
demandVZ2 = pandas.merge(demandVZ1,mainzone[["ZONE","MAINZONE"]],left_on="destination",right_on="ZONE")

dPWgrouped=demandPW2.groupby(['MAINZONE_x','MAINZONE_y'])
#dPWgrouped.groups.keys()
dPW_BB=dPWgrouped.get_group((1,1))
dPW_BW=dPWgrouped.get_group((1,2))
dPW_BF=dPWgrouped.get_group((1,3))
dPW_WB=dPWgrouped.get_group((2,1))
dPW_WW=dPWgrouped.get_group((2,2))
dPW_WF=dPWgrouped.get_group((2,3))
dPW_FB=dPWgrouped.get_group((3,1))
dPW_FW=dPWgrouped.get_group((3,2))
dPW_FF=dPWgrouped.get_group((3,3))

dVLgrouped=demandVL2.groupby(['MAINZONE_x','MAINZONE_y'])
#dPWgrouped.groups.keys()
dVL_BB=dVLgrouped.get_group((1,1))
dVL_BW=dVLgrouped.get_group((1,2))
dVL_BF=dVLgrouped.get_group((1,3))
dVL_WB=dVLgrouped.get_group((2,1))
dVL_WW=dVLgrouped.get_group((2,2))
dVL_WF=dVLgrouped.get_group((2,3))
dVL_FB=dVLgrouped.get_group((3,1))
dVL_FW=dVLgrouped.get_group((3,2))
dVL_FF=dVLgrouped.get_group((3,3))

dVZgrouped=demandVZ2.groupby(['MAINZONE_x','MAINZONE_y'])
#dPWgrouped.groups.keys()
dVZ_BB=dVZgrouped.get_group((1,1))
dVZ_BW=dVZgrouped.get_group((1,2))
dVZ_BF=dVZgrouped.get_group((1,3))
dVZ_WB=dVZgrouped.get_group((2,1))
dVZ_WW=dVZgrouped.get_group((2,2))
dVZ_WF=dVZgrouped.get_group((2,3))
dVZ_FB=dVZgrouped.get_group((3,1))
dVZ_FW=dVZgrouped.get_group((3,2))
dVZ_FF=dVZgrouped.get_group((3,3))

dPW_BB[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_BB.tsv",sep="\t",index=False)
dPW_BW[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_BW.tsv",sep="\t",index=False)
dPW_BF[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_BF.tsv",sep="\t",index=False)
dPW_WB[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_WB.tsv",sep="\t",index=False)
dPW_WW[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_WW.tsv",sep="\t",index=False)
dPW_WF[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_WF.tsv",sep="\t",index=False)
dPW_FB[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_FB.tsv",sep="\t",index=False)
dPW_FW[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_FW.tsv",sep="\t",index=False)
dPW_FF[['origin','destination','population']].to_csv(r"/Users/Desktop/DPW_FF.tsv",sep="\t",index=False)

dVL_BB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_BB.tsv",sep="\t",index=False)
dVL_BW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_BW.tsv",sep="\t",index=False)
dVL_BF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_BF.tsv",sep="\t",index=False)
dVL_WB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_WB.tsv",sep="\t",index=False)
dVL_WW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_WW.tsv",sep="\t",index=False)
dVL_WF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_WF.tsv",sep="\t",index=False)
dVL_FB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_FB.tsv",sep="\t",index=False)
dVL_FW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_FW.tsv",sep="\t",index=False)
dVL_FF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVL_FF.tsv",sep="\t",index=False)

dVZ_BB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_BB.tsv",sep="\t",index=False)
dVZ_BW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_BW.tsv",sep="\t",index=False)
dVZ_BF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_BF.tsv",sep="\t",index=False)
dVZ_WB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_WB.tsv",sep="\t",index=False)
dVZ_WW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_WW.tsv",sep="\t",index=False)
dVZ_WF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_WF.tsv",sep="\t",index=False)
dVZ_FB[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_FB.tsv",sep="\t",index=False)
dVZ_FW[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_FW.tsv",sep="\t",index=False)
dVZ_FF[['origin','destination','population']].to_csv(r"/Users/Desktop/DVZ_FF.tsv",sep="\t",index=False)