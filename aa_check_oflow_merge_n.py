# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 12:51:33 2019



"""
# need to rewrite the check of simulation flow to be faster; it has to be rerun every simulation
import pandas as pd
import requests 
###################################### 
#need to be reloaded every calibration
######################################

#import link_result from metropolis        
# column9, chk_oflow2.tsv is the field flow
# sum link_result for each link 
run=2207
url1 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/link_output"  
#first no is the simulation number and second is the run number
url2 = "https://metropolis.sauder.ubc.ca/174/run/"+str(run)+"/user_output"  
r1 = requests.get(url1) # create HTTP response object 
r2 = requests.get(url2)

with open("link_results.tsv",'wb') as f1: 
    f1.write(r1.content) 
with open("user_results.tsv",'wb') as f2: 
    f2.write(r2.content)

#dfin3 = pd.read_csv("link_results.tsv", sep="\t",usecols=fields)  
dfin3 = pd.read_csv("link_results.tsv", sep="\t")   
#dfin3.loc[:,'total']=dfin3.drop('link', axis=1).sum(axis=1)
dfin3['in-flow_H_total']=dfin3.iloc[:,1:72].sum(axis=1)
dfin3['in-flow_S_total']=dfin3.iloc[:,73:144].sum(axis=1)
dfin3['out-flow_H_total']=dfin3.iloc[:,145:216].sum(axis=1)
dfin3['out-flow_S_total']=dfin3.iloc[:,217:288].sum(axis=1)

# putting them together as X and Y
#dfin4 = pd.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/chk_oflow2.tsv", sep="\t", names=["0",
#                "1","2","3","4","5","6","7","8","field","10","11","link"])
dfin4 = pd.read_csv(r"D:\METROPOLIS\Brussels calibration\chk_oflow2.tsv", sep="\t", names=["0",
                "1","2","3","4","5","6","7","8","field","10","11","link"])
dfinflow = pd.merge(dfin3[["link","in-flow_H_total",'in-flow_S_total','out-flow_H_total','out-flow_S_total']],dfin4[["link","field"]],on="link")

# regression to see if they match
## Without a constant

import statsmodels.api as sm
import matplotlib.pyplot as plt

X = dfinflow['in-flow_S_total'] #metropolis
#X = dfinflow['out-flow_S_total'] #metropolis
Y = dfinflow["field"] #field

# Note the difference in argument order
linkcountnt = sm.OLS(Y, X).fit()
predictions = linkcountnt.predict(X) # make the predictions by the model

# Print out the statistics
linkcountnt.summary()
print(linkcountnt.summary().as_latex())
# plot
# scatter-plot data
plt.scatter(X, Y, s=5, label='data points')

# plot regression line and the line for perfect match
plt.plot(X, predictions,color='r',label='reg line')
plt.plot(X, 10*X, color='g',label='metro=field')
plt.xlabel('metropolis')
plt.ylabel('field')
plt.title('field flow vs simulated flow')
plt.legend(loc='upper left')
fig = plt.gcf()
plt.show()
fig.savefig(r'D:\METROPOLIS\nov2020\flow.png')
    