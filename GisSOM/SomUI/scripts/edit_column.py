# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:08:04 2019

Script to edit data columns saved as numpy arrays saved in binary format. Actual data begins around index 5 or 6, the first entries
are used to mark whether data is winsorized, log transformed, is column excluded, winsormin, winsor max, etc...
@author: shautala
"""
import numpy as np
import sys

"""
Input:    
    1) Input file(column)
    2) Is winsorized ("true" or "false")
    3) WinsorMin (int/float)
    4) WinsorMax (int/float)
    5) Is log transformed ("true" or "false")
    6) Column type (0 or 1), included or excluded
    7) NoData value
"""

inputFile=sys.argv[1]
isWinsorized=sys.argv[2]
winsorMin=sys.argv[3]
winsorMax=sys.argv[4]
isLogTransformed=sys.argv[5]
ColumnType=sys.argv[6]

column=np.load(inputFile)

#if input contains optional noDataValue argument
if(len(sys.argv)>7): 
    noDataValue=str(float(sys.argv[7]))
    #Logarithm
    columnValues=column[6:]
    columnValues=columnValues[(columnValues!=noDataValue)]   
    if(isLogTransformed=='true' or isLogTransformed=='True'):    
        column[3]='true'
        min_value=(min(columnValues.astype(float))).astype(float)  # select min value for normalizing data:
        for x in range(6, len(column)): 
            if(column[x]!=noDataValue):
                column[x]=(float(column[x])-float(min_value))+1 #normalize data before log transform so that all values >=1
                column[x]=np.log(float(column[x]))   

    if(isWinsorized=='true' or isWinsorized=='True'):
        column[0]='true'
        column[2]=winsorMax
        column[1]=winsorMin
        for x in range (6, len(column)):
            if(column[x]!=noDataValue):
                if float(column[x])>float(winsorMax):
                    column[x]=float(winsorMax)
                elif float(column[x])<float(winsorMin):
                    column[x]=float(winsorMin)
     
    column[4]=ColumnType      
    outputFile=inputFile[:-4]
    np.save(outputFile+"_edited", column)

#input doesn't contain nodata value:
else:
    #Logarithm
    columnValues=column[6:]
    if(isLogTransformed=='true' or isLogTransformed=='True'): 
        min_value=(min(columnValues.astype(float))).astype(float)#take min value for normalizing log data
        column[3]='true'
        for x in range(6, len(column)):
            column[x]=(float(column[x])-float(min_value))+1 #Normalize data for log transform, so that all values >=1
            column[x]=np.log(float(column[x]))
    #Winsorize
    if(isWinsorized=='true' or isWinsorized=='True'):
        column[0]='true'
        column[2]=winsorMax
        column[1]=winsorMin
        for x in range (6, len(column)):
            if float(column[x])>float(winsorMax):
                column[x]=float(winsorMax)
            elif float(column[x])<float(winsorMin):
                column[x]=float(winsorMin)
                      
    column[4]=ColumnType       
    outputFile=inputFile[:-4]
    np.save(outputFile+"_edited", column) 
