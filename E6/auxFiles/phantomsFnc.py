import numpy as np
from auxFnc import get_coef

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def breast_phantom(edge_size, energy):
    breast_coef = get_coef(3,energy)
    air_coef = get_coef(1,energy)
    soft_coef = get_coef(4,energy)
    adipose_coef = get_coef(0,energy)

    print(round(air_coef, 2), round(adipose_coef, 2), round(breast_coef, 2), round(soft_coef, 2))


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

def insertArtifact(obj, pos, sizeArtifact, mu):
   return