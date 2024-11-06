import numpy as np
from auxFnc import get_coef

def cube_phantom_h(edge_size, energy):
    soft_coef = round(get_coef(index=4, energy=energy), 2)
    bone_coef = round(get_coef(index=2, energy=energy), 2)
    air_coef = round(get_coef(index=1, energy=energy), 2)
    print(soft_coef, bone_coef)

    air_size = edge_size * 2
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        soft_tissue_size = edge_size
        bone_size = int(edge_size / 2)
        tissue = np.zeros(
            (soft_tissue_size, soft_tissue_size, soft_tissue_size))
        tissue[:] = soft_coef
        offset = int((soft_tissue_size - bone_size) / 2)
        tissue[offset:offset + bone_size, offset: offset + bone_size, offset:offset+bone_size] = bone_coef
        # tissue = np.full((air_size, air_size, air_size), air_coef)
        # offset_soft = int((air_size / 2) - (edge_size / 2))
        # tissue[offset_soft:offset_soft + edge_size, offset_soft: offset_soft + edge_size, offset_soft:offset_soft + edge_size] = soft_coef
        
        # bone_size = int(edge_size / 2)

        # offset_bone = int((air_size - bone_size) / 2)
        # tissue[offset_bone:offset_bone + bone_size, offset_bone: offset_bone + bone_size, offset_bone:offset_bone + bone_size] = bone_coef
        return tissue
    else:
        print('not powers of 2')
        return