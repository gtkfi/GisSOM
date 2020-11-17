# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 08:38:34 2020

@author: shautala
"""

import matplotlib.pyplot as plt
import sys
import pickle    

working_dir=sys.argv[1]
cluster_dict=sys.argv[2]
with open(cluster_dict, 'rb') as cluster_dictionary_file:
    cluster_dictionary = pickle.load(cluster_dictionary_file)
with open(working_dir+'/som.dictionary', 'rb') as som_dictionary_file:
    som_dictionary = pickle.load(som_dictionary_file)  
    
clusters=[]
db_scores=[]
for i in range (len(cluster_dictionary)): 
    clusters.append(cluster_dictionary[i]['n_clusters'])
    db_scores.append(cluster_dictionary[i]['db_score'])
plt.plot(clusters, db_scores)
fig, ax = plt.subplots()
ax.set_xticks(clusters)
ax.set_xticklabels(clusters)

ax.xaxis.grid()
ax.yaxis.grid(linestyle='--', linewidth=1)
ax.set(xlabel='Number of clusters',ylabel='Davies-Bouldin index')
plt.plot(clusters, db_scores)
ax.figure.savefig(working_dir+'/cluster_plot.png')


