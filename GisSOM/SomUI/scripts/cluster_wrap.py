# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:22:33 2019
Python script to calculate new clustering to existing som. Calls nextsomcore clustering method.
@author: shautala
"""
"""
inputs:
1)som (som dictionary saved to file.=
2)Model.KMeans_min 
3)Model.KMeans_max 
4)Model.KMeans_initializations
5)Model.OutputFolder
"""

from nextsomcore import NxtSomCore
import sys
import pickle

som=sys.argv[1]
kmeans_min=sys.argv[2]
kmeans_max=sys.argv[3]
kmeans_init=sys.argv[4]
working_dir=sys.argv[5]
  
with open(working_dir+'/som.dictionary', 'rb') as som_dictionary_file:
    som = pickle.load(som_dictionary_file)
nxtsomcore = NxtSomCore()
nxtsomcore.clusters(som,int(kmeans_min),int(kmeans_max),int(kmeans_init),working_dir)  

