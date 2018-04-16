from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([2]) 
    # reaction1
    rxn[0] = p[0] * y[0] * y[1]
    # reaction2
    rxn[1] = p[1] * y[2]

    S = numpy.array([[-1.,  1.],
       [-1.,  1.],
       [ 1., -1.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(2,1) 
    # reaction1
    rxn[0] = p[0] * y[0] * y[1]
    # reaction2
    rxn[1] = p[1] * y[2]
    return rxn 
