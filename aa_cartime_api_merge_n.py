# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:31:24 2019


"""

#import googlemaps
import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm
import requests 

#large = pandas.read_csv(r"/Volumes/Samsung_T5/METROPOLIS/Brussels calibration/large1000.csv")
large = pandas.read_csv(r"D:\METROPOLIS\Brussels calibration\large1000.csv")
large["metrodur"]='' 
######################################
run = 2207
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
linkresults = pandas.read_csv("link_results.tsv", sep="\t")
# need user_results. tsv too for calculation of welfare
uresults = pandas.read_csv("user_results.tsv", sep="\t")
################################################### 
#uresults = pandas.read_csv(r"/Users/username/Desktop/user_results.tsv", sep="\t")
uresults['odgroup']=''
uresults['simdur'] = (uresults['ta'] - uresults['td'])
# add up the trip time and individuals with the large ODs

df = pandas.merge(large[["origin","destination","population","duration"]],
                  uresults[["origin","destination","travelerType","simdur"]],on=["origin","destination"])
a=df.groupby(['origin','destination'])['simdur'].mean()
dfout=pandas.merge(large[["origin","destination","population","distance","duration"]],
                  a,on=["origin","destination"])


# regression to compare simulated time and field time
# field time= duration
# simulated time= simdur
# regression to see if they match
## Without a constant


X = dfout["simdur"] #metropolis
Y = large["duration"] #field

# Note the difference in argument order
vsduration = sm.OLS(Y, X).fit()
predictions = vsduration.predict(X) # make the predictions by the model

# Print out the statistics
vsduration.summary()
print(vsduration.summary().as_latex())
# plot
# scatter-plot data
plt.scatter(X, Y, s=5, label='data points')

# plot regression line and the line for perfect match
plt.plot(X, predictions,color='r',label='reg line')
plt.plot(X, X, color='g',label='metro=field')
plt.xlabel('metropolis')
plt.ylabel('field')
plt.title('google duration vs metropolis trip time')
plt.legend(loc='upper left')
fig = plt.gcf()
plt.show()
fig.savefig(r'D:\METROPOLIS\nov2020\triptime.png')

