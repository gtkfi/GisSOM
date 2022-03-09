# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:12:44 2019

Script for running nextsom_wrap multiple times with different input parameters and input data. 
Script is run from linux.
@author: shautala
"""
import sys
import os
#input files(data&params) as xml files
#some list is a list of xml files. passed as input params somehow.

python_path=sys.argv[1]
some_list=["C:/Users/shautala/Documents/SOMConfig/SOMConfig.xml",
           "C:/Users/shautala/Documents/SOMConfig/SOMConfig_GeoTiff.xml",
           "C:/Users/shautala/Documents/SOMConfig/SOMConfigNoKmeans.xml"]#sys.argv[2]#list of xml files. needs to be formatted, and original format and formatted format need to be decided upon.
for xmlfile in some_list:
    os.system(python_path+' C:/Users/shautala/source/repos/SomUI/SomUI/scripts/nextsom_wrap.py --xmlfile='+xmlfile)  
    #HARDCODED REPLACE REPLACE REPLACE. maybe make it so that this file and nextsom_wrap need to be in the same folder
    #would get rid of the hardcoding and simplify things overall
    #xml files should have different output paths to avoid overwriting
