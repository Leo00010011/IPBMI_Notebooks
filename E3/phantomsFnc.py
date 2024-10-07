import numpy as np
from utils import utils

def cube_phantom_h(edge_size, energy):
  soft_coef = utils.get_coef(index=4, energy=energy)
  bone_coef = utils.get_coef(index=2, energy=energy)
  if edge_size > 2 and np.log2(edge_size) % 1 == 0:
    soft_tissue_size = edge_size
    bone_size = int(edge_size / 2)
    tissue = np.zeros((soft_tissue_size, soft_tissue_size, soft_tissue_size))
    tissue[:] = soft_coef
    offset = int((soft_tissue_size - bone_size) / 2)
    tissue[offset:offset + bone_size, offset: offset+bone_size, offset:offset+bone_size] = bone_coef
    # normalize
    # tissue = utils.normalize_data(tissue)
    return tissue
  else:
    print('not powers of 2')
    return
  
def cube_phantom_nh(edge_size, energy):
  soft_coef = utils.get_coef(4, energy)
  air_coef = utils.get_coef(1, energy)
  water_coef = utils.get_coef(5, energy)
  if edge_size > 2 and np.log2(edge_size) % 1 == 0:
    tissue_edge = int(edge_size / 2)
    offset = int((edge_size - tissue_edge) / 2)
    phantom = np.zeros((edge_size, edge_size, edge_size))
    phantom[:, :, :] = water_coef
    phantom[:, :, tissue_edge:] = air_coef
    phantom[offset:offset + tissue_edge, offset: offset+tissue_edge, offset:offset+tissue_edge] = soft_coef
    # phantom = utils.normalize_data(phantom)
    return phantom
  else:
    print('not powers of 2')
    return 
  

def breast_phantom(edge_size, energy):
    cell_size = edge_size//18
    frame = np.full((edge_size, edge_size, edge_size),1)
    mid_point = edge_size//2
    # putting breast base
    frame[mid_point - 6*cell_size: mid_point + 3*cell_size,
          mid_point - 4*cell_size: mid_point + 3*cell_size,
          mid_point - 3*cell_size: mid_point + 4*cell_size] = 0
    return frame
    