from __future__ import division 
import numpy, sympy 

def ode_fun( y, t, p ): 

    rxn = numpy.zeros([47]) 
    # Activation_I
    rxn[0] = p[11] * y[4] * y[10] / (y[10] + p[54])
    # Activation_K
    rxn[1] = p[3] * y[0] * y[12] / (y[12] + p[50])
    # Deactivation_I
    rxn[2] = p[10] * y[5]
    # Deactivation_K
    rxn[3] = p[2] * y[2] * y[6] / (y[6] + p[47]) * p[48] / (y[7] + p[48]) * p[49] / (y[8] + p[49])
    # Deactivation_Ks
    rxn[4] = p[6] * y[3]
    # Differentiation
    rxn[5] = p[1] * y[0]
    # Separation
    rxn[6] = p[4] * y[2]
    # Proliferation_Kq
    rxn[7] = p[0] * y[0] / (y[0] + p[45]) * p[46] / (y[6] + p[46])
    # Proliferation_Ka
    rxn[8] = p[0] * y[2] / (y[2] + p[45]) * p[46] / (y[6] + p[46]) * y[8] / (y[8] + p[51]) * y[12] / (y[12] + p[50])
    # Clearance_Kd
    rxn[9] = p[5] * y[1]
    # Clearance_Ks
    rxn[10] = p[7] * y[3]
    # Influx_Iq
    rxn[11] = p[8] + p[9] * y[12] / (y[12] + p[53])
    # Clearance_Iq
    rxn[12] = p[12] * y[4]
    # Mass_Transfer_TGFb
    rxn[13] = p[14] * (y[13] - y[6]) * p[55] / (y[19] + p[55]) * y[20] / (y[20] + p[56])
    # Clearance_TGFb
    rxn[14] = p[13] * y[6]
    # Mass_Transfer_IFNg
    rxn[15] = p[16] * (y[15] - y[7]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_IFNg
    rxn[16] = p[15] * y[7]
    # Mass_Transfer_TNFa
    rxn[17] = p[19] * (y[16] - y[8]) * p[55] / (y[19] + p[55]) * y[20] / (y[20] + p[56])
    # Clearance_TNFa
    rxn[18] = p[17] * y[8]
    # Mass_Transfer_IF
    rxn[19] = p[24] * (y[17] - y[10]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_IF
    rxn[20] = p[23] * y[10]
    # Mass_Transfer_Sig
    rxn[21] = p[27] * (y[18] - y[11]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_Sig
    rxn[22] = p[26] * y[11]
    # Clearance_TGFa
    rxn[23] = p[21] * y[9]
    # Clearance_IL1
    rxn[24] = p[30] * y[12]
    # Production_TNFa
    rxn[25] = p[18] * y[3] / (y[3] + p[57])
    # Production_IF
    rxn[26] = p[22] * y[2] / (y[2] + p[59])
    # Production_Sig
    rxn[27] = p[25] * y[2] / (y[2] + p[60])
    # Production_TGFa
    rxn[28] = p[20] * y[2] / (y[2] + p[58])
    # Production_IL1
    rxn[29] = p[29] * y[2] / (y[2] + p[61])
    # Release_IL1
    rxn[30] = p[28] * p[68] * y[1] * y[21] / (y[21] + p[51])
    # Release_TGFb
    rxn[31] = p[32] * y[14] + p[33] * y[14] * y[18] / (y[18] + p[62])
    # Clearance_TGFbd
    rxn[32] = p[31] * y[13]
    # Production_IFNgd
    rxn[33] = p[36] * y[5] / (y[5] + p[64])
    # Clearance_IFNgd
    rxn[34] = p[35] * y[15]
    # Production_TNFad
    rxn[35] = p[36] * y[5] / (y[5] + p[64])
    # Clearance_TNFad
    rxn[36] = p[37] * y[16]
    # Clearance_IFd
    rxn[37] = p[38] * y[17]
    # Clearance_Sigd
    rxn[38] = p[39] * y[18]
    # Production_C
    rxn[39] = p[40] * y[0] / (y[0] + p[65])
    # Clearance_C
    rxn[40] = p[41] * y[19]
    # Wounding_C
    rxn[41] = p[69] * y[19] * y[21] / (y[21] + p[51])
    # Production_F
    rxn[42] = p[42] * y[2] / (y[2] + p[66])
    # Clearance_F
    rxn[43] = p[43] * y[20]
    # Wounding_Kd
    rxn[44] = p[68] * y[1] * y[21] / (y[21] + p[70])
    # Wounding_Kq
    rxn[45] = p[67] * y[0] * y[21] / (y[21] + p[70])
    # Clearance_W
    rxn[46] = p[44] * y[21]

    S = numpy.array([[ 0., -1.,  0.,  1.,  0., -1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0., -1.,  0.],
       [ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0., -1.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0., -1.,  0.,  0.],
       [ 0.,  1.,  0., -1.,  0.,  0., -1.,  0.,  1.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0., -1.,  0.,  1.,  0.,  0.,  0., -1.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [-1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1., -1.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 1.,  0., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,
         0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,  0.,  0.,  0.,
         1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,  0.,
         0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,
         0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
        -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1., -1.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         1., -1., -1.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  1., -1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0., -1.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
    
    dy = S.dot(rxn) 
    return dy 


def rxn_fun( y, t, p ): 

    rxn = sympy.zeros(47,1) 
    # Activation_I
    rxn[0] = p[11] * y[4] * y[10] / (y[10] + p[54])
    # Activation_K
    rxn[1] = p[3] * y[0] * y[12] / (y[12] + p[50])
    # Deactivation_I
    rxn[2] = p[10] * y[5]
    # Deactivation_K
    rxn[3] = p[2] * y[2] * y[6] / (y[6] + p[47]) * p[48] / (y[7] + p[48]) * p[49] / (y[8] + p[49])
    # Deactivation_Ks
    rxn[4] = p[6] * y[3]
    # Differentiation
    rxn[5] = p[1] * y[0]
    # Separation
    rxn[6] = p[4] * y[2]
    # Proliferation_Kq
    rxn[7] = p[0] * y[0] / (y[0] + p[45]) * p[46] / (y[6] + p[46])
    # Proliferation_Ka
    rxn[8] = p[0] * y[2] / (y[2] + p[45]) * p[46] / (y[6] + p[46]) * y[8] / (y[8] + p[51]) * y[12] / (y[12] + p[50])
    # Clearance_Kd
    rxn[9] = p[5] * y[1]
    # Clearance_Ks
    rxn[10] = p[7] * y[3]
    # Influx_Iq
    rxn[11] = p[8] + p[9] * y[12] / (y[12] + p[53])
    # Clearance_Iq
    rxn[12] = p[12] * y[4]
    # Mass_Transfer_TGFb
    rxn[13] = p[14] * (y[13] - y[6]) * p[55] / (y[19] + p[55]) * y[20] / (y[20] + p[56])
    # Clearance_TGFb
    rxn[14] = p[13] * y[6]
    # Mass_Transfer_IFNg
    rxn[15] = p[16] * (y[15] - y[7]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_IFNg
    rxn[16] = p[15] * y[7]
    # Mass_Transfer_TNFa
    rxn[17] = p[19] * (y[16] - y[8]) * p[55] / (y[19] + p[55]) * y[20] / (y[20] + p[56])
    # Clearance_TNFa
    rxn[18] = p[17] * y[8]
    # Mass_Transfer_IF
    rxn[19] = p[24] * (y[17] - y[10]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_IF
    rxn[20] = p[23] * y[10]
    # Mass_Transfer_Sig
    rxn[21] = p[27] * (y[18] - y[11]) * p[55] / (y[19] + p[55]) * y[20] / (p[56] + y[20])
    # Clearance_Sig
    rxn[22] = p[26] * y[11]
    # Clearance_TGFa
    rxn[23] = p[21] * y[9]
    # Clearance_IL1
    rxn[24] = p[30] * y[12]
    # Production_TNFa
    rxn[25] = p[18] * y[3] / (y[3] + p[57])
    # Production_IF
    rxn[26] = p[22] * y[2] / (y[2] + p[59])
    # Production_Sig
    rxn[27] = p[25] * y[2] / (y[2] + p[60])
    # Production_TGFa
    rxn[28] = p[20] * y[2] / (y[2] + p[58])
    # Production_IL1
    rxn[29] = p[29] * y[2] / (y[2] + p[61])
    # Release_IL1
    rxn[30] = p[28] * p[68] * y[1] * y[21] / (y[21] + p[51])
    # Release_TGFb
    rxn[31] = p[32] * y[14] + p[33] * y[14] * y[18] / (y[18] + p[62])
    # Clearance_TGFbd
    rxn[32] = p[31] * y[13]
    # Production_IFNgd
    rxn[33] = p[36] * y[5] / (y[5] + p[64])
    # Clearance_IFNgd
    rxn[34] = p[35] * y[15]
    # Production_TNFad
    rxn[35] = p[36] * y[5] / (y[5] + p[64])
    # Clearance_TNFad
    rxn[36] = p[37] * y[16]
    # Clearance_IFd
    rxn[37] = p[38] * y[17]
    # Clearance_Sigd
    rxn[38] = p[39] * y[18]
    # Production_C
    rxn[39] = p[40] * y[0] / (y[0] + p[65])
    # Clearance_C
    rxn[40] = p[41] * y[19]
    # Wounding_C
    rxn[41] = p[69] * y[19] * y[21] / (y[21] + p[51])
    # Production_F
    rxn[42] = p[42] * y[2] / (y[2] + p[66])
    # Clearance_F
    rxn[43] = p[43] * y[20]
    # Wounding_Kd
    rxn[44] = p[68] * y[1] * y[21] / (y[21] + p[70])
    # Wounding_Kq
    rxn[45] = p[67] * y[0] * y[21] / (y[21] + p[70])
    # Clearance_W
    rxn[46] = p[44] * y[21]
    return rxn 
