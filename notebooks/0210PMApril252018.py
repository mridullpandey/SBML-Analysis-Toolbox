from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([5]) 
    # Clearance_C
    rxn[0] = p[0] * y[2] / (y[2] + p[5])
    # Clearance_Kd
    rxn[1] = p[1] * y[2]
    # Differentiation_Kq
    rxn[2] = p[2] * y[3]
    # Production_C
    rxn[3] = p[3] * y[2] / (y[2] + p[6])
    # Proliferation_Kq
    rxn[4] = p[4] * y[4]

    S = numpy.array([[ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 1., -1.,  0.,  0.,  0.],
       [ 0.,  1., -1.,  0.,  0.],
       [ 0.,  0.,  0.,  1., -1.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(5,1) 
    # Clearance_C
    rxn[0] = p[0] * y[2] / (y[2] + p[5])
    # Clearance_Kd
    rxn[1] = p[1] * y[2]
    # Differentiation_Kq
    rxn[2] = p[2] * y[3]
    # Production_C
    rxn[3] = p[3] * y[2] / (y[2] + p[6])
    # Proliferation_Kq
    rxn[4] = p[4] * y[4]
    return rxn 
