# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:25:42 2019
Python script to save new clustering to som and geospace result files, and som codebook.
@author: shautala
"""


import pickle
from nextsomcore import NxtSomCore
import sys
import argparse

"""
inputs:
1)selectedClusterIndex
2)cluster_file
3)som -som dictionary saved 
4)Model.InputFile 
5)Model.Output_file_geospace
6)Model.Output_file_somspace 
7)Model.OutputFolder
"""

parser = argparse.ArgumentParser(description='Script for editing clustering results of self organizing maps')
parser.add_argument('--input_file',nargs='?', dest="input_file", help=' #input file path, only reads headers and notes from this')
parser.add_argument('--n_clusters', nargs='?', dest="n_clusters", help='#number of clusters selected')
parser.add_argument('--cluster_file', nargs='?', dest="cluster_file", help='#path to cluster dictionary file')
parser.add_argument('--som_dict',nargs='?', dest="som_dict", help=' #path to som dictionary file')
parser.add_argument('--outsomfile', nargs='?', dest="outsomfile", help='#path to som results text file, where new clustering is saved to')
parser.add_argument('--workingdir', nargs='?', dest="workingdir", help='#working directory')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#path to geo results text file, where new clustering is saved to. Optional (in case of non-spatial data)')
parser.add_argument('--normalized', type=str, default="False", dest='normalized',help='Whether the data has been normalized or not')
#parser.add_argument('--minN', type=str, default=0, dest='minN',help='Minimum value for normalization')
#parser.add_argument('--maxN', type=str, default=1, dest='maxN',help='Maximum value for normalization')
parser.add_argument('--label', type=str, default=None, dest='label', help='Whether data contains label column, true or false')
parser.add_argument('--scale_min_list',default=None, dest="scale_min_list", help="List of floats for scaling minimum values") 
parser.add_argument('--scale_max_list',default=None, dest="scale_max_list", help="List of floats for scaling maximum values") 
                    
args=parser.parse_args()

outgeofile=None
selected_number=args.n_clusters
cluster_file=args.cluster_file
som_file=args.som_dict
input_file=args.input_file
output_file_somspace=args.outsomfile
working_dir=args.workingdir

if(args.outgeofile is not None):
    outgeofile=args.outgeofile
nxtsomcore=NxtSomCore()
with open(working_dir+'/cluster.dictionary', 'rb') as cluster_dictionary_file:
    cluster_dictionary = pickle.load(cluster_dictionary_file)
selected_cluster=cluster_dictionary[int(selected_number)]
with open(working_dir+'/som.dictionary', 'rb') as som_dictionary_file:
    som = pickle.load(som_dictionary_file)

som['clusters'] = selected_cluster['cluster']
header = nxtsomcore.load_data(input_file)
if(outgeofile is not None):
    nxtsomcore.save_geospace_result(outgeofile, header, som, working_dir, input_file,args.normalized, args.label)
#nxtsomcore.save_somspace_result(output_file_somspace, header, som, working_dir,input_file)
nxtsomcore.save_somspace_result(output_file_somspace, header, som, working_dir, args.input_file, args.normalized)  
with open(working_dir+'/som.dictionary', 'wb') as som_dictionary_file:
    pickle.dump(som, som_dictionary_file) 
