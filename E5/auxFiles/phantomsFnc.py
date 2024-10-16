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
    print('N0:',N0)
    print('obj:',obj)
    print('prj:',prj)