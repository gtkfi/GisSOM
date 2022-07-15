# -*- coding: utf-8 -*-
"""
Created on Tue May 11 12:05:05 2021

@author: shautala
"""


"""
inputs:
1)som (som dictionary saved to file.)
2)Model.KMeans_min 
3)Model.KMeans_max 
4)Model.KMeans_initializations
5)Model.OutputFolder
"""

from nextsomcore import NxtSomCore
import sys

output_folder=sys.argv[1]
input_file=sys.argv[2]
nxtsomcore = NxtSomCore()
nxtsomcore.write_geotiff_out(output_folder, input_file)

