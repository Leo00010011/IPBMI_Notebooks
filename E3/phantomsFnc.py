import numpy as np

def cube_phantom_h(edge_size, energy):
  tissue_size = edge_size
  bone_size = int(edge_size / 2)
  tissue = np.zeros((edge_size, edge_size, edge_size))
  bone = np.zeros((bone_size, bone_size, bone_size))
  return tissue