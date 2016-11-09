import matplotlib.pyplot as plt
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


from sklearn.cluster import KMeans
X = np.array([[1,2], [1,4], [1,0], [4,2], [4,4], [4,0]])
subset =df[["Bare Plural Noun Percentage","Quantifier Percentage"]]
Y = [tuple(x) for x in subset.values]
#print Y
kmeans = KMeans(n_clusters=4, random_state=0).fit(Y)
df["clusternum"] = kmeans.labels_

#print df["clusternum"]

plt.figure(3)
use_colors = {0:"red", 1:"green", 2:"blue", 3:"grey",}
plt.scatter(df["Bare Plural Noun Percentage"], df["Quantifier Percentage"], c=[use_colors[x] for x in df["clusternum"]])

plt.xlabel('bare Plural')
plt.ylabel('quantifier')
plt.show()

newdf = df.sort(["clusternum"])
for i in range(len(newdf)):
	 if df["clusternum"][i] == 2:
	 	print df["Noun"][i]
	#print newdf["Noun"][i], newdf["clusternum"][i]
