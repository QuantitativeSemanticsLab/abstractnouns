import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pylab
#import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
#import ast
#from itertools import chain 
#from collections import Counter	
#import csv

infile = 'master.csv'
df = pd.read_csv(infile)

#print df["Noun"]
X = 'Bare Plural Noun Percentage'
y = 'Unit Denumerator Percentage'
z = 'Verb Subject Percentage'
dim = 3 #2 or 3
clusternum = 8 #up to 8

from sklearn.cluster import KMeans
if dim == 2:
	subset = df[[X,y]]
if dim ==3:
	subset =df[[X,y,z]]
Y = [tuple(x) for x in subset.values]
kmeans = KMeans(n_clusters=clusternum, random_state=0).fit(Y)
df["clusternum"] = kmeans.labels_


plt.figure(3)
fig = pylab.figure()
ax = Axes3D(fig)
use_colors = {0:"b", 1:"g", 2:"r", 3:"c", 4:"m", 5:"y", 6:"k", 7:"w"}
if dim == 2:
	plt.scatter(df[X], df[y], c=[use_colors[x] for x in df["clusternum"]])
if dim == 3:
	ax.scatter(df[X], df[y], df[z], c=[use_colors[x] for x in df["clusternum"]])
	ax.set_zlabel(z)

plt.xlabel(X)
plt.ylabel(y)
plt.show()

newdf = df.sort(["clusternum"])

for num in range(clusternum):
	print [df["Noun"][i] for i in range(len(newdf)) if df["clusternum"][i]==num]