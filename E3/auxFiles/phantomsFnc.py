import numpy as np
from IoFnc import get_coef


def cube_phantom_h(edge_size, energy):
    soft_coef = get_coef(index=4, energy=energy)
    bone_coef = get_coef(index=2, energy=energy)
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        soft_tissue_size = edge_size
        bone_size = int(edge_size / 2)
        tissue = np.zeros(
            (soft_tissue_size, soft_tissue_size, soft_tissue_size))
        tissue[:] = soft_coef
        offset = int((soft_tissue_size - bone_size) / 2)
        tissue[offset:offset + bone_size, offset: offset +
               bone_size, offset:offset+bone_size] = bone_coef
        # normalize
        # tissue = utils.normalize_data(tissue)
        return tissue
    else:
        print('not powers of 2')
        return


def cube_phantom_nh(edge_size, energy):
    soft_coef = get_coef(4, energy)
    air_coef = get_coef(1, energy)
    water_coef = get_coef(5, energy)
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        tissue_edge = int(edge_size / 2)
        offset = int((edge_size - tissue_edge) / 2)
        phantom = np.zeros((edge_size, edge_size, edge_size))
        phantom[:, :, :] = water_coef
        phantom[:, :, tissue_edge:] = air_coef
        phantom[offset:offset + tissue_edge, offset: offset +
                tissue_edge, offset:offset+tissue_edge] = soft_coef
        # phantom = utils.normalize_data(phantom)
        return phantom
    else:
        print('not powers of 2')
        return

def breast_phantom(edge_size, energy):
    breast_coef = get_coef(3,energy)
    air_coef = get_coef(1,energy)
    soft_coef = get_coef(4,energy)
    adipose_coef = get_coef(0,energy)


    cell_size = edge_size//18
    frame = np.full((edge_size, edge_size, edge_size), air_coef)
    mid_point = edge_size//2

    # putting breast adipose 
    frame[1 + mid_point - 4*cell_size: mid_point + 3*cell_size + 1,
          mid_point - 3*cell_size: mid_point + 4*cell_size,
          mid_point - 10 - 6*cell_size: mid_point + 3*cell_size - 10] = adipose_coef
      
    # putting breast tissue 
    frame[1 + mid_point - 2*cell_size: mid_point + cell_size + 1,
          mid_point - cell_size: mid_point + 2*cell_size,
          mid_point - 10 - 5*cell_size: mid_point - 2*cell_size - 10] = breast_coef
    
    # putting soft tissue
    frame[1 + mid_point - cell_size: mid_point + 1,
          mid_point: mid_point + cell_size,
          mid_point - 10 - 4*cell_size: mid_point - 3*cell_size - 10] = soft_coef

    # putting right most square
    frame[1 + mid_point - 2*cell_size: mid_point + cell_size + 1,
          mid_point - cell_size: mid_point + 2*cell_size,
          mid_point - 10 + 3*cell_size: mid_point + 6*cell_size - 10] = adipose_coef
      
    # putting second soft tissue
    frame[1 + mid_point - cell_size: mid_point + 1,
          mid_point: mid_point + cell_size,
          mid_point - 10 - cell_size: mid_point - 10] = soft_coef

    # putting third soft tissue
    frame[1 + mid_point - cell_size: mid_point + 1,
          mid_point: mid_point + cell_size,
          mid_point - 10 + 4*cell_size: mid_point + 5*cell_size - 10] = soft_coef
    
    return frame