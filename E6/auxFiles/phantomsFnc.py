import numpy as np
from auxFnc import get_coef

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def cube_phantom_nh(edge_size, energy):
    soft_coef = round(get_coef(4, energy), 2)
    air_coef = round(get_coef(1, energy), 2)
    water_coef = round(get_coef(5, energy), 2)
    print(soft_coef, air_coef, water_coef)
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        tissue_edge = int(edge_size / 2)
        offset = int((edge_size - tissue_edge) / 2)
        phantom = np.zeros((edge_size, edge_size, edge_size))
        phantom[:, :, :] = air_coef
        phantom[:, :, tissue_edge:] = water_coef
        phantom[offset:offset + tissue_edge, offset: offset +
                tissue_edge, offset:offset+tissue_edge] = soft_coef
        return phantom
    else:
        print('not powers of 2')
        return

def breast_phantom(edge_size, energy):
    breast_coef = get_coef(3,energy)
    air_coef = get_coef(1,energy)
    soft_coef = get_coef(4,energy)
    adipose_coef = get_coef(0,energy)

    print(round(air_coef, 2), round(adipose_coef, 2), round(breast_coef, 2), round(soft_coef, 2))
    cell_size = 24
    frame = np.full((edge_size, edge_size, edge_size), air_coef)
    # biggest photon
    frame[cell_size * 3:cell_size * 7, (edge_size - cell_size * 4) // 2 - 8:(edge_size - cell_size * 4) // 2 + cell_size*4 - 8, :cell_size*8] = adipose_coef
    # rightest photon
    frame[cell_size*4:cell_size * 6, (edge_size - cell_size * 2) // 2 - 8:(edge_size - cell_size * 2) // 2 + cell_size*2 - 8, cell_size*8:cell_size*10] = adipose_coef
    # breast tissue
    frame[cell_size*4:cell_size * 6, (edge_size // 2) - cell_size - 8:(edge_size // 2) + cell_size - 8, cell_size*2:cell_size*4] = breast_coef
    # leftest soft photon
    frame[cell_size*4+cell_size // 2:6*cell_size - cell_size // 2 , (edge_size // 2) - cell_size // 2 - 8:(edge_size // 2) + cell_size // 2 - 8, cell_size*2 + cell_size//2:cell_size*3 + cell_size // 2] = soft_coef
    # rightest soft photon
    frame[cell_size*4+cell_size // 2:6*cell_size - cell_size // 2 , (edge_size // 2) - cell_size // 2 - 8:(edge_size // 2) + cell_size // 2 - 8, cell_size*8 + cell_size // 2:cell_size*9 + cell_size // 2] = soft_coef
    # middle soft photon
    frame[cell_size*4+cell_size // 2:6*cell_size - cell_size // 2 , (edge_size // 2) - cell_size // 2 - 8:(edge_size // 2) + cell_size // 2 - 8, cell_size*5 + cell_size // 2:cell_size*6 + cell_size // 2] = soft_coef

    return frame