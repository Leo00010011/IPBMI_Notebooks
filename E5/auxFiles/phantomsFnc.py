import numpy as np
from auxFiles.auxFnc import get_coef

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def cube_phantom_nh(edge_size, energy):
    soft_coef = get_coef(4, energy)
    air_coef = get_coef(1, energy)
    water_coef = get_coef(5, energy)
    print(soft_coef, air_coef, water_coef)
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        tissue_edge = int(edge_size / 2)
        offset = int((edge_size - tissue_edge) / 2)
        phantom = np.zeros((edge_size, edge_size, edge_size))
        phantom[:, :, :] = water_coef
        phantom[:, :, tissue_edge:] = air_coef
        phantom[offset:offset + tissue_edge, offset: offset +
                tissue_edge, offset:offset+tissue_edge] = soft_coef
        return phantom
    else:
        print('not powers of 2')
        return
    
def interactor_PR(N0, obj, prj):
    # N0 * e^{-mux}
    # N_0e^{-\mu (x+z)} = N_0e^{-\mu x}e^{-\mu z}
    coef_sum = 0.0
    if prj == 'frontal':
        coef_sum = np.sum(obj, axis=2)
    elif prj == 'lateral':
        coef_sum = np.sum(obj, axis=0)
    else:
        print('please input the right parameter: frontal or lateral')
        return False
    print(coef_sum)
    return N0 * obj.shape[0] * np.exp(-coef_sum)

def getNumberPhotons(qImage):
    photons_num = np.sum(qImage)
    return photons_num