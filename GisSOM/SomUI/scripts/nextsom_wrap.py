# -*- coding: utf-8 -*-
"""
Script for performing SOM training and saving results.


First 7 parameters (script name, input data, output geo file, output som file, som x, som y, epochs) are required.
Parameters are passed in the following format: '--name=value'. The order of the parameters doesn't matter.
If input contains --xmlfile parameter, other command line parameters will be ignored.
If Initial codebook parameter is given, Initialization parameter is ignored, and the given som x and som y dimensions must match those of the existing codebook.
@author: Janne Kallunki, Sakari Hautala
"""
#import warnings
#with warnings.catch_warnings():
import argparse
import xml.etree.ElementTree as ET
from nextsomcore import NxtSomCore
import pickle
#import time


"""
Parse command line arguments
"""
def parse_command_line():
    parser = argparse.ArgumentParser(description='Script for generating self organizing maps')
    parser.add_argument('--input_file',nargs='?', help='Input file(*.lrn)')
    parser.add_argument('--output_file_somspace',nargs='?', help='Text file that will contain calculated values: som_x som_y b_data1 b_data2 b_dataN umatrix cluster in geospace.')
    parser.add_argument('--som_x',nargs='?', type=int, help='X dimension of generated SOM')
    parser.add_argument('--som_y',nargs='?', type=int, help='Y dimension of generated SOM')
    parser.add_argument('--epochs',nargs='?', type=int, help='Number of epochs to run')
    #^base parameters required for som calculation. Additional optional parameters below:
    parser.add_argument('--output_file_geospace', default=None, dest="outgeofile", help='Text file that will contain calculated values: {X Y Z} data1 data2 dataN som_x som_y cluster b_data1 b_data2 b_dataN in geospace.')   # but can this be included, cause its not given by user? either check for the existence of this file, or...hmmm...
    parser.add_argument('--kmeans_min',type=int, default=2, help='Minimum number of k-mean clusters')
    parser.add_argument('--kmeans_max',type=int, default=25, help='Maximum number of k-mean clusters')
    parser.add_argument('--kmeans_init',type=int, default=5, help='Number of initializations')
    parser.add_argument('--kmeans',type=str,default="True", dest='kmeans',help='Run k-means clustering')
    parser.add_argument('--neighborhood',type=str,default="gaussian",dest='neighborhood',help='Shape of the neighborhood function. gaussian or bubble')
    parser.add_argument('--std_coeff',type=float, default=0.5, dest='std_coeff', help='Coefficient in the Gaussian neighborhood function')
    parser.add_argument('--maptype', type=str, default="toroid", dest='maptype', help='Type of SOM (sheet, toroid)')
    parser.add_argument('--initialcodebook', type=str, default=None, dest='initialcodebook', help='File path of initial codebook, 2D numpy.array of float32.') 
    parser.add_argument('--radiuscooling', type=str, default='linear', dest='radiuscooling', help='Function that defines the decrease in the neighborhood size as the training proceeds (linear, exponential)') 
    parser.add_argument('--radius0', type=float, default=0, dest='radius0', help='Initial size of the neighborhood')
    parser.add_argument('--radiusN', type=float, default=1, dest='radiusN', help='Final size of the neighborhood')
    parser.add_argument('--scalecooling', type=str, default='linear', dest='scalecooling', help='Function that defines the decrease in the learning scale as the training proceeds (linear, exponential)')
    parser.add_argument('--scale0', type=float, default=0.1, dest='scale0', help='Initial learning rate')
    parser.add_argument('--scaleN', type=float, default=0.01, dest='scaleN', help='Final learning rate')
    parser.add_argument('--initialization', type=str, default='random', dest='initialization', help='Type of SOM initialization (random, pca)')
    parser.add_argument('--gridtype', type=str, default='rectangular', dest='gridtype', help='Type of SOM grid (hexagonal, rectangular)')
    parser.add_argument('--xmlfile', type=str, default='none',dest='xmlfile',help='SOM inputs as an xml file')
    parser.add_argument('--output_folder', type=str, default="",dest='output_folder',help='Folder to save som dictionary and cluster dictionary')
    parser.add_argument('--geotiff_input', type=str, default=None, dest='geotiff_input')
    parser.add_argument('--normalized', type=str, default="False", dest='normalized',help='Whether the data has been normalized or not')
    parser.add_argument('--minN', type=str, default=0, dest='minN',help='Minimum value for normalization')
    parser.add_argument('--maxN', type=str, default=1, dest='maxN',help='Maximum value for normalization')
    parser.add_argument('--label', type=str, default=None, dest='label', help='Whether data contains label column, true or false')
    return parser.parse_args()

