import numpy as np

def read_postaXecombine(combinefile):
    """
    This function reads combine.dat from post-aXe processing. combine.dat is a text file with the following structure: first line = '# LAMBDA,FLAM,FLAM_ORIG,FERROR' and the following lines are csv entries.
    """
    filepath = combinefile
    f = open(filepath,'r')
    keys = []
    tmp = np.array([])
    for i,ii in enumerate(f.readlines()):
        if i==0:
            keys = np.array(ii.split(' ')[1].split(','))
        else:
            tmp = np.concatenate((tmp,np.array(ii.split(','))))
    nrow = int(len(tmp)/len(keys))
    ncol = len(keys)
    tmp = np.reshape(tmp,(nrow,ncol))
    out = {}
    for i,ii in enumerate(keys):
        out[ii] = tmp[:,i].astype(float)
    return out
