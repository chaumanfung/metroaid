# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 18:10:46 2020


"""
## comparing results from different number of iterations ##
## 100: 2207, 50: 4614, 20: 4613
import pandas
import requests

######################################
run = 2207 #99
run = 4614 #49
run = 4613 #19

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
linkresults19 = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results. tsv too for calculation of welfare
uresults19 = pandas.read_csv("user_results.tsv", sep="\t")
#####################################################
# Run OLS with iter99 results being 'explained' by iter49 and iter19 results

linkresults99['in-flow_H_total']=linkresults99.iloc[:,1:72].sum(axis=1)
linkresults99['in-flow_S_total']=linkresults99.iloc[:,73:144].sum(axis=1)
linkresults99['out-flow_H_total']=linkresults99.iloc[:,145:216].sum(axis=1)
linkresults99['out-flow_S_total']=linkresults99.iloc[:,217:288].sum(axis=1)

linkresults49['in-flow_H_total']=linkresults49.iloc[:,1:72].sum(axis=1)
linkresults49['in-flow_S_total']=linkresults49.iloc[:,73:144].sum(axis=1)
linkresults49['out-flow_H_total']=linkresults49.iloc[:,145:216].sum(axis=1)
linkresults49['out-flow_S_total']=linkresults49.iloc[:,217:288].sum(axis=1)

linkresults19['in-flow_H_total']=linkresults19.iloc[:,1:72].sum(axis=1)
linkresults19['in-flow_S_total']=linkresults19.iloc[:,73:144].sum(axis=1)
linkresults19['out-flow_H_total']=linkresults19.iloc[:,145:216].sum(axis=1)
linkresults19['out-flow_S_total']=linkresults19.iloc[:,217:288].sum(axis=1)

iterinflow49 = pandas.merge(linkresults99[["link","in-flow_H_total",'in-flow_S_total','out-flow_H_total','out-flow_S_total']],linkresults49[["link","in-flow_H_total",'in-flow_S_total','out-flow_H_total','out-flow_S_total']],on="link")

# regression to see if they match
## Without a constant

import statsmodels.api as sm
import matplotlib.pyplot as plt

Y = iterinflow49['in-flow_S_total_x'] #99
X = iterinflow49['in-flow_S_total_y'] #49

# Note the difference in argument order
linkcount49 = sm.OLS(Y, X).fit()
predictions = linkcount49.predict(X) # make the predictions by the model

# Print out the statistics
linkcount49.summary()
#print(linkcount49.summary().as_latex())
# plot
# scatter-plot data
plt.scatter(X, Y, s=5, label='data points')

# plot regression line and the line for perfect match
plt.plot(X, predictions,color='r',label='reg line')
plt.plot(X, X, color='g',label='iter99=iter49')
plt.xlabel('iter49')
plt.ylabel('iter99')
plt.title('iter99 vs iter49')
plt.legend(loc='upper left')
fig = plt.gcf()
plt.show()
fig.savefig(r'D:\METROPOLIS\nov2020\iterFlow49.png')


iterinflow19 = pandas.merge(linkresults99[["link","in-flow_H_total",'in-flow_S_total','out-flow_H_total','out-flow_S_total']],linkresults19[["link","in-flow_H_total",'in-flow_S_total','out-flow_H_total','out-flow_S_total']],on="link")

# regression to see if they match
## Without a constant

#import statsmodels.api as sm
#import matplotlib.pyplot as plt

Y = iterinflow19['in-flow_S_total_x'] #99
X = iterinflow19['in-flow_S_total_y'] #19

# Note the difference in argument order
linkcount19 = sm.OLS(Y, X).fit()
predictions = linkcount19.predict(X) # make the predictions by the model

# Print out the statistics
linkcount19.summary()
#print(linkcount49.summary().as_latex())
# plot
# scatter-plot data
plt.scatter(X, Y, s=5, label='data points')

# plot regression line and the line for perfect match
plt.plot(X, predictions,color='r',label='reg line')
plt.plot(X, X, color='g',label='iter99=iter19')
plt.xlabel('iter19')
plt.ylabel('iter99')
plt.title('iter99 vs iter19')
plt.legend(loc='upper left')
fig = plt.gcf()
plt.show()
fig.savefig(r'D:\METROPOLIS\nov2020\iterFlow19.png')
    