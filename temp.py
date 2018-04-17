from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([9]) 
    # Kq_Differentiation
    rxn[0] = p[0] * y[0]
    # Kq_Activation
    rxn[1] = p[1] * y[0]
    # Ka_Deactivation
    rxn[2] = p[2] * y[2]
    # Ks_Deactivation
    rxn[3] = p[3] * y[3]
    # Ka_Differentiation
    rxn[4] = p[4] * y[2]
    # Ks_Clearance
    rxn[5] = p[5] * y[3]
    # Kd_Clearance
    rxn[6] = p[6] * y[1]
    # Kq_Proliferation
    rxn[7] = p[7] * y[0]
    # Ka_Proliferation
    rxn[8] = p[8] * y[2]

    S = numpy.array([[-1., -1.,  1.,  0.,  0.,  0.,  0.,  1.,  0.],
       [ 1.,  0.,  0.,  1.,  0.,  0., -1.,  0.,  0.],
       [ 0.,  1., -1.,  0., -1.,  0.,  0.,  0.,  1.],
       [ 0.,  0.,  0., -1.,  1., -1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(9,1) 
    # Kq_Differentiation
    rxn[0] = p[0] * y[0]
    # Kq_Activation
    rxn[1] = p[1] * y[0]
    # Ka_Deactivation
    rxn[2] = p[2] * y[2]
    # Ks_Deactivation
    rxn[3] = p[3] * y[3]
    # Ka_Differentiation
    rxn[4] = p[4] * y[2]
    # Ks_Clearance
    rxn[5] = p[5] * y[3]
    # Kd_Clearance
    rxn[6] = p[6] * y[1]
    # Kq_Proliferation
    rxn[7] = p[7] * y[0]
    # Ka_Proliferation
    rxn[8] = p[8] * y[2]
    return rxn 
