import numpy as np

def sample( xmin, xmax, nsample ):
    """ LHS from uniform distribution.
    s = sample(xmin, xmax, nsample)

    Input:
      xmin    : min of data [1,nvar]
      xmax    : max of data [1,nvar]
      nsample : number of samples to pull

    Output:
      s       : Latin-Hypercube random sample [nsample,nvar]

    Budiman (2003)
    Adapted from MATLAB implementation
    """
    nvar = len( xmin )
    ran  = np.random.uniform( 0, 1, [nsample, nvar] )
    s    = np.zeros( [nsample, nvar] )
    for x_idx in range( nvar ):
        idx = np.random.permutation( nsample )
        P   = ( np.transpose(idx) - ran[:,x_idx] )/nsample
        s[:,x_idx] = xmin[x_idx] + P * ( xmax[x_idx] - xmin[x_idx] )

    return s
