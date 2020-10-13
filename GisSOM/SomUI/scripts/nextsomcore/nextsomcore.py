# -*- coding: utf-8 -*-
"""
The module contains the NxtSomCore class that is used to train self-organizing
maps and write results to the disk. NxtSomCore depends on somoclu package written
by Peter Wittek to perform actual SOM calculations.

@author: Janne Kallunki
"""
import warnings
with warnings.catch_warnings():
    import numpy as np
    import sklearn.cluster
    import somoclu
    #from .lrnfile import load_lrn_file, read_coordidate_columns, read_data_columns
    from .loadfile import load_input_file, read_coordinate_columns, read_data_columns
    import heapq
    import pickle
    from sklearn.metrics import davies_bouldin_score

class NxtSomCore(object):
    """Class for training self-organizing map and saving results.
    """
    def __init__(self):
        """Constructor for the class
        """
        self.som = {}

    def load_data(self, input_file):
        """Load and return the input data as a dict containing numpy array and metadata
        :param input_file: The name of the file to be loaded.
        :type filename: str.
        :rtype: dict
        """
        return load_input_file(input_file)

    def train(self, data, som_x, som_y , epochs=10, **kwargs):
        """Train the map and return results as a dict.
        :param data: Training data used in SOM.
        :type data: 2D numpy.array of float32.
        :param som_x: X-size of the map.
        :type som_x: int.
        :param som_y: Y-size of the map.
        :type som_y: int.
        :param epochs: Number of rounds the training is performed.
        :type epochs: int.
        :rtype: dict
        """
        self.som = somoclu.Somoclu(som_x, som_y, 
            kerneltype = kwargs.pop("kerneltype", 0), 
  			verbose = kwargs.pop("verbose", 2),
  			neighborhood = kwargs.pop("neighborhood", "gaussian"), 
  			std_coeff = kwargs.pop("std_coeff", 0.5),  
            maptype= kwargs.pop("maptype", "toroid"), 
            initialcodebook=kwargs.pop("initialcodebook", None), 
            initialization=kwargs.pop("initialization", 'random'), 
            gridtype=kwargs.pop("gridtype","rectangular" ) )
        self.som.train(data, epochs,
			radius0 = kwargs.pop("radius0", 0),
			radiusN = kwargs.pop("radiusN", 1),
			radiuscooling = kwargs.pop("radiuscooling", "linear"),
			scale0 = kwargs.pop("scale0", 0.1),
			scaleN = kwargs.pop("scaleN", 0.01),
			scalecooling = kwargs.pop("scalecooling", "linear"))
        return {
            'codebook': self.som.codebook.copy(),
            'bmus': self.som.bmus.copy(),
            'umatrix' : self.som.umatrix.copy(),
            'n_columns' : self.som._n_columns,
            'n_rows': self.som._n_rows,
            'n_dim': self.som.n_dim,
            'clusters': None}

    def cluster(self, som, cluster_count):
        """Cluster the codebook and return clustering results as a 2d numpy array. Code taken from
         somoclu's train.py and changed to operate on input parameters only
        :param som: SOM-related data obtained from training(codebook, dimensions, etc..)
        :type som: dictionary
        :param cluster_count: Number of clusters used in clustering
        :type cluster_count: int.
        :rtype: numpy.array
        """
        algorithm = sklearn.cluster.KMeans(n_clusters=cluster_count, init='random')
        original_shape = som['codebook'].shape
        som['codebook'].shape = (som['n_columns'] * som['n_rows'], som['n_dim'])
        linear_clusters = algorithm.fit_predict(som['codebook'])
        som['codebook'].shape = original_shape
        clusters = np.zeros((som['n_rows'], som['n_columns']), dtype=int)
        for i, c in enumerate(linear_clusters):
            clusters[i // som['n_columns'], i % som['n_columns']] = c
        som['clusters'] = clusters
        return clusters

    def clusters(self, som, cluster_min, cluster_max, cluster_init,working_dir): 
        """Cluster the codebook and return clustering results as a 2d numpy array. Code taken from
         somoclu's train.py and changed to operate on input parameters only.
         Calculates clusters multiple times and selects the best result by Davies-Bouldin score. 
         Returns the best clustering, and writes the 3 best clustering results to a binary file.
        :param som: SOM-related data obtained from training(codebook, dimensions, etc..)
        :type som: dictionary
        :param cluster_min: Minimum number of clusters used in clustering
        :type cluster_min: int.
        :param cluster_max: Maximum number of clusters used in clustering
        :type cluster_max: int.
        :param cluster_init: Minimum number of clusters used in clustering
        :type cluster_min: int.
        :rtype: numpy.array                       
        
        """               
        min=2 
        algorithm = sklearn.cluster.KMeans()
        original_shape = som['codebook'].shape       
        if (cluster_init<1):
            cluster_init=1
        if(cluster_min<2):
            cluster_min=2   
        if(cluster_max<3):
            cluster_max=3
        cluster_list=[]    
        min_clusters=[]
        total=(cluster_max-cluster_min+1)*cluster_init 
        value=0
        if(total>20):
            interval=int(total/10)
        else:
            interval=1
        
        
        print("Clustering progress:")
        for a in range(cluster_min, cluster_max+1):                                   
            min=2
            min_dict={}
            for j in range(0, cluster_init):
                algorithm = sklearn.cluster.KMeans(n_clusters=a,init='random')
                som['codebook'].shape = (som['n_columns'] * som['n_rows'], som['n_dim'])  
                linear_clusters=algorithm.fit_predict(som['codebook'])       
                current=davies_bouldin_score(som['codebook'], linear_clusters)
                clusters = np.zeros((som['n_rows'], som['n_columns']), dtype=int)
                for i, c in enumerate(linear_clusters):
                    clusters[i // som['n_columns'], i % som['n_columns']] = c
                som['codebook'].shape = original_shape
                dict={'db_score': current, 'n_clusters' : a, 'cluster' : clusters}
                
                value=((a-cluster_min)*cluster_init + j)
                if (value%interval==0):
                    print(("%.2f" % ((value/total)*100))+"%")
                if(min>current):
                    min=current
                    min_clusters=clusters
                    min_dict=dict
            cluster_list.append(min_dict)
        smallest_3=[]
        smallest_3=heapq.nsmallest(3, cluster_list,key=lambda k: k['db_score'])    
        with open(working_dir+'/cluster.dictionary', 'wb') as cluster_dictionary_file:
            pickle.dump(cluster_list, cluster_dictionary_file)
        print("100% Clustering completed.")
        return smallest_3[0]["cluster"]     
                

    def save_geospace_result(self, output_file, header, som, output_folder):
        """Write SOM results with header line and input columns to disk in geospace

        Output file columns:
        X, Y, Z - Coordinates in the input file (if present in input file)
        data1, data2, dataN, ... - Original columns in input file
        som_x, som_y - X Y indices in the map
        cluster - Cluster group number
        b_data1, bdata2, bdataN, ... - SOM results
        q_error= Q-error, difference between som results and original columns

        :param output_file: Filename to be used for saving the result.
        :type output_file: str.
        :param header: Dictionary holding header data ((load_data(...)).
        :type header: dictionary.
        :param som: Dictionary holding SOM results (train(...)).
        :type som: dictionary.
        """
        coord_cols = read_coordinate_columns(header)
        data_cols = read_data_columns(header)
        som_cols = self._extract_som_cols_geospace(som, data_cols['colnames'])   
        q_cols = som_cols['data'][:,3:] - data_cols['data'] #calculate q error
        q_error=np.linalg.norm(q_cols,axis=1)               #calculate q error     
        mean_q_error=np.mean(q_error)                       #calculate mean q error
        f=open(output_folder+"/RunStats.txt", "a+")         #write mean q error to runstats file
        f.write("Quantization error: "+str(mean_q_error))   #write mean q error to runstats file     
        f.close                                             #write mean q error to runstats file
        header_line = '{} {} {} {}'.format(str(coord_cols['colnames']),
										str(som_cols['colnames']),
										str(data_cols['colnames']),'q_error').replace('[','').replace(']','').replace(',','').replace('\'','')#.translate(None, "[]',") replaced by a lower level solution that works in both 2.x and 3.x python
        combined_cols = np.c_[coord_cols['data'], som_cols['data'], data_cols['data'], q_error]     
        fmt_combined = '{} {} {} {}'.format(coord_cols['fmt'], som_cols['fmt'], data_cols['fmt'], '%.5f') 
        np.savetxt(output_file, combined_cols,fmt=fmt_combined, header=header_line, comments='')

    def save_somspace_result(self, output_file, header, som):
        """Write SOM results with header line and input columns to disk in somspace.

        Output file columns:
        som_x, som_y - X Y indices in the map
        b_data1, bdata2, bdataN, ... - SOM results
        umatrix - U-matrix
        cluster - Cluster group number

        :param output_file: Filename to be used for saving the result.
        :type output_file: str.
        :param header: Dictionary holding header data ((load_data(...)).
        :type header: dictionary.
        :param som: Dictionary holding SOM results (train(...)).
        :type som: dictionary.
        """
        col_names = read_data_columns(header)['colnames']
        som_cols = self._extract_som_cols_somspace(som, col_names)
        header_line = '{}'.format(str(som_cols['colnames'])).replace('[','').replace(']','').replace(',','').replace('\'','')#.translate(None, "[]',") replaced by a lower level solution that works in both 2.x and 3.x python
        np.savetxt(output_file, som_cols['data'], fmt=som_cols['fmt'], header=header_line, comments='')

    def _extract_som_cols_geospace(self, som, col_names):
        """Internal function to combine geospace output file columns together
        """
        x_col = som['bmus'][:, 1]#alunperin nää oli 0
        y_col = som['bmus'][:, 0]# ja 1     
        data = som['codebook'][x_col, y_col]
        if (som['clusters'] is not None):            
            clusters = som['clusters'][x_col, y_col]
            combined_data = np.c_[y_col, x_col, clusters, data]
            combined_col_list = ['som_x', 'som_y', 'cluster'] + ['b_%s' % x for x in col_names]
            combined_fmt = ('%d %d %d ' + '%f ' * len(col_names)).rstrip()
        else:
            clusters=np.zeros(shape=(len(x_col)))
            combined_data = np.c_[y_col, x_col, clusters, data]
            combined_col_list = ['som_x', 'som_y', 'cluster'] + ['b_%s' % x for x in col_names]
            combined_fmt = ('%d %d %d ' + '%f ' * len(col_names)).rstrip()
        return {'data': combined_data, 'colnames':combined_col_list, 'fmt': combined_fmt}

    def _extract_som_cols_somspace(self, som, col_names):
        """Internal function to combine somspace output file columns together
        """
        rows = som['codebook'].shape[0]
        cols = som['codebook'].shape[1]
        som_x_y_cols = np.array(np.meshgrid(np.arange(cols), np.arange(rows))).T.reshape(-1, 2)
        row = som_x_y_cols[:, 0]
        col = som_x_y_cols[:, 1]
        data = som['codebook'][col, row]#col=x, row=y
        umatrix = som['umatrix'][col, row]
        if (som['clusters'] is not None):
            clusters = som['clusters'][col, row]
            combined_data = np.c_[som_x_y_cols, data, umatrix, clusters]
            combined_col_list = ['som_x', 'som_y'] + ['b_%s' % x for x in col_names] + ['umatrix', 'cluster']
            combined_fmt = ('%d %d ' + '%f ' * len(col_names)) +'%f %d'
        else:           
            clusters=np.zeros(shape=(len(umatrix)))
            combined_data = np.c_[som_x_y_cols, data, umatrix, clusters]
            combined_col_list = ['som_x', 'som_y'] + ['b_%s' % x for x in col_names] + ['umatrix', 'cluster']
            combined_fmt = ('%d %d ' + '%f ' * len(col_names)) +'%f %d'
        return {'data': combined_data, 'colnames':combined_col_list, 'fmt': combined_fmt}






    def write_geotiff_out(self, output_folder, input_file): 
        from osgeo import gdal
        import pandas as pd
        dir=output_folder
        inDs=gdal.Open(input_file)
        som_data= np.genfromtxt(dir+"/result_som.txt",skip_header=(1), delimiter=' ')
        geo_data=np.genfromtxt(dir+"/result_geo.txt", skip_header=(1), delimiter=' ')
        for a in range(0, len(som_data[0])-3): 
            x=geo_data[:,0]
            y=geo_data[:,1]
            z=geo_data[:,(len(som_data[0])-3+a)]
            df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
            df.columns = ['X_value','Y_value','Z_value']
            df['Z_value'] = pd.to_numeric(df['Z_value'])
            pivotted= df.pivot('Y_value','X_value','Z_value')
        
            cols=pivotted.shape[1] 
            rows=pivotted.shape[0]
    
            driver = gdal.GetDriverByName('GTiff')
            outDs = driver.Create(dir+"/GeoTIFF/out_"+str(a)+".tif", cols, rows, 1, gdal.GDT_Float32)
            if outDs is None:
                print ("Could not create tif file")
                sys.exit(1) 
    
            outBand = outDs.GetRasterBand(1)
            outData = np.zeros((rows,cols), np.float32)
            pivotted_np=pivotted.to_numpy()
            pivotted_np=np.flip(pivotted_np,0)

            for i in range(0, rows):
                for j in range(0, cols):    
                    outData[i,j] = pivotted_np[i,j]
    
            #write data to array
            outBand.WriteArray(outData, 0, 0)
    
            # flush data to disk, set NoData value
            outBand.FlushCache()
            outBand.SetNoDataValue(-99)

            # georeference and projection
            outDs.SetGeoTransform(inDs.GetGeoTransform())
            outDs.SetProjection(inDs.GetProjection())
            outDs.FlushCache()
    
