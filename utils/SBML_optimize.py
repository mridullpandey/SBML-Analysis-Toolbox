from scipy.optimize import minimize
from pandas import read_excel
from generated import simulateModel
import numpy

def SBML_minimize( timeSeries_path, bnds, y0, pStart ):

    timeSeries_data = read_excel( timeSeries_path, header=None ).set_index(0).as_matrix()

    # Set conditions after wounding
    y0[0] = timeSeries_data[1,1]
    y0[1] = timeSeries_data[2,1]

    # Set parameter boundaries
    bnds = ( (0,10), (0,10), (0,10) )

    def error_minimization( pVarySet ):
    
        y = numpy.transpose( simulateModel( timeSeries_data[0,:], y0, pVarySet ) )
    
        return numpy.nansum( abs( y[0,:] - timeSeries_data[1,:] ) / y[0,:] )

    result = minimize( error_minimization, pStart,
                   options = {'disp' : True}, bounds = bnds,
                   method = 'TNC', tol = 1E-12 )
    pErr = result.fun
    pOpt = result.x

    return pErr, pOpt
