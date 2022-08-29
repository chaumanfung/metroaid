#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 17:01:32 2019


"""

import pandas as pd

# conda activate metro
# conda install -c anaconda xlrd

table_zones= pd.read_excel (r'/Users/Desktop/zones_n.xlsx', sheet_name='Sheet1')
table_nodes= pd.read_excel (r'/Users/Desktop/nodes_n.xlsx', sheet_name='Sheet1')
table_links= pd.read_excel (r'/Users/Desktop/links_n.xlsx', sheet_name='Sheet1')
table_connectors= pd.read_excel (r'/Users/Desktop/connectors_n.xlsx', sheet_name='Sheet1')

# links
table_nodes['node_old2']=table_nodes['node_old']
table_nodes.rename(columns={'node_old':'from_node_old','node_old2':'to_node_old'}, 
                 inplace=True)
table_linksm1 = pd.merge(table_links,table_nodes[['from_node_old','node_new']],on=['from_node_old'])
table_linksm2 = pd.merge(table_linksm1,table_nodes[['to_node_old','node_new']],on=['to_node_old'])

#print (table_linksm2.dtypes)
table_linksm2['function']=2 #bottleneck function
table_linksm2['length'] = table_linksm2['length'].map(lambda x: x.rstrip('km'))
table_linksm2['speed'] = table_linksm2['speed'].map(lambda x: x.rstrip('km/h'))

table_linksm2=table_linksm2[table_linksm2.tsysset == 'PW,VL,VZ,W']

#table_linksm2['speed']=pd.to_numeric(table_linksm2['speed'], downcast='float')
#table_linksm2=table_linksm2[table_linksm2.speed != 0]
#table_linksm2=table_linksm2[table_linksm2.capacity != 0]
#table_linksm2=table_linksm2[table_linksm2.lane != 0]

table_linksm2.rename(columns={'capacity':'capacity_all'}, 
                 inplace=True)
table_linksm2['capacity']=table_linksm2['capacity_all']/table_linksm2['lane']

table_linksm2.rename(columns={'link_new':'id','node_new_x':'origin','node_new_y':'destination','lane':'lanes'}, 
                 inplace=True)

# connectors
table_con_o=table_connectors[table_connectors.direction == 'O']
table_con_d=table_connectors[table_connectors.direction == 'D']

table_con_o.rename(columns={'node_old':'to_node_old'}, 
                 inplace=True)
table_con_o = pd.merge(table_con_o,table_nodes[['to_node_old','node_new']],on=['to_node_old'])
table_con_o['function']=1 #freeflow function
table_con_o['lanes']=1 
table_con_o['length'] = table_con_o['length'].map(lambda x: x.rstrip('km'))
table_con_o['speed']=45
table_con_o['capacity']=99999  
table_con_o.rename(columns={'linkcon':'id','zone':'origin','node_new':'destination'}, 
                 inplace=True)

table_con_d.rename(columns={'node_old':'from_node_old'}, 
                 inplace=True)
table_con_d = pd.merge(table_con_d,table_nodes[['from_node_old','node_new']],on=['from_node_old'])
table_con_d['function']=1 #freeflow function
table_con_d['lanes']=1 
table_con_d['length'] = table_con_d['length'].map(lambda x: x.rstrip('km'))
table_con_d['speed']=45
table_con_d['capacity']=99999  
table_con_d.rename(columns={'linkcon':'id','zone':'destination','node_new':'origin'}, 
                 inplace=True)

table_con_od = pd.concat([table_con_o,table_con_d])
table_con_od.rename(columns={'link_con':'id'}, 
                 inplace=True)

# export links and connectors
table_linkscon= pd.concat([table_con_od,table_linksm2])
table_linkscon[['id','origin','destination','function','lanes','length','speed','capacity']].to_csv(r"/Users/Desktop/newlinks.tsv",sep="\t",index=False)

######################################
# export zones 
table_zones.rename(columns={'zone':'id','xcoor':'x','ycoor':'y'}, 
                 inplace=True)
table_zones[['id','x','y']].to_csv(r"/Users/Desktop/newzones.tsv",sep="\t",index=False)

# export nodes
table_nodes.rename(columns={'node_new':'id','xcoor':'x','ycoor':'y'}, 
                 inplace=True)
table_nodes[['id','x','y']].to_csv(r"/Users/Desktop/newnodes.tsv",sep="\t",index=False)

######################################
dPWgrouped=demandPW2.groupby(['MAINZONE_x','MAINZONE_y'])
#dPWgrouped.groups.keys()
dPW_BB=dPWgrouped.get_group((1,1))
dPW_BW=dPWgrouped.get_group((1,2))
dPW_BF=dPWgrouped.get_group((1,3))