"""Run SOM training using command line input, and save the results. Uses NxtSomCore package to do the actual work.
:param args: Command line arguments passed to script
:type args: args
"""
def run_command_line(args):
    nxtsomcore = NxtSomCore()
    if args.initialcodebook is not None: #if initial codebook was provided (in the form of som.dictionary), open the file, and load som codebook from it.
        with open(args.initialcodebook, 'rb') as som_dictionary_file:
            som_dictionary = pickle.load(som_dictionary_file)
            args.initialcodebook=som_dictionary['codebook']
            args.initialization=None           
    header = nxtsomcore.load_data(args.input_file) 
    som = nxtsomcore.train(
        header['data'],
        args.som_x,
        args.som_y,
        args.epochs,
        kerneltype=0,
        verbose=1,
        neighborhood=args.neighborhood,
        std_coeff=args.std_coeff,
        maptype=args.maptype,
        radiuscooling=args.radiuscooling,
        scalecooling=args.scalecooling,
        initialization=args.initialization,
        initialcodebook=args.initialcodebook,
        gridtype=args.gridtype
        )          
    if(args.output_folder==""):
        output_folder="C:/Temp/NextSom"
    else:
        output_folder=args.output_folder
    print(args.output_folder)
    if(args.kmeans.lower()=="true"):
        som['clusters']=nxtsomcore.clusters(som,args.kmeans_min,args.kmeans_max,args.kmeans_init,output_folder)     
    
    if args.outgeofile is not None:
        nxtsomcore.save_geospace_result(args.outgeofile, header, som, output_folder, args.input_file, args.normalized, args.label) 
    
    nxtsomcore.save_somspace_result(args.output_file_somspace, header, som, output_folder, args.input_file, args.normalized)  
    if(args.geotiff_input is not None):
        inputFileArray=args.geotiff_input.split(",")    
        nxtsomcore.write_geotiff_out(args.output_folder, inputFileArray[0])
    with open(output_folder+'/som.dictionary', 'wb') as som_dictionary_file:
        pickle.dump(som, som_dictionary_file) #save som object to file.




def read_xml_input(args):
    tree = ET.parse(args.xmlfile)
    root = tree.getroot()   
    som_files=root.find('som_files')
    som_params=root.find('som_parameters')
    kmeans= som_params.find('kMeans')
    input_node=som_files.find('input')
    initial_codebook=None
    if(root.find('som_files') is None):
        raise Exception("XML file does not contain proper definition for input")
    if(som_files.find('input') is not None):
        args.input_file=som_files.find('input').text
    else:
        raise Exception("Input file is missing")
    if(som_files.find('output_somspace') is not None):
        args.output_file_somspace=som_files.find('output_somspace').text
    else:
        args.output_file_somspace="C:/Temp/Nextsom/result_som.txt"   #Is this still relevant? Ask BEAK.
    if(som_files.find('output_geospace') is not None):               
        args.outgeofile=som_files.find('output_geospace').text  
    else:
        args.outgeofile=None      
    if(som_files.find('output_folder') is not None):
        args.output_folder=som_files.find('output_folder').text
    input_list_text=[]
    if(len(input_node.findall('geotiff'))>1):
        input_list= input_node.findall('geotiff')
        for item in input_list:
            input_list_text.append(item.text)
        args.input_file= ",".join(input_list_text)
        

    if(som_params.find('som_x') is not None):
        args.som_x=int(som_params.find('som_x').text)
    else:
        args.som_x=10

    if(som_params.find('som_y') is not None):
        args.som_y=int(som_params.find('som_y').text)
    else:
        args.som_y=10

    if(som_params.find('nEpoch') is not None):
        args.epochs=int(som_params.find('nEpoch').text)
    else:
        args.epochs=10

    if(som_params.find('codebook') is not None):
        initial_codebook=som_params.find('codebook').text       


    if(som_params.find('initialization') is not None):
        args.initialization=som_params.find('initialization').text        
    else:
        args.initialization='random'

    if(som_params.find('mapType') is not None):     
        args.maptype=som_params.find('mapType').text
    else:
        args.maptype='toroid'

    if(som_params.find('gridType') is not None):        
        args.gridtype=som_params.find('gridType').text
    else:
        args.gridtype='rectangular'

    if(som_params.find('neighborhood') is not None):        
        args.neighborhood=som_params.find('neighborhood').text
    else:
        args.neighborhood='gaussian'

    if(som_params.find('std_coeff') is not None):        
        args.std_coeff=som_params.find('std_coeff').text
    else:
        args.std_coeff=0.5

    if(som_params.find('radius0') is not None):
        args.radius0=som_params.find('radius0').text       
    else:
        args.radius0=0

    if(som_params.find('radiusN') is not None):    
        args.radiusN=som_params.find('radiusN').text
    else:
        args.radiusN=1

    if(som_params.find('radiuscooling') is not None):		
        args.radiuscooling= som_params.find('radiuscooling').text
    else:
        args.radiuscooling='linear'

    if(som_params.find('scalecooling') is not None):
        args.scalecooling=som_params.find('scalecooling').text
    else:
        args.scalecooling='linear'
   
    if(som_params.find('scale0') is not None):
        args.scale0=som_params.find('scale0').text
    else:
        args.scale0=0.1

    if(som_params.find('scaleN') is not None):
        args.scaleN=som_params.find('scaleN').text
    else:
        args.scaleN=0.01      

    if(som_params.find('kMeans') is not None):   
        if(kmeans.find('number') is not None):
            args.kmeans_init=int(kmeans.find('number').text)
        else:
            args.kmeans_init=5
        if(kmeans.find('number_min') is not None):
            args.kmeans_min=int(kmeans.find('number_min').text)
        else:
            args.kmeans_min=2
        if(kmeans.find('number') is not None):
            args.kmeans_max=int(kmeans.find('number_max').text)
        else:
            args.kmeans_max=25

        if(initial_codebook is not None and initial_codebook != ""):
            with open(initial_codebook, 'rb') as som_dictionary_file:
                som_dictionary = pickle.load(som_dictionary_file)
                args.initial_codebook=som_dictionary['codebook']
                args.initialization=None
        else:
            args.initial_codebook=None

    return(args)


"""
main
    
"""
def main():
    
    args = parse_command_line()

    if(args.xmlfile!='none'):#is there a reason for this being a string?
        args=read_xml_input(args)

    
    run_command_line(args)
        
    
if __name__ == "__main__":
    main()
