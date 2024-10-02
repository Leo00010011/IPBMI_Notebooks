import numpy as np
from utils import utils

def cube_phantom_h(edge_size, energy):
  soft_coef = utils.get_coef(index=4, energy=energy)
  bone_coef = utils.get_coef(index=2, energy=energy)
  if np.log2(edge_size) != 1 and np.log2(edge_size) % 1 == 0:
    soft_tissue_size = edge_size
    bone_size = int(edge_size / 2)
    tissue = np.zeros((soft_tissue_size, soft_tissue_size, soft_tissue_size))
    tissue[:] = soft_coef
    offset = (soft_tissue_size - bone_size) / 2
    offset = int(offset)
    tissue[offset:offset + bone_size, offset: offset+bone_size, offset:offset+bone_size] = bone_coef
    return tissue
  else:
    print('not powers of 2')
    return 