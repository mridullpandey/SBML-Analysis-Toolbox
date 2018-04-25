from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([9]) 
    # Proliferation_Kq
    rxn[0] = p[0] * y[2] / (y[2] + p[6])
    # Differentiation_Kq
    rxn[1] = p[1] * y[2]
    # Clearance_Kd
    rxn[2] = p[2] * y[3]
    # Production_C
    rxn[3] = p[3] * y[2] / (y[2] + p[7])
    # Clearance_C
    rxn[4] = p[4] * y[5]
    # Wounding_Kq
    rxn[5] = p[5] * y[4]
    # Wounding_Kd
    rxn[6] = p[8] * y[2] * y[4] / (y[4] + p[11])
    # Wounding_C
    rxn[7] = p[9] * y[3] * y[4] / (y[4] + p[11])
    # Clearance_W
    rxn[8] = p[10] * y[5] * y[4] / (y[4] + p[12])

    S = numpy.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 1., -1.,  0.,  0.,  0.,  0., -1.,  0.,  0.],
       [ 0.,  1., -1.,  0.,  0.,  0.,  0., -1.,  0.],
       [ 0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1., -1.,  0.,  0.,  0., -1.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(9,1) 
    # Proliferation_Kq
    rxn[0] = p[0] * y[2] / (y[2] + p[6])
    # Differentiation_Kq
    rxn[1] = p[1] * y[2]
    # Clearance_Kd
    rxn[2] = p[2] * y[3]
    # Production_C
    rxn[3] = p[3] * y[2] / (y[2] + p[7])
    # Clearance_C
    rxn[4] = p[4] * y[5]
    # Wounding_Kq
    rxn[5] = p[5] * y[4]
    # Wounding_Kd
    rxn[6] = p[8] * y[2] * y[4] / (y[4] + p[11])
    # Wounding_C
    rxn[7] = p[9] * y[3] * y[4] / (y[4] + p[11])
    # Clearance_W
    rxn[8] = p[10] * y[5] * y[4] / (y[4] + p[12])
    return rxn 
