import numpy as np
import nextsomcore
from nextsomcore import NxtSomCore
nxtsomcore = NxtSomCore()

#outdated script for testing.

header = nxtsomcore.load_data('testdata_10000pts.lrn')
som = nxtsomcore.train(header['data'], 50, 50, 5, kerneltype=0, verbose=2)
nxtsomcore.cluster(som, 8)
print("n_rows:"+str(som['n_rows'])+" n_columns:"+str(som['n_columns']))
np.savetxt("codebook.txt",som['codebook'].reshape(som['n_rows'] * som['n_columns'] ,som['n_dim']), fmt='%f')
np.savetxt("bmu.txt", som['bmus'], fmt='%d')
np.savetxt("umatrix.txt", som['umatrix'], fmt='%f')
np.savetxt("clusters.txt", som['clusters'], fmt='%d')
nxtsomcore.save_geospace_result('geo_result.txt', header, som)
nxtsomcore.save_somspace_result('som_result.txt', header, som)

print("done!")

