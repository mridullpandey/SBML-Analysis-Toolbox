from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([5]) 
    # Dermis_to_Epidermis
    rxn[0] = p[2] * y[1] * p[6] / (p[6] + y[2]) * y[3] / (p[5] + y[3])
    # Dermal_Clearance
    rxn[1] = p[1] * y[1]
    # Epidermis_to_Dermis
    rxn[2] = p[3] * y[0] * p[6] / (p[6] + y[2]) * y[3] / (p[5] + y[3])
    # Epidermal_Clearance
    rxn[3] = p[1]_y[0]
    # Production_Signal
    rxn[4] = p[0]

    S = numpy.array([[ 1.,  0., -1., -1.,  0.],
       [-1., -1.,  1.,  0.,  1.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0., -1.],
       [ 0.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(5,1) 
    # Dermis_to_Epidermis
    rxn[0] = p[2] * y[1] * p[6] / (p[6] + y[2]) * y[3] / (p[5] + y[3])
    # Dermal_Clearance
    rxn[1] = p[1] * y[1]
    # Epidermis_to_Dermis
    rxn[2] = p[3] * y[0] * p[6] / (p[6] + y[2]) * y[3] / (p[5] + y[3])
    # Epidermal_Clearance
    rxn[3] = p[1]_y[0]
    # Production_Signal
    rxn[4] = p[0]
    return rxn 
